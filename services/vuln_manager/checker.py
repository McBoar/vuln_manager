#!/usr/bin/env python3

import random
import re
import string
import sys
import socket
import telnetlib
import os
import inspect

# DEBUG -- logs to stderr
DEBUG = os.getenv("DEBUG", True)

OK, CORRUPT, MUMBLE, DOWN, CHECKER_ERROR = 101, 102, 103, 104, 110
SERVICENAME = "market"
PORT = 10081 #fixed


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


def close(code, public="", private=""):
    if public:
        print(public)
    if private:
        print(private, file=sys.stderr)
    print("Exit with code {}".format(code), file=sys.stderr)
    exit(code)


def put(*args): #fixed
    team_addr, flag_id, flag = args[:3]
    tn = WaryTelnet(team_addr, PORT, timeout=10)
    username, password = generate_rand(16), generate_rand(16)
    name = generate_rand(16)
    try:
        _log(f"Try register with username: {username}, passwd: {password}")
        if not register(tn, username, password):
            close(MUMBLE)
        _log(f"Try auth with username: {username}, passwd: {password}")
        if not authorize(tn, username, password):
            close(MUMBLE)
        
        _log(f"Try create file with name: {name} and content: {flag}")
        create_file(tn, name, flag)

        # Exit gracefully.
        _log(f"Try exit")
        tn.write(b"exit\n")
        tn.write(b"\n")
        new_flag_id = username + ":" + password + ":" + name
        print(new_flag_id, flush=True)
        close(OK, private = new_flag_id)
    except Exception as e:
        close(MUMBLE, private=f"Excepction {e}")


def error_arg(*args):
    close(CHECKER_ERROR, private="Wrong command {}".format(sys.argv[1]))


def init(*args):
    close(OK, "vulns: 1")


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
        close(MUMBLE, private=f"Excepction {e}")


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
        close(MUMBLE, private=f"Excepction {e}")


def sft(tn): #fixed
    try:
        tn.write(b"sft\n")
        tn.expect([b"]"], 5)
        return True
    except Exception as e:
        close(MUMBLE, private=f"Excepction {e}")


def sut(tn): #fixed
    try:
        tn.write(b"sut\n")
        tn.expect([b"]"], 5)
        return True
    except Exception as e:
        close(MUMBLE, private=f"Excepction {e}")


def create_file(tn, name, flag): #fixed
    try:
        tn.write(b"\n")
        tn.expect([b"Enter your request"], 5)
        tn.write(b"create " + name.encode() + b"\n")
        tn.expect([b"Enter a text for the file"], 5)
        tn.write(flag.encode() + b"\n")
        tn.expect([b"DONE"], 5)

    except Exception as e:
        close(MUMBLE, private=f"Excepction {e}")


def check(*args): #fixed
    team_addr = args[0]
    tn = WaryTelnet(team_addr, PORT, timeout=10)
    username = generate_rand(16)
    password = generate_rand(16)
    name, content= (
        generate_rand(16),
        generate_rand(16),
    )
    try:
        _log(f"Try register with username: {username}, passwd: {password}")
        if not register(tn, username, password):
            close(MUMBLE)
        _log(f"Try auth with username: {username}, passwd: {password}")
        if not authorize(tn, username, password):
            close(MUMBLE)
        _log(f"Try sft")
        if not sft(tn):
            close(MUMBLE)
        _log(f"Try sut")
        if not sut(tn):
            close(MUMBLE)
            
        _log(f"Try create file with name: {name} and content: {content}")
        create_file(tn, name, content)
        
        _log(f"Check is file: {name} in sft")
        tn.write(b"sft\n")
        tn.expect([name.encode()], 5)

        _log(f"Try get content")
        tn.write(b"read " + name.encode() + b"\n")
        try:
            tn.expect([content.encode()], 5)
        except Exception as e:
            close(CORRUPT, private=f"Excepction {e}")
        close(OK)

    except Exception as e:
        close(MUMBLE, private=f"Excepction {e}")


def get(*args): #fixed
    team_addr, flag_id, flag = args[:3]
    try:
        username, password, name = flag_id.split(sep=":")
    except:
        close(
            CHECKER_ERROR,
            f"Unexpected flagID from jury: {flag_id}! Are u using non-RuCTF checksystem?",
        )
    tn = WaryTelnet(team_addr, PORT, timeout=10)
    try:
        _log(f"Try register with username: {username}, passwd: {password}")
        if not register(tn, username, password):
            close(MUMBLE)
        _log(f"Try auth with username: {username}, passwd: {password}")
        if not authorize(tn, username, password):
            close(MUMBLE)
        _log(f"Try find content: {flag} in file: {name}")
        tn.write(b"sft\n")
        tn.expect([name.encode()], 5)
        tn.write(b"read " + name.encode() + b"\n")
        tn.expect([flag.encode()], 5)
        close(OK)

    except Exception as e:
        close(CORRUPT, private=f"Excepction {e}")


def info(*args): #Kate
    print('{"vulns": 1, "timeout": 30, "attack_data": ""}', flush=True, end="")
    # print("vulns : 1", flush=True, end="")
    exit(101)


def _log(msg):
    if DEBUG:
        caller = inspect.stack()[1].function
        print(f"func {caller}, msg: {msg} ", file=sys.stderr)
    return


COMMANDS = {"put": put, "check": check, "get": get, "info": info, "init": init}


if __name__ == "__main__":
    try:
        COMMANDS.get(sys.argv[1], error_arg)(*sys.argv[2:])
    except socket.error as ex:
        close(DOWN, public=f"Connection error: {ex}")
    except Exception as ex:
        close(CHECKER_ERROR, private="INTERNAL ERROR: {}".format(ex))
