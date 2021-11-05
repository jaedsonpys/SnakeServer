# Arquivo principal de inicialização
import socket

from utils.log_server import custom_log
from response import Response
from request import Request
import json


class Snake:
    __ROUTES = {}
    __http_codes = {
        'client': {
            '400': {
                'Body': '@default-page',
                'Message': 'Bad Request'
            },
            '401': {
                'Body': '@default-page',
                'Message': 'Unauthorized'
            },
            '403': {
                'Body': '@default-page',
                'Message': 'Forbidden'
            },

            '404': {
                'Body': '@default-page',
                'Message': 'Page not Found'
            },
            '405': {
                'Body': '@default-page',
                'Message': 'Method not Allowed'
            },
            '406': {
                'Body': '@default-page',
                'Message': 'Not Acceptable'
            },
            '407': {
                'Body': '@default-page',
                'Message': 'Proxy Authentication Required'
            },
            '408': {
                'Body': '@default-page',
                'Message': 'Request Timeout'
            },
            '409': {
                'Body': '@default-page',
                'Message': 'Conflict'
            },
            '413': {
                'Body': '@default-page',
                'Message': 'Payload Too Large'
            },
            '414': {
                'Body': '@default-page',
                'Message': 'URI Too Long'
            },
            '415': {
                'Body': '@default-page',
                'Message': 'Unsupported Media Type'
            },
            '429': {
                'Body': '@default-page',
                'Message': 'Too Many Requests'
            }
        }
    }

    def __init__(self, host='127.0.0.1', port=3000) -> None:
        self.port = port
        self.host = host

        self.__address = (self.host, self.port)


    # Filtrando portas em strings para inteiro
    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        if isinstance(port, str):
            self._port = int(port)
        else:
            self._port = port


    # Filtrando parâmetro host vazio ou inválido
    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        if len(host) == 0:
            self._host = '127.0.0.1'
        elif len(host) < 7:
            custom_log('HOST especificado inválido', 'error')
            exit()
        else:
            self._host = host


    def start(self) -> None:
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            # O servidor será iniciado no endereço
            # que foi especificado em self.__address.
            # 
            # Limite máximo para testes de 5000 conexões.
            # #

            self.server.bind(self.__address)
            self.server.listen(5000)
        except socket.error as err:
            # Lista de erros possíveis ao iniciar socket:
            # 
            # 1. 98: Endereço já em uso
            # 2. 99: Não é possível identificar o endereço especificado
            # #

            if err.args[0] == 98:
                custom_log('O endereço especificado já está sendo utilizado.', 'error')
            elif err.args[0] == 99:
                custom_log('Endereço especificado inválido', 'error')
            else:
                print(err)

            exit()

        # Se não houver erros, a função que começa
        # a aguardar conexões é chamada.

        custom_log(f'Servidor iniciado em: http://{self.host}:{self.port}', 'sucess')
        self.__wait_requests()

    
    def __wait_requests(self):
        # Nessa função, o servidor fica esperando 
        # por requisições feitas por meio de um navegador,
        # e após isso, ler a mensagem HTTP para obter headers.
        # #

        while True:
            try:
                client, address = self.server.accept()
                self.__client_info = (client, address)

                # Se alguma conexão for recebida, receba dados
                # da requisição
                if address:
                    http_request = client.recv(1024)

                    self.__request_info = Request(http_request)
                    self.request = self.__request_info

                    # Com esses dados da requisição, podemos agora, processar
                    # esses dados para enviar uma resposta ao cliente. #
                    self.__process_request()

                    # Após a solicitação ser processada e enviada,
                    # podemos fechar a conexão com o cliente. #
                    client.close()
            except KeyboardInterrupt:
                try:
                    self.server.close()
                    client.close()
                except:
                    pass
                finally:
                    del self.server

                    custom_log('Fechando servidor...', 'loading', True)
                    exit()

    def __process_request(self):
        # Aqui processamos a requisição feita,
        # sabendo para onde o cliente vai e o que
        # ele quer receber.
        # 
        # Primeiro, vamos saber se a rota em que o usuário
        # está solicitando existe:

        if self.__request_info.path in self.__ROUTES.keys():
            # Agora verificamos se a rota aceita o método
            # da solicação:
            self.__route = self.__request_info.path

            if self.__request_info.method == self.__ROUTES[self.__route]['method']:
                # Tudo está correto, agora basta apenas responder:
                self.__prepare_response()
                pass
            else:
                # Caso a rota não aceita esse método que foi solicitado
                # pelo usuário, retorne um erro 405.
                self.__prepare_response(405)

        else:
            # Caso a rota solicitada pelo usuário não exista,
            # uma resposta com o erro 404 é enviada. #
            self.__prepare_response(404)


    def __prepare_response(self, status=None):
        # Envia a resposta para o usuário

        # Essa condição é especialmente para códigos de status
        # HTTP. #
        if status:
            status = str(status)

            # As linhas abaixo obtém as informações sobre o código especifico.
            #
            # É necessário para verificar se há uma página de erro
            # personalizada que o usuário deseja mostrar ao erro ser
            # disparado pelo servidor.
            # 
            # Além de conter o Content-Type da resposta a ser enviada,
            # que ajudar na criação de APIs, sendo da escolha do usuário
            # retornar JSON, HTML, e outros tipos.

            http_code_info = self.__http_codes['client'][status]

            # Se não houver uma página de erro personalizada 
            # retorne a padrão. #
            if http_code_info['Body'] == '@default-page':
                with open('pages/error.html', 'r') as ep:
                    error_page = str(ep.read())
                    ep.close()

                # Formatando os dados que vão na página
                response = error_page.format(message=http_code_info['Message'], status=status)

                # Construindo resposta HTTP
                http_response = Response(content_type='text/html', status=status, response=response)

                return self.__send_response(http_response)
            else:
                # Chamando a função que vai retornar uma resposta
                # para o erro. #
                response = http_code_info['Body']()

                if not response:
                    custom_log(f'A rota {self.__route} não retornou uma resposta válida', 'error')
                    self.__client_info[0].close()
                    exit()

                return self.__send_response(response)

        # Diferente do código acima, aqui as respostas
        # serão definidas pela função em que o usuário
        # definiu como resposta as registrar uma nova
        # rota.
        #
        # O código de status também é definido pelo
        # usuário, caso ele não esteja presente, 200
        # é o padrão.
        # 
        # Se a função não retornar nada, será taxada
        # como inválida e um erro é acionado.

        function_response = self.__ROUTES[self.__route]['target']()

        # Se a função não retornar algo válido
        if not function_response:
            custom_log(f'A rota {self.__route} não retornou uma resposta válida', 'error')
            self.__client_info[0].close()
            exit()

        return self.__send_response(function_response)


    def __send_response(self, response):
        # Tentando enviar a resposta ao usuário
        if isinstance(response, object):
            self.__client_info[0].send(response.http.encode())
        else:
            self.__client_info[0].send(response.encode())

        custom_log(f'HTTP {self.__request_info.method} {self.__request_info.path}: {self.__client_info[1]}', 'sucess')
        return


    def add_new_route(self, name, method, target):
        '''Para criar suas rotas, basta adicionar o nome dela (Ex. /login), o
        método (POST ou GET) e a função que vai ser chamada quando uma solicitação
        for feita a essa rota.
        
        :param name: Nome da rota. Ex: /login.
        :param method: Método da rota (POST ou GET).
        :param target: Função a ser ativada ao receber uma solicitação.'''

        method = str(method).upper()

        # Registrando a rota
        self.__ROUTES[name] = {
            'method': method,
            'target': target
        }


    def add_error_page(self, error, target):
        '''A função especificada no parâmetro target
        será chamada quando o erro for disparado.
        
        Por exemplo, o erro 404 dispara uma função
        que retorna um página informando o problema.

        :param target: Função a ser chamada.
        :param error: Erro que vai ser disparado.'''

        if error > 400 and error < 500:
            self.__http_codes['client'][str(error)]['Body'] = target
        else:
            custom_log(f'Erro "{error}" não pode ser definido!', 'error')
            exit()