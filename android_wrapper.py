from tprint import tprint
import sys

tprint("Current platform is %s." % (sys.platform))

if sys.platform.startswith('linux-armv'):
    tprint("This device is android")
    from android import Android
else:
    tprint("This device is not android")

    import collections
    import json
    import socket

    PORT = 9999
    HOST = "127.0.0.1"
    Result = collections.namedtuple('Result', 'id,result,error')

    class Android(object):
        def __init__(self, addr=None):
            if addr is None:
                addr = HOST, PORT
            tprint("connect to addr: ", addr)
            self.conn = socket.create_connection(addr)
            tprint("create file pointer: ", self.conn)
            self.client = self.conn.makefile(mode='rw', encoding='utf-8')
            tprint("created file pointer: ", self.client)
            self.id = 0

        def _rpc(self, method, *args):
            data = {'id': self.id, 'method': method, 'params': args }
            request = json.dumps(data)
            self.client.write(request + '\n')
            self.client.flush()
            response = self.client.readline()
            self.id += 1
            result = json.loads(response)
            if result['error'] is not None:
                tprint(result['error'])
            # namedtuple doesn't work with unicode keys.
            return Result(id=result['id'], result=result['result'], error=result['error'],)

        def __getattr__(self, name):
            def rpc_call(*args):
                return self._rpc(name, *args)
            return rpc_call
