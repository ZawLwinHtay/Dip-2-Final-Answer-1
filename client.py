import ast
import threading
import socket
import json
import re
from colorama import Fore
from datetime import datetime
import time


class Bids_client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 59000))

        # handle my info
        self.myId = None
        self.myInfo = []
        self.updateInfo = []

        # color
        self.red = Fore.RED
        self.green = Fore.GREEN
        self.blue = Fore.BLUE
        self.white = Fore.WHITE

    def start_auction(self):
        while True:
            try:
                opt = int(input(self.blue +
                                "\n=====================\nPress 1 to 'Register'\nPress 2 to 'Login'\nPress 3 to 'Exit'\nEnter Choose Option: "))
                if opt == 1:
                    self.register()
                elif opt == 2:
                    email = input(self.blue + "Enter 'Email' for Login: ")
                    password = input(self.blue + "Enter 'Password' for Login: ")
                    self.login(email, password)
                elif opt == 3:
                    exit(1)
                else:
                    print(
                        self.red + f">>>  Error Msg: Invalid Choose.\n\t Option < {opt} > does not exit.\n\t Please try again! (1 - 3).")
                    self.start_auction()
            except Exception as err:
                print(self.red + "Start_auction Error Msg: ", err)

    # register page
    def register(self):
        while True:
            name = input(self.blue + "\nEnter 'Your Name' for Registration: ")
            if name:
                break

        while True:
            password = input(self.blue + "Enter 'Password' for Registration: ")
            if password:
                break

        while True:
            email = input(self.blue + "Enter 'Email' for Registration: ")
            if email:
                if self.email_validation(email):
                    break
                else:
                    print(self.red + "===== Invalid email address. =====")

        while True:
            phone = input(self.blue + "Enter 'Phone' for Registration: ")
            if phone:
                try:
                    phone = int(phone)
                    break
                except ValueError:
                    print(self.red + "===== Invalid Phone Input, Try again. =====")

        show_money = "0"
        send_data = ("register" + "~" + name + "~" + password + "~" + email + "~" +
                     "0" + str(phone) + "~" + show_money)
        self.client.send(send_data.encode('utf-8'))
        recv_data = self.client.recv(1024).decode('utf-8')
        if recv_data == "1":
            print(self.green + "===== Registration Success =====")
            print(self.green + "===== Thank you so much for using this app. =====")
        else:
            print(self.red + recv_data)

        # while True:
        #     name = input(self.blue + "\nEnter 'Your Name' for Registration: ")
        #     if name:
        #         password = input(self.blue + "Enter 'Password' for Registration: ")
        #         if password:
        #             email = input(self.blue + "Enter 'Email' for Registration: ")
        #             if email:
        #                 if self.email_validation(email):
        #                     phone = int(input(self.blue + "Enter 'Phone' for Registration: "))
        #                     if phone:
        #                         show_money = "0"
        #                         send_data = "register" + "~" + name + "~" + password + "~" + email + "~" + "0" + str(
        #                             phone) + "~" + show_money
        #                         self.client.send(send_data.encode('utf-8'))
        #                         recv_data = self.client.recv(1024).decode('utf-8')
        #                         if recv_data == "1":
        #                             print(self.green + "===== Registration Success =====")
        #                             print(self.green + "===== Thank you so much for using this app. =====")
        #                         else:
        #                             print(self.red + recv_data)
        #                         break
        #                 else:
        #                     print(self.red + "===== Invalid email address. =====")

    def email_validation(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        match = re.match(pattern, email)
        return bool(match)

    # login page
    def login(self, email, password):
        send_data = "login" + "~" + email + "~" + password
        self.client.send(send_data.encode('utf-8'))
        recv_data = self.client.recv(1024).decode('utf-8')
        recv_data = ast.literal_eval(recv_data)
        if recv_data[0]:
            self.myInfo = recv_data[1]
            self.myId = recv_data[2]
            self.hello_boss()
        else:
            print(self.red + f">>> Login Error Msg: Email or Password is not found. Please, Try again!!!")

    def logout(self):
        self.client.send("exit".encode('utf-8'))
        msg = self.client.recv(1024).decode('utf-8')
        print(self.white + "Server: ", msg)

    def hello_boss(self):
        while True:
            try:
                print(self.blue + "\n===== This is Home Page ===== ")
                print(self.blue + f"===== Wellcome <<< {self.myInfo['username']} >>> :id < {self.myId} > =====")
                print(self.green + f"+++++ Your Show Money: {self.myInfo['show_money']} kyats +++++")
                self.updateInfo = self.myInfo.copy()
                opt = int(
                    input(
                        self.blue + "Press 0 to Show My Info: \nPress 1 to Create Auction:\nPress 2 to Go to Place Bids:\nPress 3 to Transfer Amount:\n"
                                    "Press 4 to Fill Amount:\nPress 5 to Show All Auctions Status:\nPress 6 to Show My Auctions and Status:\n"
                                    "Press 7 to Logout:\nPress 8 to Refresh:\nPress 9 to Exit this app:\nEnter Something: "))
                if opt == 0:  # Done
                    self.show_my_info_and_edit()
                elif opt == 1:
                    self.create_auction()
                elif opt == 2:
                    self.client.send("Press 2 to Go to Place Bids".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                elif opt == 3:  # Done transfer amount
                    self.transfer_amount()
                elif opt == 4:  # Done Fill Amount
                    self.fill_amount()
                elif opt == 5:
                    self.client.send("Press 5 Show All Auctions Status".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                elif opt == 6:
                    self.client.send("Press 6 to Show My Auctions and Status".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                elif opt == 7:  # Done Logout
                    self.logout()
                    self.myInfo = []
                    self.start_auction()
                elif opt == 8:  # Done Refresh
                    self.logout()
                    self.login(self.myInfo['email'], self.myInfo['password'])
                elif opt == 9:  # Done Exit
                    self.client.send("exit".encode('utf-8'))
                    msg = self.client.recv(1024).decode('utf-8')
                    print(self.white + "Server: ", msg)
                    exit(1)

            except Exception as err:
                print(self.red + "hello_boss err: ", err)
                self.hello_boss()

    def create_auction(self):
        print(self.blue + "===== This is Auction Create Page =====")
        title = input(self.blue + "Enter Title for Auction: ")
        description = input(self.blue + "Enter Description for Auction: ")

        # auction end_time
        while True:
            try:
                end_date = input("Enter Auction End Date ( YYYY/M/D H:M:S ) : ")
                end_date = datetime.strptime(end_date, "%Y/%m/%d %H:%M:%S")
                break
            except ValueError:
                print("Error Msg: Incorrect End Date Format!")

        # reserve_price
        while True:
            reserve_price = input("Enter Reserve Price for Auction: ")
            try:
                reserve_price = int(reserve_price)
                break
            except ValueError:
                print("Error Msg: Invalid Reserve Price Input!")

        old_owner = None
        current_owner = self.myInfo['username']
        highest_bidder = []
        highest_bid = 0
        sale = False
        owner_id = self.myId

        send_data = ["create_auction", title, description, str(end_date), reserve_price, old_owner,
                     current_owner, highest_bidder, highest_bid, sale, owner_id]
        self.client.send(f"{send_data}".encode('utf-8'))

        recv_data = self.client.recv(1024).decode('utf-8')
        recv_data = int(recv_data)
        if recv_data:
            print(self.green + "Success! New Auction Created!!")
        else:
            print(self.red + "Error Msg: Fail! Auction Create, try again!!")

    def show_my_info_and_edit(self):
        try:
            print(self.blue + f"\n===== My Info =====\n"
                              f"Name: {self.myInfo['username']}\n"
                              f"Email: {self.myInfo['email']}\n"
                              f"Phone: {self.myInfo['phone']}\n"
                              f"My Amount: {self.myInfo['show_money']} kyats")

            opt = int(input(self.blue + "\nPress 1 to Edit My Info:\nPress 2 to Back:\nEnter Something Option: "))
            if opt == 1:
                print(self.white + "===== Press (Enter) you don't want to edit: =====")
                new_name = input(self.blue + f"Enter new name: current( {self.myInfo['username']} ): ")
                new_email = input(self.blue + f"Enter new email: current( {self.myInfo['email']} ): ")
                new_phone = input(self.blue + f"Enter new phone: current( {self.myInfo['phone']} ): ")
                new_password = input(self.blue + f"Enter new password: current( {self.myInfo['password']} ): ")

                if new_name:
                    self.updateInfo["username"] = new_name
                    print(self.green + f"Success! Change name ( {self.myInfo['username']} ) to ( {new_name} ).")
                if new_email:
                    if self.email_validation(new_email):
                        self.updateInfo["email"] = new_email
                        print(self.green + f"Success! Change email ( {self.myInfo['email']} ) to ( {new_email} ).")
                    else:
                        print(self.red + "===== Invalid email address. =====")
                if new_phone:
                    try:
                        new_phone = int(new_phone)
                        self.updateInfo["phone"] = f"0{new_phone}"
                        print(self.green + f"Success! Change phone {self.myInfo['phone']} to ( {new_phone} ).")
                    except ValueError:
                        print(self.red + "===== Invalid phone number. =====")
                if new_password:
                    self.updateInfo["password"] = new_password
                    print(self.green + f"Success! Change password ( {self.myInfo['password']} ) to ( {new_password} ).")
            elif opt == 2:
                self.logout()
                self.login(self.myInfo['email'], self.myInfo['password'])

            # check exist user or not
            send_data = None
            if (not new_name and not new_email) or not new_name or not new_email:
                send_data = ["update_info", None, None]
            else:
                send_data = ["update_info", self.updateInfo['email'], self.updateInfo['username']]
            self.client.send(f"{send_data}".encode('utf-8'))
            recv_data = self.client.recv(1024).decode('utf-8')
            recv_data = ast.literal_eval(recv_data)
            if recv_data[0]:
                print(self.red + f"Update Info Err Msg: {recv_data[1]}")
            else:
                data = [self.myId, {f"{self.myId}": self.updateInfo}]
                self.client.send(f"{data}".encode('utf-8'))
                self.myInfo = self.updateInfo

        except Exception as err:
            print(self.red + "edit_my_info Err: ", err)
            self.show_my_info_and_edit()

    def transfer_amount(self):
        try:
            print(self.green + f"+++++ Your current amount: {self.myInfo['show_money']} kyats +++++")
            other_username = input(self.blue + "Enter 'UserName' for you want to transfer: ")
            if other_username != self.myInfo["username"]:
                other_userphone = input(self.blue + "Enter 'Phone' for you want to transfer: ")
                data = ["transfer_amount", other_username, other_userphone]
                self.client.send(f"{data}".encode('utf-8'))
                msg = self.client.recv(1024).decode('utf-8')
                msg = ast.literal_eval(msg)  # msg = [ status 0 or 1, other user info dict]
                status = [0]
                if msg[0]:
                    print(self.blue + "\n===== Active User =====")
                    amount = int(input(self.blue + "Enter you want to transfer amount: "))
                    if amount <= self.myInfo["show_money"] != 0:
                        other_user = msg[1]
                        other_user_id = None
                        other_username = None
                        for k, v in other_user.items():
                            other_user_id = int(k)
                            v["show_money"] += amount
                            other_username = v["username"]
                        self.myInfo['show_money'] -= amount
                        status = [1, other_user_id, other_user, self.myId, {f"{self.myId}": self.myInfo}]
                        print(self.green + f"===== Success! < {amount} > kyats transfer to < {other_username} > =====")
                    else:
                        print(self.red + ">>> Transfer Err Msg: Not enough money for transfer")
                        print(self.red + "                      Please,after fill amount transfer again.")
                        # self.hello_boss()
                else:
                    print(self.red + ">>> Error Msg: Not Found User. Please Check Username or Phone!!!")

                self.client.send(f"{status}".encode('utf-8'))
            else:
                print(self.red + f">>> Error Msg: < {other_username} > is you. Don't transfer yourself.")
                self.transfer_amount()

        except Exception as err:
            print(self.red + "transfer_amount err msg: ", err)

    # hello boss press 4 Fill Amount
    def fill_amount(self):
        try:
            print(self.blue + "\n===== Fill Amount Page =====")
            print(self.green + f"===== Your Current Amount : {self.myInfo['show_money']} kyats =====")
            amount = int(input(self.blue + "Enter Amount You want to fill: "))
            self.updateInfo["show_money"] += amount
            data = ["fill_amount", self.myId, {f"{self.myId}": self.updateInfo}]
            self.client.send(f"{data}".encode('utf-8'))
            self.myInfo = self.updateInfo
            print(self.green + "===== Amount Fill Success =====")
        except Exception as err:
            print(self.red + "fill_amount_err: ", err)
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
