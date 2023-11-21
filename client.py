import ast
import threading
import socket
import json


class Bids_client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 59000))

        self.username = 'username'
        self.status = True

        self.myId = None
        self.myInfo = []
        self.updateInfo = []

    def start_auction(self):
        while True:
            try:
                opt = int(input(
                    "=====================\nPress 1 to 'Register'\nPress 2 to 'Login'\nPress 3 to 'Exit'\nEnter Choose Option: "))  # =====================\n
                if opt == 1:
                    self.register()
                elif opt == 2:
                    self.login()
                elif opt == 3:
                    exit(1)
                else:
                    print(f">>>  Error Msg: Invalid Choose.\n\t Option < {opt} > does not exit.\n\t Please try again! (1 - 3).")
                    self.start_auction()
            except Exception as err:
                print("Start_auction: ", err)

    # register page
    def register(self):
        name = input("Enter 'Your Name' for Registration: ")
        password = input("Enter 'Password' for Registration: ")
        email = input("Enter 'Email' for Registration: ")
        phone = input("Enter 'Phone' for Registration: ")
        show_money = "0"

        send_data = "register" + "~" + name + "~" + password + "~" + email + "~" + phone + "~" + show_money
        self.client.send(send_data.encode('utf-8'))
        recv_data = self.client.recv(1024).decode('utf-8')
        print(recv_data)

    def login(self):
        email = input("Enter 'Email' for Login: ")
        password = input("Enter 'Password' for Login: ")
        send_data = "login" + "~" + email + "~" + password
        self.client.send(send_data.encode('utf-8'))
        recv_data = self.client.recv(1024).decode('utf-8')
        recv_data = ast.literal_eval(recv_data)
        if recv_data[0]:
            self.myInfo = recv_data[1]
            self.myId = recv_data[2]
            self.hello_boss()
        else:
            print(f">>> Login Error Msg: {recv_data[1]}")

    def hello_boss(self):
        while True:
            try:
                print("===== This is Home Page ===== ")
                print(f"===== Wellcome <<< {self.myInfo['username']} >>> :id < {self.myId} > =====")
                print(f"+++++ Your Show Money: {self.myInfo['show_money']} kyats +++++")
                self.updateInfo = self.myInfo.copy()
                opt = int(input("Press 1 to Create Auction:\nPress 2 to Go to Place Bids:\nPress 3 to Transfer Amount:\n"
                                "Press 4 to Fill Amount:\nPress 5 Show All Auctions Status:\nPress 6 to Show My Auctions and Status:\n"
                                "Press 7 to Logout:\nPress 8 to Exit this app:\nEnter Something: "))
                if opt == 1:
                    self.client.send("Press 1 to Create Auction".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                elif opt == 2:
                    self.client.send("Press 2 to Go to Place Bids".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                elif opt == 3:
                    self.client.send("Press 3 to Transfer Amount".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                elif opt == 4:
                    self.fill_amount()
                elif opt == 5:
                    self.client.send("Press 5 Show All Auctions Status".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                elif opt == 6:
                    self.client.send("Press 6 to Show My Auctions and Status".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                elif opt == 7:
                    self.client.send("exit".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                    print("Server: ", msg)
                    self.myInfo = []
                    self.start_auction()
                elif opt == 8:
                    self.client.send("exit".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                    print("Server: ", msg)
                    exit(1)

            except Exception as err:
                print("hello_boss err: ", err)
                self.hello_boss()

    # hello boss press 4 Fill Amount
    def fill_amount(self):
        try:
            print("===== Fill Amount Page =====")
            amount = int(input("Enter Amount You want to fill: "))
            self.updateInfo["show_money"] += amount
            data = ["fill_amount", {f"{self.myId}": self.myInfo}, {f"{self.myId}": self.updateInfo}]
            self.client.send(f"{data}".encode('utf-8'))
            msg = self.client.recv(1024).decode('utf-8')
            if msg:
                print("Server: ", msg)
                self.myInfo = self.updateInfo
            else:
                print("Update User Not Found!")
        except Exception as err:
            print("fill_amount_err: ", err)
            self.fill_amount()

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
