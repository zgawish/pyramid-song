import socket
import threading

class SocketServer:
    HEADER = 1024
    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname()) # 192.168.86.23
    ADDR = (SERVER, PORT)
    FORMAT = 'utf-8'
    DISCONNECT_MSG = "!DISCONNECT"
    REQUEST_MSG = "!REQUEST"
    RECENT = {}

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)

        self.new_data = False # indicator of new data
        self.num_conns = 0  # number of connections


    def handle_client(self, conn, addr):
        print("[NEW CONNECTIONS] " + str(addr[0]) + " connected.")

        connected = True
        while connected:
            msg_length = conn.recv(self.HEADER).decode(self.FORMAT) # recieve size of message then actual string
            if msg_length: # if theres a msg
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(self.FORMAT)
                if msg == self.DISCONNECT_MSG:
                    connected = False
                
                elif msg == self.REQUEST_MSG:
                    conn.send(("SENDING WORK OVER").encode(self.FORMAT))
                else:    
                    print(str(addr[0]) + ": " + msg)
                    conn.send("Msg recieved".encode(self.FORMAT))
        conn.close()


    def start_server(self):
        self.server.listen()
        print("[LISTENING] Server is listening on " + self.SERVER)
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()
            print("[ACTIVE CONNECTIONS] " + str(threading.activeCount() - 1))


def main():
    server = SocketServer()
    server.start_server()

if __name__ == "__main__":
    main()