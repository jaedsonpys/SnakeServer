def custom_log(message, type, new_line=False):
    if new_line:
        print()

    if type == 'error':
        print(f'[\033[31m  ERROR  \033[m] {message}')
    elif type == 'sucess':
        print(f'[\033[32m  SUCESS  \033[m] {message}')
    elif type == 'started':
        print(f'[\033[32m  STARTED  \033[m] {message}')
    elif type == 'disconnected':
        print(f'[\033[31m  DISCONNECTED  \033[m] {message}')
    elif type == 'warning':
        print(f'[\033[34m  WARNING  \033[m] {message}')
    elif type == 'loading':
        print(f'[\033[33m  LOADING  \033[m] {message}')


def welcome_message():
    print('              SnakeServer © 2021            ')
    print('=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*=*')
    print('It\'s not just a server, this is SnakeServer')
    print('=*=*=*=*=*=*=*=**=*  LOG  =*=*=*=*=*=*=*=*=*')