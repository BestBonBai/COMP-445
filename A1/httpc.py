'''
COMP 445 lab assignment 1

-- cURL-like Command Line Implementation

@ authors: Hualin Bai (40053833), Qichen Liu (40055916)
@ date: 2021-09-20
@ version: 1.0.0

'''

def httpc_help_menu():
    '''
    The method is to return help menu for httpc.
    '''
    print('\nhttpc is a curl-like application but supports HTTP protocol only.\n' +
          'Usage: \n' + '\t httpc command [arguments]\n'
          + 'The commands are: \n' + 
          '\t get    executes a HTTP GET request and prints the response.\n' +
          '\t post   executes a HTTP POST request and prints the resonse.\n' +
          '\t help   prints this screen.\n')

def httpc_help_get_menu():
    print('\nusage: httpc get [-v] [-h key:value] URL\n' +
            'Get executes a HTTP GET request for a given URL.\n' +
             '\t -v Prints the detail of the response such as protocol, status, and headers.\n' +
             '\t -h key:value Associates headers to HTTP Request with the format \'key:value\'.\n')

def httpc_help_post_menu():
    print('\nusage: httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL\n' +
            'Post executes a HTTP POST request for a given URL with inline data or from file.\n' +
             '\t -v Prints the detail of the response such as protocol, status, and headers.\n' +
             '\t -h key:value Associates headers to HTTP Request with the format \'key:value\'.' +
             '\t -d string Associates an inline data to the body HTTP POST request.\n' +
             '\t -f file Associates the content of a file to the body HTTP POST request\n' +
             'Either [-d] or [-f] can be used but not both.\n')

print("-"*50)
print("\t A simple HTTP client application")
print("-"*50)

while True:
    command = input('Please input a command or \'exit\' :\n')
    num_words = command.split(' ')

    # exit
    if command == 'exit': break
    
    # help menu cases
    if len(num_words) == 2 and num_words[0] == 'httpc' and num_words[1] == 'help':
        httpc_help_menu()
    if len(num_words) == 3 and num_words[0] == 'httpc' and num_words[1] == 'help' and num_words[2] == 'get':
        httpc_help_get_menu()
    if len(num_words) == 3 and num_words[0] == 'httpc' and num_words[1] == 'help' and num_words[2] == 'post':
        httpc_help_post_menu()