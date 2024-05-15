import socket
import json
from math import sqrt
from threading import Thread

def threadedFunction(conn,addr):
    with conn:
        print(f"Connected by {addr}")
        while True:
            while True:
                data = conn.recv(1024)
                print(data)
                dataDic = json.loads(data)
                if dataDic["method"] == "isPrime" and type(dataDic["number"]) == int :
                    print("You did it")
                    n = dataDic["number"]
                    primeBool = 1
                    if (n > 1):
                        for i in range (2, int(sqrt(n)) + 1):
                            if(n % i == 0):
                                primeBool = 0
                                break
                        if(primeBool == 1):
                            print("Prime")
                            returnData = {"method":"isPrime","prime":bool(primeBool)}
                            
                            
                            conn.sendall(bytes(json.dumps(returnData), 'utf-8'))
                        else:
                            print("Not Prime")
                            returnData = {"method":"isPrime","prime":bool(primeBool)}
                            conn.sendall(bytes(json.dumps(returnData), 'utf-8'))
                                        
                else:
                    print("Failure")
                    conn.sendall(data)
                    break

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
        while True:
            conn, addr = s.accept()
            thread = Thread(target = threadedFunction, args = (conn,addr))
            thread.start()
            thread.join()                    

if __name__ == "__main__":
    main()