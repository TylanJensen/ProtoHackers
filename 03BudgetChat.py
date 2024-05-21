import socket
from threading import Thread

def runChat(conn: socket.socket,addr):
    with conn:
        file = conn.makefile() # using .makefile allows to take all the data sent by client.
        print(f"Connected by {addr}")
        while True:
            return
            


                

def main():
    HOST = "0.0.0.0"
    PORT = 65432
    #creates a socket that supports context manager type. 
    #AF_INET internet adress for IPv4 expects two-tuple (host,port)
    #SOCK_STREAM socket type for TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        #.bind() method assosciates specific network interface and port number
        #s.setsockopt allows me to close and open on the same port rapidly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen()
        historicalPD = {}
        while True:
            conn, addr = s.accept()
            thread = Thread(target = runChat, args = (conn,addr))

            thread.start()
                    
if __name__ == "__main__":
    main()