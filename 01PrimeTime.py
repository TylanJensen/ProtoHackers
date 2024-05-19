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

def valid_json(data):
    try:
        json.loads(data)
    except Exception as e:
        print("Error", e)
        return False
    return True



def threadedFunction(conn: socket.socket,addr):
    with conn:
        file = conn.makefile() # using .makefile allows to take all the data sent by client.
        print(f"Connected by {addr}")

        while True:
            data = file.readline() #readline() will take all the data up to \n and run it.
            print(data)
            #guard clause to make sure JSON is valid
            validCheck = valid_json(data)
            if validCheck != True:
                conn.sendall(bytes(data, encoding="ascii"))
                return

            dataDic = json.loads(data)
            #guard clause to see if string is empty
            if dataDic == None or dataDic == '':
                print("I'm empty")
                return
            #guard clause for checking if malformed
            if dataDic.get("method") is None or dataDic.get("number") is None:
                print("Failure 1")
                print(dataDic)
                conn.sendall(bytes(data,'ascii'))
                return
            #guard clause to check if submission contains valid values
            if dataDic["method"] != "isPrime" or type(dataDic["number"]) not in [int, float]:
                print("Failure 2")
                print(dataDic)
                conn.sendall(bytes(data,'ascii'))
                return
            #guard clause to check if number is 1, 0 or negative.
            if dataDic["number"] <= 1 or type(dataDic["number"]) == float:
                print("Number less than 1")
                returnData = {"method":"isPrime","prime":False}
                print(dataDic)
                conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
                continue
            #Checks if number is prime is true then sends results to client
            primeBool = is_prime(dataDic["number"])
            if(primeBool == True):
                print("Prime")
                returnData = {"method":"isPrime","prime":primeBool}
                print(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
                conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
            else:
                print("Not Prime")
                returnData = {"method":"isPrime","prime":primeBool}
                print(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'utf-8'))
                conn.sendall(bytes(json.dumps(returnData, separators=(',', ':')) + "\n", 'ascii'))
                continue             

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