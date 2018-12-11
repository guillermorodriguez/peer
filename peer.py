
import socket
import threading
import time
import argparse
import os

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
    def __init__(self, id):
        threading.Thread.__init__(self)

        self.host = '127.0.0.1'
        self.port = 9000
        self.id = id
        self.bytes = 1024

        self.nodes = []
        with open(str(self.id) + ".txt", 'r') as _file:
            for line in _file:
                self.nodes.append(int(line.rstrip('\n')))

        self.log = str(self.id) + "/log/log.log"

    """
        @Author:    Guillermo Rodriguez
        @Created:   2018.11.08
        @Purpose:   Main class thread
    """
    def run(self):
        print("Client Session Started ....")

        print("Commands: Query:[Text] | Quit")
        message = input(">> ")
        while message.lower().strip() != 'quit':

            if "query" in message.lower():
                for node in self.nodes:

                    _mode = 'w'
                    if os.path.exists(self.log):
                        _mode = 'a'

                    _logit = open(self.log, _mode)
                    _logit.write(message + '\n')
                    _logit.close()

                    _client = socket.socket()
                    _client.connect((self.host, self.port+node))
                    _client.send(message.lower().encode())
                    response = _client.recv(self.bytes).decode()

                    _client.close()

                    if "FILE:" in response:
                        response = response.replace('FILE:', '')
                        with open(str(self.id) + "/" + message.lower().replace('query:', ''), 'w') as _target:
                            _target.write(response)

                    _logit = open(self.log, _mode)
                    _logit.write(response + '\n')
                    _logit.close()

            message = input(">> ")

        print("Client Session Terminated ....")
        exit()

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
    def __init__(self, id):
        threading.Thread.__init__(self)

        self.host = '127.0.0.1'
        self.port = 9000+id
        self.id = id
        self.bytes = 1024

        self.nodes = []
        with open(str(self.id) + ".txt", 'r') as _file:
            for line in _file:
                self.nodes.append(int(line.rstrip('\n')))

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
                        query = data.decode().replace('query:', '')
                        print("Searching File .... %s" % query)

                        content = ''
                        for _file in os.listdir(str(self.id)+"/"):
                            if _file == query:
                                print("File Found")
                                with open(str(self.id)+"/"+_file, 'r') as _target:
                                    content = _target.read()
                                break

                        if len(content) > 0:
                            connection.sendall(str.encode("FILE:"+content))
                        else:
                            # Route to Peers
                            for node in self.nodes:
                                _client = socket.socket()
                                _client.connect((self.host, self.port+node))
                                _client.send(message.lower().encode())
                                content = _client.recv(self.bytes).decode()

                                _client.close()

                                if len(content) > 0:
                                    break

                            if len(content) > 0:
                                connection.sendall(str.encode("FILE:"+content))
                            else:
                                connection.sendall(str.encode("NOTFOUND"))


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

    parser = argparse.ArgumentParser(prog='peer.py')
    parser.add_argument('-id', help='Client ID Number')
    parse = parser.parse_args()

    if parse.id:
        print("Starting Peer ....")

        # Start Server Instance
        server(int(parse.id)).start()

        # Start Client Instance
        client(int(parse.id)).start()

        print("Server Invoked ....")
    else:
        parser.print_help()
