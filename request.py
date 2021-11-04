from http_parser.pyparser import HttpParser

class Request:
    def process_http_message(self, message):
        hp = HttpParser()
        hp.execute(message, len(message))

        request_info = {
            'path': hp.get_path(),
            'method': hp.get_method(),
            'headers': hp.get_headers(),
            'params': hp.get_query_string(),
            'body': hp.recv_body()
        }

        return request_info