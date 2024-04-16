import socket
import threading
from colorama import Fore
from .templateHandler import parse_template
HOST, PORT = '127.0.0.1', 5000


class Serve:

    def __init__(self) -> None:
        self.routes: dict = {}
        self.lis_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lis_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self, debug=True, host=HOST, port=PORT):
        if debug:
            print(f"This is a Development server")
            print(f"{Fore.RED}Please Don't use this in Production {Fore.WHITE} ")
            print(f"Server is starting at http://{host}:{port}")

        self.lis_socket.bind((host, port))
        self.lis_socket.listen(5)
        try:
            while True:
                connection, address = self.lis_socket.accept()
                thread = threading.Thread(
                    target=self.handle_request, args=(connection, address))
                thread.start()
        except KeyboardInterrupt:
            print("server is closing")
            self.lis_socket.close()
            print("server is closed")
            return

    def handle_request(self, connection, address):
        data = connection.recv(8190)
        decode_data = data.decode()
        method, path = self.parse_request(decode_data)
        print(f"{method} // {path} from {address}")

        handler = self.routes.get((method, path), None)
        if handler:
            response_data = handler()
            connection.sendall(response_data.encode())
            print(
                f"{Fore.CYAN} {method}/{path} successfully responce with 200 to {address} {Fore.WHITE}")
        else:
            response_data = self.render_temp('404.html', status_code=404)
            print(
                f"{Fore.RED} {method} // {path} Invalid responce with 404 to {address} {Fore.WHITE}")
            connection.sendall(response_data.encode())
        connection.close()

    def parse_request(self, request):
        lines = request.split('\n')
        start_line = lines[0].split()
        if start_line[1] == None:
            return self.render_temp('400.html', status_code=404)
        method = start_line[0].upper()
        path = start_line[1]
        return method, path

    def route(self, path, methods=['GET']):
        def decorator(func):
            self.routes[(methods[0].upper(), path)] = func
            return func
        return decorator

    def response(self, res, status_code=200):
        return f"""\
HTTP/1.0 {status_code}
Content-Type: application/json

{res}
"""

    def render_temp(self, path, status_code=200, *args):
        data, statuscode = parse_template(path=path, status_code=status_code)
        if 'error' in data:
            print(f"{path} is not valid")
            res = "<h1>NO FILE FOUND </h1>"
            return f"""\
HTTP/1.0 500 Internal Server Error
Content-Type: text/html

{res}
"""

        return f"""\
HTTP/1.0 {statuscode}
Content-Type: text/html

{data}
"""
