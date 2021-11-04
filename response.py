# Módulo utilizado pelo usuário e pelo próprio
# SnakeServer.

from http_parser.pyparser import HttpParser

class NewResponse:
    def __init__(self, content_type: str='text/plain',
                status=200, response=None, headers: dict={},
                connection='Keep-Alive', keep_alive='timeout=5',
                cookies: dict={}
            ):

        http = ''

        # Contruindo mesagem HTTP
        http += f'HTTP/1.1 {status}\r\n'
        http += f'Acess-Control-Allow-Origin: *\r\n'
        http += f'Connection: {connection}\r\n'
        http += f'Keep-Alive: {keep_alive}\r\n'
        http += 'Server: SnakeServer\r\n'
        
        if len(headers) != 0:
            for k,v in headers.items():
                http += f'{k}: {v}\r\n'

        if len(cookies) != 0:
            for k,v in cookies.items():
                http += f'Set-Cookie: {k}={v}\r\n'

        http += f'Content-Type: {content_type}'
        
        if response:
            http += '\n\n'
            http += response


        return http