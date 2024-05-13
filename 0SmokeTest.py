#Common python convetion for running a main function.

from socket import IP_DEFAULT_MULTICAST_LOOP


def main():

    print("hello world")
#guard the main function call with an if statement. 
# __name is the name of the file in the context of how the name is envoked.
#reason, you don't want to run the main function when importing.
# for example you might not want it to run the whole thing, just a piece.
if __name__ == "__main__":
    main()

