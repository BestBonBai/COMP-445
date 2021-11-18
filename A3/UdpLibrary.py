import logging
from math import trunc
import time
import socket
import sys
import threading
from packet import *
from config import *
from Window import *

class UdpLibrary:
    '''
    The class is to implement UDP functions to connect client and server.
    
    '''
    def __init__(self):
        self.conn = None
        self.router_addr = None
        self.packate_builder = None
       
    def connect_client(self):
        '''
        The method is to connect client by 3-way handshakes.
        '''   
        # UDP
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn.bind(('', SERVER_PORT))
        logging.info("Server is listening at {}:{}".format(SERVER_IP,SERVER_PORT) )
        
        pkt = self.get_packet(TIME_ALIVE)
        if pkt is None:
            logging.debug('Connecting is timeout.')
            return False
        
        # if pkt type is syn, then send ACK SYN
        # if already ACKed, return true
        if pkt.packet_type == PACKET_TYPE_SYN:
            pkt.packet_type = PACKET_TYPE_SYN_AK
            self.conn.sendto(pkt.to_bytes(), self.router_addr )
            logging.info('Client connection is established')
            return True
        else:
            # otherwise, return False
            return False
        
        
        
    def get_packet(self, timeout):
        '''
        The method is to get packet cosidering timeout.
        :return: packate
        '''
        self.conn.settimeout(timeout)
        try:
            data, addr = self.conn.recvfrom(PACKET_SIZE)
            pkt = Packet.from_bytes(data)
            logging.debug("Received: {}:{}".format(pkt, pkt.payload))
            self.router_addr = addr
            
            if self.packate_builder is None:
                self.packate_builder = PacketBuilder(pkt.peer_ip_addr, pkt.peer_port)
            
        except socket.timeout:
            logging.debug('Time out for recvfrom message !!!')
            pkt = None
        finally:
            return pkt
    
    def send_msg(self, msg):
        '''
        The method is to send message from sending window.
        :param: msg
        '''
        window = Window()
        window.create_sender_window(msg)
        
        threading.Thread(target=self.handle_listener, args=(window,) ).start()
        while window.is_waiting_packet():
            # check if it has some packets need to be send in window.
            for f in window.get_sendable_frames():
                pkt = self.packate_builder.build(PACKET_TYPE_DATA, f.seq_num, f.payload, )
                self.conn.sendto(pkt.to_bytes(), self.router_addr )
                logging.debug('Send Message is : {}'.format(pkt.payload))
                # set timer
                f.timer = time.time()
                # set send state
                f.send_state = True
        
        
    def handle_listener(self, window):
        '''
        The method is to handle listener that listen response from server.
        :param: window
        '''
        while window.is_waiting_packet():
            # find packets that have been sent, but not ACK. 
            # then check if their timer is timeout or not.
            try:
                self.conn.settimeout(TIME_OUT)
                response, sender = self.conn.recvfrom(PACKET_SIZE)
                pkt = Packet.from_bytes(response)
                logging.debug('Received Response is : \n {}:{}'.format(pkt, pkt.payload.decode("utf-8")))
                if pkt.packet_type == PACKET_TYPE_AK:
                    window.update_window(pkt.seq_num)
                    
            except socket.timeout:
                logging.debug('Time out when waiting ACK')
                for i in range(window.ptr, window.ptr + WINDOW_SIZE):
                    if i >= len(window.frames):
                        break
                    f = window.frames[i]
                    if f.send_state and not f.ACK:
                        # reset send state, then it will be re-sent
                        f.send_state = False
        logging.debug('Listener has checked the window!')
    
    
    def recv_msg(self):
        '''
        The method is to receive message from receiving window.
        :return: data (bytes)
        '''
        window = Window()
        while not window.check_finish():
            pkt = self.get_packet(TIME_OUT_RECV)
            # case : no msg
            if pkt is None:
                logging.debug('No message received in timeout time.')
                return None
            # case : discard possible packet from handshake
            if pkt.seq_num == 0 and pkt.packet_type == PACKET_TYPE_AK:
                continue
            window.handle_packet(pkt)
            # send ACK to router
            pkt.packet_type = PACKET_TYPE_AK
            self.conn.sendto(pkt.to_bytes(), self.router_addr)
            
        # get data from window
        data = self.get_data(window)
        return data
    
        
    def get_data(self, window):
        '''
        The method is to get byte data of all frames in window.
        :param: window
        :return: data
        '''
        data = b''
        for f in window.frames:
            data += f.payload
        return data
        
    
    def close_connect(self):
        '''
        The method is to close the connection : FIN, ACK, FIN, ACK
        '''
        logging.info('Disconnecting...')
        self.conn.close()
        
     
    def connect_server(self):
        '''
        The method is to connect server by 3-way handshakes.
        '''
        logging.info('Connecting to {}:{}'.format(SERVER_IP, SERVER_PORT))
        self.router_addr = (ROUTER_IP, ROUTER_PORT)
        peer_ip = ipaddress.ip_address(socket.gethostbyname(SERVER_IP))
        self.packate_builder = PacketBuilder(peer_ip,SERVER_PORT)
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # send SYN to peer
            pkt = self.packate_builder.build(PACKET_TYPE_SYN)
            self.conn.sendto(pkt.to_bytes(), self.router_addr)
            self.conn.settimeout(TIME_ALIVE)
            logging.debug('Client waiting for a response from the server')
            # Expecting SYN_ACK
            response, sender = self.conn.recvfrom(PACKET_SIZE)
            pkt = Packet.from_bytes(response)
            logging.debug('Server connection is established')
         
        except socket.timeout:
            logging.debug('Connection is Timeout')
            self.conn.close()
            sys.exit(0)
            
        if pkt.packet_type == PACKET_TYPE_SYN_AK:
            # send ACK
            pkt = self.packate_builder.build(PACKET_TYPE_AK)
            self.conn.sendto(pkt.to_bytes(),self.router_addr)
            return True
        else:
            logging.debug("Unexpected packet: {}".format(pkt))
            self.conn.close()
            sys.exit(0)
        
        
        