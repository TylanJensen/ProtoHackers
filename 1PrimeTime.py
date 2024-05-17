import socket
import json
from math import sqrt
from threading import Thread


def is_prime(num: int) -> bool:
    if (num > 1):
        for i in range (2, int(sqrt(num)) + 1):
            if(num % i == 0):
                return False
    return True

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
                #guard clause to check if submission contains needed keys
                if dataDic["method"] != "isPrime" or type(dataDic["number"]) != int :
                    print("Failure")
                    conn.sendall(data)
                    break
                #guard clause to check if submission contains valid values
                if dataDic["method"] != "isPrime" or type(dataDic["number"]) != int :
                    print("Failure")
                    conn.sendall(data)
                    break
                if dataDic.get('method') is None or dataDic.get('number')is None:
                    print("Failure")
                    conn.sendall(data)
                    break
                #guard clause to check if number is 1, 0 or negative.
                if dataDic["number"] <= 1:
                    print("Number less than 1")
                    returnData = {"method":"isPrime","prime":False}
                    print(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'utf-8'))
                    conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
                    break
                #Checks if number is prime is true then sends results to client
                primeBool = is_prime(dataDic["number"])
                if(primeBool == True):
                    print("Prime")
                    returnData = {"method":"isPrime","prime":primeBool}
                    print(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'utf-8'))
                    conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
                else:
                    print("Not Prime")
                    returnData = {"method":"isPrime","prime":primeBool}
                    print(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'utf-8'))
                    conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
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
            print("Starting", thread.name)
                    
if __name__ == "__main__":
    main()