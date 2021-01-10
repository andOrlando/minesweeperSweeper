from client import MyClient
token = open("token.txt", "r").read().strip()

if __name__ == '__main__':
    client = MyClient()
    client.run(token)