from Crypto.Util.number import *
import subprocess
import time
from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL)
 
def attack(ssh):
    n_list = []

    flag_found = False

    start = time.time()

    while not flag_found:
        # Send ssh commands to stdin
        ssh.stdin.write('{"msg": "request"}')
        # Fetch output
        for line in ssh.stdout:
            message = line.strip()
            if message == '{"error": "Invalid JSON"}':
                print("Try to reconnect")
                ssh.kill()
                ssh = subprocess.Popen(['nc', 'localhost', '13370'],
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)
                break
            elif (message != 'New Challenge'):
                try:
                    messageArray = line.strip().split('"')[-2].split(",")
                    n=int(messageArray[-3].split(":")[1])
                    e=int(messageArray[-2].split(":")[1])
                    ct = int(messageArray[-1].split(":")[1])
                    print(n,e,ct)
                    ## check if there is a shared factor with the current n that is being used
                    for n_prev in n_list:
                        if GCD(n_prev, n) > 1:
                            p = GCD(n_prev, n)
                            q = n // p
                            #print(p,q, "p and q found")
                            flag_found = True
                    n_list.append(n)
                except:
                    print(message)
            break
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    pt = pow(ct, d, n)
    decrypted = long_to_bytes(pt)
    print(decrypted)
    return time.time()-start
    
total_time = 0
tries = 1
for i in (range(tries)):
    ssh = subprocess.Popen(['nc', 'localhost', '13370'],
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)
    total_time += attack(ssh)
    ssh.kill()
print("Average time taken: " + str(total_time) + "s")

