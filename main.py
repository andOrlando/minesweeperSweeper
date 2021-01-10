from client import MyClient
token = open("token.txt", "r").read()

if __name__ == '__main__':
    client = MyClient()
    client.run(token)