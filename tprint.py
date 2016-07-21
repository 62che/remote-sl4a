import time

def tprint(*arg):
    t = time.strftime("%H:%M:%S", time.localtime()) + ("%.3f"%(time.time()%1))[1:]
    print("["+t+"]", *arg)
