from client import MyClient
token = open("token.txt", "r").read().strip()
name = 797850288543367199

if __name__ == '__main__':
    client = MyClient(name)
    client.run(token)