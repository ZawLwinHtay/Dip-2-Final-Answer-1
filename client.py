import threading
import socket
import json


class Bids_client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 59000))

        self.username = 'username'
        self.status = True

    def start_auction(self):
        while True:
            try:
                opt = int(input(
                    "=====================\nPress 1 to 'Register'\nPress 2 to 'Login'\nPress 3 to 'Exit'\nEnter Choose Option: "))  # =====================\n
                if opt == 1:
                    self.register()
                elif opt == 2:
                    print('2', opt)
                elif opt == 3:
                    exit(1)
                else:
                    print(f">>>  Error Msg: Invalid Choose.\n\t Option < {opt} > does not exit.\n\t Please try again! (1 - 3).")
                    self.start_auction()
            except Exception as err:
                print("Start_auction: ", err)

    # register page
    def register(self):
        name = input("Enter Your Name for Registration: ")
        password = input("Enter Password for Registration: ")
        email = input("Enter Email for Register: ")
        phone = input("Enter Phone for Register: ")
        show_money = "0"

        # send_data = {"msg": "register", "username": name, "password": password}
        # send_data = {"register": {"username": "Zaw", "password": "Zaw", "email": "Zaws@gmail.com"}}
        send_data = "register" + "~" + name + "~" + password + "~" + email + "~" + phone + "~" + show_money
        self.client.send(send_data.encode('utf-8'))
        recv_data = self.client.recv(1024).decode('utf-8')
        print(recv_data)

    # def client_receive(self):
    #     while True:
    #         try:
    #             message = self.client.recv(1024).decode('utf-8')
    #             # if message == "exit":
    #             #     print("Exit: ", message)
    #             # else:
    #             print(message)
    #         except:
    #             print('Error!')
    #             self.client.close()
    #             break

    # def client_send(self):
    #     while True:
    #         message = f'{input("")}'
    #         self.client.send(message.encode('utf-8'))


if __name__ == "__main__":
    bids_client = Bids_client()
    bids_client.start_auction()
