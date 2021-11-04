# Módulo utilizado pelo usuário e pelo próprio
# SnakeServer.

class Response:
    def __init__(self, content_type: str='text/plain',
                status=200, response=None, headers: dict={},
                connection='Keep-Alive', keep_alive='timeout=5',
                cookies: dict={}
            ):

        self.http = ''

        # Contruindo mesagem HTTP
        self.http += f'HTTP/1.1 {status}\r\n'
        self.http += f'Acess-Control-Allow-Origin: *\r\n'
        self.http += f'Connection: {connection}\r\n'
        self.http += f'Keep-Alive: {keep_alive}\r\n'
        self.http += 'Server: SnakeServer\r\n'
        
        if len(headers) != 0:
            for k,v in headers.items():
                self.http += f'{k}: {v}\r\n'

        if len(cookies) != 0:
            for k,v in cookies.items():
                self.http += f'Set-Cookie: {k}={v}\r\n'

        self.http += f'Content-Type: {content_type}'
        
        if response:
            self.http += '\n\n'
            self.http += response
            