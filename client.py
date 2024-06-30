import socket
import pickle
import cv2
import numpy
from PIL import Image
from constants import BUFFER, PORT


class Client:
    def __init__(self, dest_ip: str, dest_port: int) -> None:
        self.__dest_ip = dest_ip
        self.__dest_port = dest_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self) -> None:
        self.__socket.connect((self.__dest_ip, self.__dest_port))
        message = ""
        length = 0
        while True:
            message = ""
            try:
                while True:
                    message_part = self.__socket.recv(1)
                    message += message_part.decode()
            except UnicodeDecodeError:
                length = int(message)
                message = message_part
           
            while len(message) < length:
               message_part = self.__socket.recv(min(BUFFER, length - len(message))) #
               message += message_part 
            image = pickle.loads(message)
            self.__show_frame(image)
    
    def __show_frame(self, image: Image) -> None:
        cv2_image = numpy.array(image)[:, :, ::-1].copy()
        cv2.imshow('frame', cv2_image)
        cv2.waitKey(1) 
        

if __name__ == "__main__":
    dest_ip = input("Enter ip:\n")
    try:
        Client(dest_ip, PORT).connect()
    except ConnectionRefusedError:
        input("Server unavailable\n")
    except socket.gaierror:
        input("Incorrect ip format\n")