# 🐚 포너블 (**Pwnable**) *Exploit* 환경 세팅 및 풀이
###### Pwnable environment settings and basic code [ *Written by NullBins* ]

---

## 🐧 **Linux VM** 세팅 (*Based on Intel macOS*)
### > **Linux Server Environment** <
- Distro: ```Ubuntu Linux 26.04 LTS```
- Tools: ```GDB```, ```GDBServer```, ```GEF Plugins```
- Network: ```192.168.10.0/24```

---

## 💻 **macOS 호스트** 포너블 환경 세팅 (*Based on Intel macOS*)
### > **macOS Host Environment** <
- IDE: ```VSCode```
- Terminal: ```iTerm```
- Terminal session control: ```tmux```
- Language: ```Python@3.13``` (*Important!*)
- Library: ```pwntools```
- Network: ```192.168.10.0/24```

## ⚙️ **Pwnable Exploit** *Basic* Codes
### > **Basic Linux ELF Exec Environment** <
- ```pwn_exploit.py```
>```python
>from pwn import *
>
>HOST, PORT = "addr", 1234
>
>exe = ELF("./chall", checksec=False)
>context.binary = exe
>context.log_level = 'debug'
>context.terminal = ["tmux", "splitw", "-h"]
>
>def conn():
>   if args.LOCAL:
>       p = process([exe.path])
>        gdb.attach(p)
>    else:
>        p = remote(HOST, PORT)
>    return p
>
>def main():
>    # === Alias === #
>    p = conn()
>    s = p.send
>    sl = p.sendline
>    sla = p.sendlineafter
>    sa = p.sendafter
>    r = p.recv
>    ru = p.recvuntil
>    rn = p.recvn
>    rl = p.recvline
>    # === Exploit === #
>    log.info("happy pwn!")
>    # =============== #
>    p.interactive()
>
>if __name__ == "__main__":
>    main()
>```

### > **macOS Execution Environment** <
- ```pwn_exploit_vm.py```
>```python
>from pwn import *
>
>VM_HOST, VM_PORT = "192.168.10.135", 22 # My VM Server
>HOST, PORT = "addr", 1234
>cwd = "/root/workbench/PWN/"
>
>exe = ELF("./chall",checksec=False)
>context.binary = exe
>context.log_level = 'debug'
>context.terminal = ["tmux", "splitw", "-h"]
>
>def conn():
>    if args.LOCAL:
>        sh = ssh(host=VM_HOST, port=VM_PORT, user="root", password="password")
>        p = sh.process([f"{cwd}/pwn"], cwd=cwd)
>        gdb.attach(p)
>    else:
>        p = remote(HOST, PORT)
>    return p
>
>def main():
>    # === Alias === #
>    p = conn()
>    s = p.send
>    sl = p.sendline
>    sla = p.sendlineafter
>    sa = p.sendafter
>    r = p.recv
>    ru = p.recvuntil
>    rn = p.recvn
>    rl = p.recvline
>    # === Exploit === #
>    log.info("happy pwn!")
>    # =============== #
>    p.interactive()
>
>if __name__ == "__main__":
>    main()
>```

> ![IMG](./img/modify.png)
> ![IMG](./img/basic_code.png)

- *Run screen*
```vim
python3 pwn_exploit_vm.py LOCAL
```
> ![IMG](./img/run.png)
> ![IMG](./img/basic.png)

## **CTF** 풀이 (*Solve*)
- ```Stack BOF```
> ![IMG](./img/pwn01.png)
- ```Leak Stack Canary```
> ![IMG](./img/pwn02.png)