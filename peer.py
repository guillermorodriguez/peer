
import socket
import threading
import time

"""
    @Author:    Guillermo Rodriguez
    @Created:   2018.11.08
    @Purpose:   Manage client socket communication
"""
class client(threading.Thread):

    """
        @Author:    Guillermo Rodriguez
        @Created:   2018.11.08
        @Purpose:   Client constructor
    """
    def __init__(self, host, port, id):
        threading.Thread.__init__(self)

        self.host = host
        self.port = port
        self.id = id
        self.bytes = 1024

    """
        @Author:    Guillermo Rodriguez
        @Created:   2018.11.08
        @Purpose:   Main class thread
    """
    def run(self):
        print("Client Session Started ....")

        _client = socket.socket()
        _client.connect((self.host, self.port))

        print("Commands: Query:[Text] | Quit")
        message = input(">> ")
        while message.lower().strip() != 'quit':
            _client.send(message.encode())
            response = _client.recv(self.bytes).decode()

            print(response)

            message = input(">> ")

        print("Client Session Terminated ....")

"""
    @Author:    Guillermo Rodriguez
    @Created:   2018.11.08
    @Purpose:   Manage server socket communication
"""
class server(threading.Thread):
    """
        @Author:    Guillermo Rodriguez
        @Created:   2018.11.08
        @Purpose:   Server constructor
    """
    def __init__(self, host, port, id):
        threading.Thread.__init__(self)

        self.host = host
        self.port = port
        self.id = id
        self.bytes = 1024

    """
        @Author:    Guillermo Rodriguez
        @Created:   2018.11.08
        @Purpose:   Manage individual socket sessions
    """
    def session(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket:
            _socket.bind((self.host, self.port))
            _socket.listen(5)

            connection, address = _socket.accept()
            with connection:
                print("Session Established ....")
                while True:
                    data = connection.recv(self.bytes)
                    if data:
                        print("Data Received ....")
                        print(data.decode())

                        response = "Processing Command"
                        connection.sendall(str.encode(response))
                    else:
                        break;

                print("Session Terminated ....")

    """
        @Author:    Guillermo Rodriguez
        @Created:   2018.11.08
        @Purpose:   Main class thread
    """
    def run(self):
        print("Starting Server ....")

        while True:
            self.session()

        print("Server Instance Terminated ....")


if __name__ == "__main__":
    print("Starting Peer ....")

    # Start Server Instance
    server('127.0.0.1', 9000, 1).start()

    # Start Client Instance
    client('127.0.0.1', 9000, 1).start()

    print("Server Invoked ....")
