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

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle_client(self, client, addr):
        while True:
            try:
                message = client.recv(1024)
                data = message.decode('utf-8').split('~')

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
            add_user = self.writeFile(self.users_txt, data)
            self.readFile(self.users_txt)
            client.send(f">>> {add_user}: {data[1]}".encode('utf-8'))
        else:
            client.send(f">>> Error Msg for Register: {user_found}".encode('utf-8'))

    def login(self, client, log, data):
        user_found = self.check_user(log, data)
        print("login user found: ", user_found)
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
                                update = self.update_user_data(msg[1], msg[2])
                                client.send(f"{update}".encode('utf-8'))
                        except Exception as err:
                            print("This is error", err)
                            continue
                else:
                    break

    def update_user_data(self, oldData: dict, newData: dict):
        exist = 0
        for i in range(len(self.all_user)):
            if self.all_user[i] == oldData:
                self.all_user[i] = newData
                exist = 1
                break
        # over wirte (update user data)
        with open(self.users_txt, 'w') as file:
            for user in self.all_user:
                file.write(f"{json.dumps(user)}\n")
        self.readFile(self.users_txt)
        return exist

    def check_user(self, log, data):
        exits = None
        if log == "register":
            for i in range(len(self.all_user)):
                check_name = self.all_user[i][f'{i}']['username']
                check_email = self.all_user[i][f'{i}']['email']
                if check_name == data[1] and check_email == data[3]:
                    exits = "username and email are already exits, Please, Try again with other different username and email!"
                    break
                elif check_name == data[1]:
                    exits = "This user is already exits, Please, Try again with other different username!"
                    break
                elif check_email == data[3]:
                    exits = "This email is already exits, Please, Try again with other different email!"
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
                    print(user)
                    break
                else:
                    user = [0, "Email or Password is not found. Please, Try again!!!"]
            return user

    # read file
    def readFile(self, filename):
        self.all_user = []
        with open(filename, "r") as file:
            for line in file.readlines():
                line = line.strip()
                user = json.loads(line)
                self.all_user.append(user)

    # write file
    def writeFile(self, filename, data):
        self.readFile(filename)
        with open(filename, "r") as rfile:
            with open(filename, "a") as file:
                ids = list(json.loads(rfile.readlines()[-1]).keys())
                data = {"username": data[1], "password": data[2], "email": data[3], "phone": data[4], "show_money": int(data[5]), "my_auctions": []}
                data = {int(ids[0]) + 1: data}
                print(data)
                file.write(json.dumps(data) + "\n")
                return "Registration is Successful!!!"

    def receive(self):
        while True:

            print('Server is running and listening ...')
            client, address = self.server.accept()
            print(f'connection is established with {str(address)}')
            self.clients.append(client)
            print(f'{address[1]} has connected to this app.')

            # loading all user acc
            self.readFile(self.users_txt)

            thread = threading.Thread(target=self.handle_client, args=(client, address[1]))
            thread.start()


if __name__ == "__main__":
    bids_server = Bids_server()
    bids_server.receive()
