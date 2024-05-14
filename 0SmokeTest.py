#Common python convetion for running a main function.

import socket


def main():
    HOST = "0.0.0.0"
    PORT = 65432
    #creates a socket that supports context manager type. 
    #AF_INET internet adress for IPv4 expects two-tuple (host,port)
    #SOCK_STREAM socket type for TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
        #.bind() method assosciates specific network interface and port number
        s.bind((HOST,PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    print(data)
                    if not data:
                        break

                    conn.sendall(data)

    
#guard the main function call with an if statement. 
# __name is the name of the file in the context of how the name is envoked.
#reason, you don't want to run the main function when importing.
# for example you might not want it to run the whole thing, just a piece.
if __name__ == "__main__":
    main()

