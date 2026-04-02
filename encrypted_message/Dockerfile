FROM kalilinux/kali-rolling

RUN apt-get update && apt-get install -y lib32gcc-s1 && rm -rf /var/lib/apt/lists/*

COPY challenge_binary /challenge/challenge_binary
RUN chmod +x /challenge/challenge_binary

WORKDIR /challenge
ENTRYPOINT ["./challenge_binary"]
