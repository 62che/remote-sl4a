from tprint import tprint
import android
import socket
from _socket import SHUT_RDWR

class AndroidProxy(android.Android):
    def __init__(self, addr=None):
        android.Android.__init__(self, addr)

    def call(self, request):
        self.conn.sendall(request)
        response = self.conn.recv(10240)
        self.id += 1
        return response

droid = AndroidProxy()

tprint("Handshake is %s" % (android.HANDSHAKE))
tprint("Server host is %s" % (android.HOST))
tprint("Server port is %s" % (android.PORT))

addr = ("", 9999)

serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock.bind(addr)
serverSock.listen(1)

while True:
    tprint("Connection waiting at %s" % (serverSock))
    sock, addr = serverSock.accept()
    tprint("Connection accepted %s" % (sock))

    while True:
        request = sock.recv(10240)
        tprint(request)
        if not request: break
        response = droid.call(request)
        tprint(response)
        sock.sendall(response)

    tprint("close the socket")
    sock.shutdown(SHUT_RDWR)
    sock.close()

serverSock.shutdown(SHUT_RDWR)
serverSock.close()
