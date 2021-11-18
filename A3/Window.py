import logging
import math
from packet import *
from config import *


class Frame:
    '''
    The class is to create a Frame.
    '''
    def __init__(self, seq_num, payload=None, is_last=False):
        # sequence number
        self.seq_num = seq_num
        # set data
        self.payload = payload
        self.is_last = is_last
        self.send_state = False
        self.ACK = False
        self.timer = 0
            
            
class Window:
    '''
    The Class is to create sliding windows for Selective Repeat.
    '''
    
    def __init__(self):
        # pointer to window start
        self.ptr = 0
        # set data
        self.frames = []
        self.num_frames = 0
        self.fini = False
        
    def create_sender_window(self, msg):
        '''
        The method is to create a sending window.
        :param: msg
        '''
        # number of packets
        self.num_frames = math.ceil(len(msg)/PAYLOAD_SIZE)
        logging.debug(f'len(msg) is : {len(msg)}')
        logging.debug(f'num of frames is : {self.num_frames}')
        # init all packets
        for i in range(self.num_frames):
            if i == self.num_frames - 1:
                self.frames.append(Frame(i+1, msg[i*PAYLOAD_SIZE:],True))
            else:
                self.frames.append(Frame(i+1, msg[i*PAYLOAD_SIZE: (i+1)*PAYLOAD_SIZE],False))
                
    def get_sendable_frames(self):
        '''
        The method is to get all sendable packets in window.
        :return: list of frames
        '''
        list_frames = []
        # sliding window is 5 size
        for i in range(self.ptr, self.ptr + WINDOW_SIZE):
            if i >= len(self.frames): break
            a_frame = self.frames[i]
            # if send state is False, then add this frame in the list.
            if not a_frame.send_state:
                list_frames.append(a_frame)
                
        return list_frames 
    
    def update_window(self, seq_num):
        '''
        The method is to update window, When received an ACK. 
        If possible, slide window.
        :param: seq_num
        '''
        self.frames[seq_num - 1].ACK = True
        offset = 0
        for i in range(self.ptr, self.ptr + WINDOW_SIZE):
            if i >= len(self.frames): break
            if self.frames[i].ACK:
                offset += 1
            else: 
                # if this frame is not ACK, then break so that the pointer will point this frame to wait.
                break
        # pointer moves right if possible.
        self.ptr += offset
        
    def handle_packet(self, aPacket):
        '''
        The method is to process a packet when it is out of the window or already received.
        '''
        index_window = aPacket.seq_num - 1
        if index_window >= self.ptr and index_window < self.ptr + WINDOW_SIZE:
            while index_window >= len(self.frames):
                # already received
                self.frames.append(None)
            if self.frames[index_window] is None:
                self.frames[index_window] = Frame(index_window, aPacket.payload, True)
                self.update_window(index_window)
                
        else:
            # discard the packet
            pass
        
        
    def is_waiting_packet(self):
        '''
        The method is to check whether all frames has been ACKed.
        :return: boolean
        '''
        for i in range(self.num_frames):
            if not self.frames[i].ACK:
                return True
        return False
    
    def check_finish(self):
        '''
        The method is to check whether the frame is last one and then update fini state.
        :return: fini
        '''
        if self.frames:
            # get last frame
            f = self.frames[-1]
            if f.is_last and self.ptr == len(self.frames):
                # update fini state
                self.fini = True
        
        return self.fini
    
    
    
        
        
        
        
    
    
            
        
    