import ast
import json
import threading
import socket

class Bids_server:
    def __init__(self):
        host = '127.0.0.1'
        port = 59000
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients: list = []
        self.bids: list = []

        # files
        self.users_txt = "users.txt"
        self.bids_txt = "bids.txt"
        self.auctions_txt = "auctions.txt"

        # file data
        self.all_user = []
        self.all_auctions = []

    def broadcast(self, message):
        # print(self.clients)
        for client in self.clients:
            client.send(message)
            # print("done")

    def handle_client(self, client, addr):
        while True:
            try:
                message = client.recv(1024)
                data = message.decode('utf-8').split('~')
                # print(data)

                goTo = data[0]
                if goTo == "register":
                    self.register(client, goTo, data)
                elif goTo == "login":
                    self.login(client, goTo, data)

            except:
                self.clients.remove(client)
                client.close()
                print(f'{addr} has disconnected form this app!')
                break

    def register(self, client, log, data):
        user_found = self.check_user(log, data)
        if not user_found:
            # print("check", user_found)
            reg_data = {"username": data[1], "password": data[2], "email": data[3], "phone": data[4],
                    "show_money": int(data[5])}
            self.readFile()
            add_user = self.writeFile(self.users_txt, reg_data)
            self.readFile()
            client.send(f"{add_user}".encode('utf-8'))  # send 1 for register success
        else:
            client.send(user_found.encode('utf-8'))  # send 0 for register fail

    def login(self, client, log, data):
        user_found = self.check_user(log, data)
        # print("login user found: ", user_found)
        # print(user_found)
        client.send(f"{user_found}".encode('utf-8'))
        if user_found[0]:
            while True:
                msg = client.recv(1024).decode('utf-8')
                if msg:
                    if msg == "exit":
                        client.send("See You Again!".encode('utf-8'))
                        break
                    else:
                        try:
                            msg = ast.literal_eval(msg)
                            if msg[0] == "fill_amount":
                                self.update_user_data(msg[1], msg[2])
                            elif msg[0] == "transfer_amount":
                                self.check_user_and_transfer_amount(client, msg[1], msg[2])
                            elif msg[0] == "update_info":
                                found_user = self.check_user(msg[0], msg)
                                client.send(f"{found_user}".encode('utf-8'))
                                if not found_user[0]:
                                    recv_data = client.recv(1024).decode('utf-8')
                                    recv_data = ast.literal_eval(recv_data)
                                    self.update_user_data(recv_data[0], recv_data[1])
                            elif msg[0] == "create_auction":
                                create_auction_data = {"title": msg[1], "description": msg[2], "end_date": msg[3], "reserve_price": msg[4], "old_owner": msg[5],
                                                       "current_owner": msg[6], "highest_bidder": msg[7], "highest_bid": msg[8], "sale": msg[9], "owner_id": msg[10]}
                                add_auction = self.writeFile(self.auctions_txt, create_auction_data)
                                client.send(str(add_auction).encode('utf-8'))
                            elif msg[0] == "show_my_auctions":
                                my_auctions = []
                                for i in range(len(self.all_auctions)):
                                    for k, v in self.all_auctions[i].items():
                                        if v['owner_id'] == int(msg[1]):
                                            my_auctions.append(self.all_auctions[i])
                                client.send(str(my_auctions).encode('utf-8'))
                            else:
                                print("Received ( while not working others ): ", msg)
                        except Exception as err:
                            print("This is error: ", err)
                            continue
                else:
                    break

    def check_user_and_transfer_amount(self, client, username, phone):
        data = None
        for i in range(len(self.all_user)):
            if self.all_user[i][f"{i}"]["username"] == username and self.all_user[i][f"{i}"]["phone"] == phone:
                # print(self.all_user[i])
                data = [1, self.all_user[i]]
                break
            else:
                data = [0]
        client.send(f"{data}".encode('utf-8'))
        msg = client.recv(1024).decode('utf-8')
        msg = ast.literal_eval(msg)
        if msg[0]:
            # update other user data
            self.update_user_data(msg[1], msg[2])

            # update my data
            self.update_user_data(msg[3], msg[4])


        else:
            print(f"Received {msg[0]}")


    def update_user_data(self, ids, newData: dict):
        self.all_user[ids] = newData
        self.update_users_txt()

    def check_user(self, log, data):
        exits = None
        if log == "register":
            for i in range(len(self.all_user)):
                check_name = self.all_user[i][f'{i}']['username']
                check_email = self.all_user[i][f'{i}']['email']
                if check_name == data[1] and check_email == data[3]:
                    exits = "username and email are already exits. Please, Try again with other different username and email!"
                    break
                elif check_name == data[1]:
                    exits = "This user is already exits. Please, Try again with other different username!"
                    break
                elif check_email == data[3]:
                    exits = "This email is already exits. Please, Try again with other different email!"
                    break
                else:
                    exits = 0
            return exits
        elif log == "login":
            user = None
            for i in range(len(self.all_user)):
                check_email = self.all_user[i][f'{i}']['email']
                check_pass = self.all_user[i][f'{i}']['password']
                if check_email == data[1] and check_pass == data[2]:
                    user = [1, self.all_user[i][f'{i}'], i]
                    break
                else:
                    user = [0]
            return user
        elif log == "update_info":
            exist = None
            for i in range(len(self.all_user)):
                check_email = self.all_user[i][f'{i}']['email']
                check_name = self.all_user[i][f'{i}']['username']
                if check_email == data[1] and check_name == data[2]:
                    exist = [1, "username and email are already exits. Please, Try again with other different username and email!"]
                    break
                elif check_email == data[1]:
                    exist = [1, "This email is already exits. Please, Try again with other different email!"]
                    break
                elif check_name == data[2]:
                    exist = [1, "This user is already exits. Please, Try again with other different username!"]
                    break
                else:
                    exist = [0]
            return exist

    # read file
    def readFile(self):
        self.all_user = []
        with open(self.users_txt, "r") as file:
            for line in file.readlines():
                line = line.strip()
                user = json.loads(line)
                self.all_user.append(user)

        self.all_auctions = []
        with open(self.auctions_txt, "r") as file:
            for line in file.readlines():
                line = line.strip()
                auction = json.loads(line)
                self.all_auctions.append(auction)

    # write file
    def writeFile(self, filename, data):
        # self.readFile(filename)
        with open(filename, "r") as rfile:
            # print(data)
            with open(filename, "a") as file:
                try:
                    ids = list(json.loads(rfile.readlines()[-1]).keys())
                    # print(ids)
                except Exception as err:
                    ids = [-1]
                data = {int(ids[0]) + 1: data}
                # print(data)
                file.write(json.dumps(data) + "\n")
                return 1

    def update_users_txt(self):
        # overwrite (update user data)
        with open(self.users_txt, 'w') as file:
            for user in self.all_user:
                file.write(f"{json.dumps(user)}\n")
        self.readFile()

    def receive(self):
        while True:

            print('Server is running and listening ...')
            client, address = self.server.accept()
            print(f'connection is established with {str(address)}')
            self.clients.append(client)
            print(f'{address[1]} has connected to this app.')

            # loading all user acc
            self.readFile()

            thread = threading.Thread(target=self.handle_client, args=(client, address[1]))
            thread.start()


if __name__ == "__main__":
    bids_server = Bids_server()
    bids_server.receive()
