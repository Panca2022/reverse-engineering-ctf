# Reverse Engineering CTF - Technical Report

**Author:** Sri Hari Aravindan 

**Stack:** C, Linux ELF x86-64, Docker, Python 3, WSL

**Repository:** github.com/Panca2022/reverse-engineering-ctf

## Abstract

This is a reverse engineering CTF challenge built as a 64-bit Linux ELF
binary. The player must identify the binary, extract its symbols and
strings, disassemble main, and decode a hard-coded secret code. Submitting
the correct code reveals a dynamically generated flag that changes on
every run.

## Objectives

- Identify an unknown binary with file.
- Extract symbols and strings without disassembling first.
- Read x86-64 assembly with objdump.
- Demonstrate that XOR and compiler string inlining are not security.

## How It Works

The binary prompts for a license key. It compares the input against a
secret code stored on the stack. If they match, it generates a random
20-character string, wraps it in flag{...}, and prints it.

Two functions do the work:
- xor_encrypt() - XORs a buffer in place
- generate_random() - fills a buffer with random characters

Both names are visible because the binary is not stripped.

## Solve Method

Step 1. Identify the binary.
    file challenge_binary
    -> ELF 64-bit, x86-64, not stripped

Step 2. Extract strings.
    tr -c '[:print:]' '\n' < challenge_binary | grep -iE "flag|secret"
    -> finds "Zflag{", "Enter License Key:", "Access Denied!"

Step 3. Read the symbol table.
    readelf -s challenge_binary | grep -E "xor_key|main|xor_encrypt"
    -> exposes xor_encrypt, xor_key, generate_random, charset

Step 4. Disassemble main.
    objdump -d -M intel challenge_binary > disasm.txt
    sed -n '/<main>:/,/^$/p' disasm.txt

Step 5. Read the assembly. Two movabs instructions load the secret code:

    127d: movabs rax, 0x50324b4d38465443
    1287: mov    QWORD PTR [rbp-0x8f], rax
    128e: movabs rax, 0x00585a5639514c50
    1298: mov    QWORD PTR [rbp-0x88], rax

Decode little-endian:
    0x50324b4d38465443 -> "CTF8MK2P"
    0x00585a5639514c50 -> "PLQ9VZX\0"

The second store overlaps the first by one byte, so the P is written
twice. Final string: CTF8MK2PLQ9VZX

Step 6. Verify.
    echo "CTF8MK2PLQ9VZX" | ./challenge_binary
    -> Hey! You found the flag: flag{9yMpiaicoY14BgBMA6ax}

## Why the XOR Obfuscation Fails

main calls xor_encrypt twice on the same buffer. XOR is its own inverse:
(X XOR K) XOR K = X. The double call is a no-op. The obfuscation does
nothing.

## Flag Generation

After strcmp succeeds, main:
1. Seeds srand with time(NULL)
2. Generates 20 random characters
3. Prepends flag{ and appends }
4. Prints the result

Every run produces a different flag.

## Design Decisions

Not stripped: focuses the challenge on logic, not symbol recovery.

XOR instead of AES: AES would be unsolvable without the key. XOR gives
a clean teaching moment.

Docker: reproducible execution across distros.

Dynamic flag: prevents sharing; each player must solve independently.

Regex flag format: flag{[A-Za-z0-9]{20}} - allows automated verification.

## Security Lessons

1. Strip production binaries. Symbols leak function names and structure.
2. XOR is not encryption. Double XOR is a no-op.
3. Compiler optimisations leak data. Short strings become immediate
   movabs instructions, readable from disassembly.
4. Obfuscation raises cost; it does not provide confidentiality.

## Tools Used

file               Identify binary type
tr + grep          Extract printable strings
readelf -s         Dump symbol table
objdump -d         Disassemble
sed                Extract function blocks
WSL Ubuntu         Run Linux binaries on Windows
Docker             Reproducible execution


## Summary

A reverse engineering CTF built as a 64-bit Linux ELF binary. The
binary is not stripped, so the symbol table exposes the entire
architecture. Disassembling main reveals the secret code
CTF8MK2PLQ9VZX stored as immediate values on the stack. A double XOR
is a no-op - a deliberate lesson that obfuscation is not encryption.
The flag is regenerated per run using srand(time(NULL)).

## Limitations

- Single-byte XOR is trivially broken.
- Unstripped binary lowers difficulty.
- Docker adds setup friction.

## Future Work

- Add ptrace anti-debugging.
- Use a multi-byte runtime key.
- Ship a stripped hard-mode variant.
- Add a server-side flag check.

## Glossary

ELF             Linux binary format
Stripped        Symbol table removed
.rodata         Read-only data section
movabs          64-bit immediate move instruction
Little-endian   Least-significant byte first
XOR             Bitwise exclusive-or; its own inverse
CTF             Capture The Flag
strcmp          C function comparing strings
ptrace          Linux syscall used for anti-debugging
