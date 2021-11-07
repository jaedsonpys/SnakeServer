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

        self.__cookies = {}

        if 'COOKIE' in self.headers.keys():
            __cookies_list = str(self.headers['COOKIE']).split(';')
            
            for i in __cookies_list:
                __cookie = str(i).replace(' ', '').split('=')
                self.__cookies[__cookie[0]] = __cookie[1]


    def get_header(self, key: str):
        '''Obtém um header através
        do seu nome.
        
        :param key: Nome do header'''

        # Função para disponibilizar os cookies
        # para o usuário.

        if key in self.headers.keys():
            return self.headers[key]
        else:
            return None


    def __query(self):
        # Essa função obtém todos os parâmetros de URL
        # e os guarda em um objeto. #
        
        self.__querys = {}

        if not len(self.query) == 0:
            __query_list = str(self.query).split('&')

            for i in __query_list:
                __query = i.split('=')
                self.__querys[__query[0]] = __query[1]


    def get_query(self, name: str):
        '''Obtém uma query (ou parâmetro) da URL através do
        seu nome:
        
        :param key: Nome da query'''

        if name in self.querys:
            return URL().decode(self.querys[name])
        else:
            return None


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