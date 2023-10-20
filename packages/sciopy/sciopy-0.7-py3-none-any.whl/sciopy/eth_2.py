import socket

TCP_IP = "139.30.207.32"
TCP_PORT = 5000

# MESSAGE = b"\xbe\x01\x01\xbe"
MESSAGE = b"\xd2\x00\xd2"

MESSAGE = b"\xd1\x00\xd1"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
client.connect((TCP_IP, TCP_PORT))
client.sendall(MESSAGE)

start_tag = client.recv(1)
print(f"{start_tag=}")
msg_len = client.recv(1)[0]
print(f"{msg_len=}")
data = client.recv(int(msg_len))
print([ele for ele in data])
end_tag = client.recv(1)
sys_ackn = client.recv(4)

print(f"{end_tag=}\n{sys_ackn=}\n")

client.close()
