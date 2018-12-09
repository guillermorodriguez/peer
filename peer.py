
import socket
import threading
import time


"""
    @Author:    Guillermo Rodriguez
    @Created:   2018.11.08
    @Purpose:   Manage server socket communication
"""
class server(threading.Thread):
    """
        @Author:    Guillermo Rodriguez
        @Created:   2018.11.08
        @Purpose:   Constructor
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

                        #connection.sendall(data)
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

    server('127.0.0.1', 9000, 1).start()
    print("Server Invoked ....")
