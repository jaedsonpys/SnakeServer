from http_parser.pyparser import HttpParser

class Request:
    def __init__(self, message):
        hp = HttpParser()
        hp.execute(message, len(message))

        self.path = hp.get_path()
        self.method = hp.get_method()
        self.headers = hp.get_headers()
        self.params = hp.get_query_string()
        self.body = hp.recv_body()

        self.__cookie()


    def __cookie(self):
        # Essa função registra e separa os cookies
        # disponibilizados através do header.
        # 
        # Os cookies são obtidos assim que a requisição
        # começa a ser processada. #

        self.cookies = {}

        if 'COOKIE' in self.headers.keys():
            cookies_list = str(self.headers['COOKIE']).split(';')
            
            for i in cookies_list:
                i = str(i).replace(' ', '')
                cookie = i.split('=')

                self.cookies[cookie[0]] = cookie[1]

            print(self.cookies)


    def get_cookie(self, key: str):
        ''''Obtém o valor de um cookie
        através do seu nome.

        Se o valor retornado for None, o cookie
        não existe.
        
        :param key: Nome do cookie'''

        if key in self.cookies:
            return self.cookies[key]
        else:
            return None