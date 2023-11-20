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
        # self.aliases: list = []

        # files
        self.users_txt = "users.txt"
        self.bids_txt = "bids.txt"
        self.auctions_txt = "auctions.txt"

        # file data
        self.all_user = []

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
                # client.send(f"Data recv: {data}\n{addr}".encode('utf-8'))

                goTo = data[0]
                if goTo == "register":
                    self.register(client, goTo, data)

            except:
                self.clients.remove(client)
                client.close()
                print(f'{addr} has disconnected form this app.!')
                break

    def register(self, client, log, data):
        user_found = self.check_user(log, data)
        if not user_found:
            # print("check", user_found)
            add_user = self.writeFile(self.users_txt, data)
            self.readFile(self.users_txt)
            client.send(f">>> {add_user}: {data[1]}".encode('utf-8'))
        else:
            client.send(f">>> Error Msg for Register: {user_found}".encode('utf-8'))

    def check_user(self, log, data):
        exits = None
        if log == "register":
            # print("check_user: ", data)
            for i in range(len(self.all_user)):
                check_name = self.all_user[i][f'{i}']['username']
                check_email = self.all_user[i][f'{i}']['email']
                # print(check_name, data[1])
                # print(check_email, data[3])
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
            # print("exits: ", exits)
            return exits

    # read file
    def readFile(self, filename):
        self.all_user = []
        with open(filename, "r") as file:
            for line in file.readlines():
                user = json.loads(line.strip())
                self.all_user.append(user)

    # write file
    def writeFile(self, filename, data):
        self.readFile(filename)
        with open(filename, "r") as rfile:
            with open(filename, "a") as file:
                ids = list(json.loads(rfile.readlines()[-1]).keys())
                data = {"username": data[1], "password": data[2], "email": data[3], "phone": data[4], "show_money": int(data[5])}
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
