import socket
import json
from math import sqrt
from threading import Thread


def is_prime(num: int) -> bool:
    return False

def threadedFunction(conn: socket.socket,addr):
    with conn:
        file = conn.makefile()
        print(f"Connected by {addr}")
        while True:
            while True:
                data = file.readline()
                print(data)
                dataDic = json.loads(data)

                #guard clause for checking if malformed
                if dataDic.get('method') is None or dataDic.get('number') is None:
                    print("Failure")
                    conn.sendall(data)
                    break
                #guard clause to check if submission contains needed fields
                if dataDic["method"] != "isPrime" or type(dataDic["number"]) != int :
                    print("Failure")
                    conn.sendall(data)
                    break
                
                prime = is_prime(dataDic["number"])
                returnData = {"method":"isPrime","prime":prime}
                conn.sendall(returnData)

                if dataDic.get('method') is not None and dataDic.get('number')is not None:
                    if dataDic["method"] == "isPrime" and type(dataDic["number"]) == int :
                        n = dataDic["number"]
                        primeBool = 0
                        if (n > 1):
                            for i in range (2, int(sqrt(n)) + 1):
                                if(n % i == 0):
                                    primeBool = 1
                                    break
                            if(primeBool == 0):
                                print("Prime")
                                returnData = {"method":"isPrime","prime":True}
                                print(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'utf-8'))
                                conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
                            else:
                                print("Not Prime")
                                returnData = {"method":"isPrime","prime":False}
                                print(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'utf-8'))
                                conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
                                break
                        else:
                            print("Negative or something")
                            returnData = {"method":"isPrime","prime":False}
                            print(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'utf-8'))
                            conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
                            break
                    else:
                        print("Failure")
                        conn.sendall(data)
                        break
                else:
                    print("Failure")
                    conn.sendall(data)
                    break
                #return                  


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
            print("Starting", thread.name)
                    

if __name__ == "__main__":
    main()