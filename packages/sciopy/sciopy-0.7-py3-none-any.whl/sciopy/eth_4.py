import socket
import select
import time


UDP_IP = "139.30.207.32"
TCP_IP = "139.30.207.32"

TCP_PORT = 5000
UDP_PORT = 8888

# MESSAGE = bytearray([0xD2, 0x00, 0xD2])
MESSAGE = b"\xd2\x00\xd2"
# MESSAGE = b"\xbe\x01\x01\xbe"

# send preamble: wake device up by one or more broadcasts
client = socket.socket(
    socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP
)  # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#
client.sendto(MESSAGE, ("<broadcast>", UDP_PORT))
time.sleep(0.01)
client.sendto(MESSAGE, ("<broadcast>", UDP_PORT))
time.sleep(0.01)
client.sendto(MESSAGE, ("<broadcast>", UDP_PORT))


# get socket, connect to specified address/port pair
tclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
# caution: may fail
tclient.connect((TCP_IP, TCP_PORT))

print("connection open")

# send some data
tclient.sendall(MESSAGE)

# receive some data with given buffer size (length)
# data = tclient.recv(31)

blub = client.recv(2)
print(f"{blub[1]=}")
data = client.recv(int(blub[1]) - 2)
# while True:
#    readable, writable, exceptional = select.select( inputs, outputs, inputs, 0.1 )
##    print(readable)
#    r=r+1
#    for s in readable:
#        r=0
#        data = s.recv(1)
#        print("!%x"%int(data))
#    if r>100:
#        break

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Internet # UDP
# sock.sendto(MESSAGE, (UDP_IP,UDP_PORT))

client.close()
tclient.close()
