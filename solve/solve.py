#!/usr/bin/env python3
"""
solve.py - Automated solver for the encrypted_message CTF challenge.

Two-pass approach:
  Pass 1: brute-force single-byte XOR against every printable string.
  Pass 2: try every candidate string as a multi-byte XOR key and look for
          readable plaintext (>= 60% printable ASCII).
"""
import re
import sys
from pathlib import Path

FLAG_RE = re.compile(rb"flag\{[A-Za-z0-9]+\}")


def printable_ratio(buf: bytes) -> float:
    if not buf:
        return 0.0
    return sum(0x20 <= b <= 0x7E or b in (0x0A, 0x0D, 0x09) for b in buf) / len(buf)


def extract_printable_strings(data: bytes, min_len: int = 4):
    out, current, start = [], b"", 0
    for i, b in enumerate(data):
        if 0x20 <= b <= 0x7E:
            if not current:
                start = i
            current += bytes([b])
        else:
            if len(current) >= min_len:
                out.append((start, current))
            current = b""
    return out


def xor_with_key(buf: bytes, key: bytes) -> bytes:
    return bytes(buf[i] ^ key[i % len(key)] for i in range(len(buf)))


def single_byte_xor_scan(strings):
    print("[+] Pass 1 — single-byte XOR against every string")
    for off, s in strings:
        for key in range(256):
            dec = bytes(b ^ key for b in s)
            if FLAG_RE.search(dec):
                print(f"    [HIT] offset {off}  key=0x{key:02X}  ->  {dec!r}")


def multibyte_xor_scan(strings, candidates):
    print("[+] Pass 2 — try each candidate as multi-byte XOR key")
    for off, s in strings:
        if not (4 <= len(s) <= 32):
            continue
        for koff, k in candidates:
            if k == s or len(k) > len(s) * 2:
                continue
            dec = xor_with_key(s, k)
            if printable_ratio(dec) >= 0.85 and FLAG_RE.search(dec):
                print(f"    [HIT] offset {off}  key@{koff}={k!r}  ->  {dec!r}")


def main():
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <path-to-challenge_binary>")

    path = Path(sys.argv[1])
    if not path.exists():
        sys.exit(f"File not found: {path}")

    data = path.read_bytes()
    print(f"[+] Loaded {len(data)} bytes from {path}")

    strings = extract_printable_strings(data, min_len=4)
    print(f"[+] Extracted {len(strings)} printable strings")

    # Show the interesting short strings — candidates for the secret code
    print("\n[+] Candidate secret-code strings (4-32 chars, alphanumeric):")
    short = [(o, s) for o, s in strings if 4 <= len(s) <= 32 and s.isalnum()]
    for off, s in short:
        print(f"    offset {off:>7}  {s.decode(errors='ignore')}")

    # Try every short string as a XOR key against every other short string
    single_byte_xor_scan(strings)
    multibyte_xor_scan(strings, short)

    # Try single-byte XOR against the encrypted flag prefix specifically
    print("\n[+] Pass 3 — XOR the 'Zflag{' prefix against all 256 single-byte keys")
    idx = data.find(b"Zflag{")
    if idx != -1:
        blob = data[idx:idx + 64]
        for key in range(256):
            dec = bytes(b ^ key for b in blob)
            if printable_ratio(dec) >= 0.9 and b"flag{" in dec:
                print(f"    [HIT] key=0x{key:02X}  ->  {dec[:40]!r}")


if __name__ == "__main__":
    main()