# Reverse Engineering CTF Challenge

Welcome to the **Encrypted Message** reverse engineering challenge! This challenge tests your skills in **binary analysis**, **reverse engineering**, and understanding **dynamic runtime behavior**.

---

## Challenge Overview

- The goal is to retrieve a **flag** from a binary.
- The flag is in the format:

    flag{<20 random alphanumeric characters>}

- The binary prompts for a **secret code** before revealing the flag.
- Only the correct **secret code** will unlock the dynamic flag.
- The secret code is **hidden in the binary** and not provided in the repository.

---

## Folder Structure

When you clone or download this repository, the relevant files are:


deploy/encrypted_message/

├── challenge_binary # The CTF binary you will analyze

├── Dockerfile # Docker configuration to run the binary safely

└── README.md # This instructions file


**Notes:**

- **challenge_binary** is already compiled and ready to run.
- **Do NOT attempt to find the secret code in the repo** — it is intentionally hidden.
- Source code is **not included** to keep the challenge fair.

---

## Prerequisites

- You need to have **Docker** installed on your system.  
- To check if Docker is installed:
    ```docker --version```
- Running the Challenge
- Build the Docker Image
- Navigate to the folder containing the Dockerfile:
  ```cd deploy/encrypted_message```
- Build the Docker image:
  ```docker build -t encrypted_message_ctf .```
- This creates a Docker image named encrypted_message_ctf.
- Run the Challenge
- Run the container interactively:
  ```docker run --rm -it encrypted_message_ctf```
- You will see:
  ```Enter secret code:```
- The program expects the correct secret code.
- If the code is incorrect, the program exits with:
  ```Access Denied! Wrong code.```
- If the code is correct, the program outputs a flag

Note: The flag changes every run to prevent simple reuse.

## Challenge Hints
- The secret code is inside the binary, not in the repo.
- Use reverse engineering tools like:
  - radare2
  - Ghidra
  - ghidra
- The binary is obfuscated in memory:
  - The secret code and flag are XOR-encrypted at runtime.
  - Strings in the binary do not reveal the code or flag.
  - Consider debugging the binary to trace where it decrypts and checks the secret code.

### Rules
Do not modify the binary — reverse engineer it as-is.
You may use any tools or debuggers to figure out the secret code.
Do not share the secret code with others outside the CTF.
Example Walkthrough (for testers only)
