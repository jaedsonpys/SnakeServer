# Arquivo principal de inicialização
import socket

from utils.log_server import custom_log
from response import Response
from request import Request
import json


class Snake:
    __ROUTES = {}

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
                self.__send_response()
                pass
            else:
                # Caso a rota não aceita esse método que foi solicitado
                # pelo usuário, retorne um erro 405.
                self.__send_response(405)

        else:
            # Caso a rota solicitada pelo usuário não exista,
            # uma resposta com o erro 404 é enviada. #
            self.__send_response(404)


    def __send_response(self, status=None):
        # Envia a resposta para o usuário

        # Essa condição é especialmente para códigos de status
        # HTTP. #
        if status:
            status = str(status)

            with open('utils/http.codes.json', 'r') as codes_json:
                # As linhas abaixo obtém as informações sobre o código especifico.
                #
                # É necessário para verificar se há uma página de erro
                # personalizada que o usuário deseja mostrar ao erro ser
                # disparado pelo servidor.
                # 
                # Além de conter o Content-Type da resposta a ser enviada,
                # que ajudar na criação de APIs, sendo da escolha do usuário
                # retornar JSON, HTML, e outros tipos.

                http_code_info = json.load(codes_json)['http-codes']['client'][status]
                codes_json.close()

            # Se não houver uma página de erro personalizada 
            # retorne a padrão. #
            if http_code_info['Body'] == '@default-page':
                with open('pages/error.html', 'r') as ep:
                    error_page = str(ep.read())
                    ep.close()

                # Formatando os dados que vão na página
                response = error_page.format(
                    message=http_code_info['Message'], status=status
                )

            # Contruindo a resposta HTTP
            http_response = Response(
                content_type=http_code_info['Content-Type'], status=status,
                response=response
            )

            try:
                self.__client_info[0].send(http_response.http.encode())
            except (ConnectionAbortedError, ConnectionError) as err:
                custom_log('Não foi possível enviar resposta HTTP', 'error')
                self.__client_info[0].close()
                exit()
            else:
                custom_log(f'HTTP {status} {self.__request_info.method} {self.__request_info.path}: {self.__client_info[1]}', 'sucess')
                return


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


        # Tentando enviar a resposta ao usuário
        try:
            if isinstance(function_response, object):
                self.__client_info[0].send(function_response.http.encode())
            else:
                self.__client_info[0].send(function_response.encode())
        except (ConnectionAbortedError, ConnectionError) as err:
            custom_log('Não foi possível enviar resposta HTTP', 'error')
            self.__client_info[0].close()
            exit()
        else:
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
