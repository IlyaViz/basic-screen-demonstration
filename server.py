import socket
import pickle
from PIL import ImageGrab, Image
from constants import PORT


class Server:
    def __init__(self, port: int) -> None:
        self.__port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def start(self) -> None:
        self.__socket.bind(('', self.__port))
        self.__socket.listen(1)    
        conn, addr = self.__socket.accept()
        while True:
            dumped_image = pickle.dumps(self.__get_next_image())
            conn.send(str(len(dumped_image)).encode())
            conn.send(dumped_image)
            
    def __get_next_image(self) -> Image:
        frame = ImageGrab.grab()
        return frame


if __name__ == "__main__":
    Server(PORT).start()