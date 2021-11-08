from http_parser.pyparser import HttpParser
from utils.urlmanager import URL

class Request:
    def new(self, message):
        hp = HttpParser()
        hp.execute(message, len(message))

        self.path = hp.get_path()
        self.method = hp.get_method()
        self.headers = hp.get_headers()
        self.query = hp.get_query_string()
        self.body = hp.recv_body()

        if self.path is None and self.method is None:
            return False

        self.__cookie()
        self.__query()

        return True

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
                __cookie = str(i).replace(' ', '').split('=')
                self.cookies[__cookie[0]] = __cookie[1]


    def __query(self):
        # Essa função obtém todos os parâmetros de URL
        # e os guarda em um objeto. #
        
        self.params = {}

        if not len(self.query) == 0:
            __query_list = str(self.query).split('&')

            for i in __query_list:
                __query = i.split('=')
                self.params[__query[0]] = __query[1]
