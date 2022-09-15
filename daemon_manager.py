#!/usr/bin/python3

import argparse
import config
import glob
import importlib.util
import multiprocessing as mp
import re
import socket
import time

SERVER_TYPE = "netcat" #config.secret.server_type
jobs = []


def chal_for_server_type(filename):
    if SERVER_TYPE == "platform":
        if 'platform_' in filename:
            return True
    elif SERVER_TYPE == "netcat":
        if 'platform_' not in filename:
            return True
    else: # development
        return True

    return False


def healthcheck(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('127.0.0.1', int(port)))
        s.recv(1024)
        s.close()
        return True
    except Exception as e:
        print(f"Challenge {port} failed healthcheck: {str(e)}")
        return False


def restart_mod(job, index):
    path = job.name
    job.terminate()
    del jobs[index]

    spec = load_spec(path)
    mod = load_mod(spec)

    run_proc(spec, mod)
    print(f"Restarted {path}")


def load_spec(filename):
    return importlib.util.spec_from_file_location(filename, filename)


def load_mod(spec):
    return importlib.util.module_from_spec(spec)


def load_modules(directory):
    files = glob.glob("{}/*.py".format(directory))
    selected = []
    for f in files:
        if chal_for_server_type(f):
            selected.append(f)

    specs = [load_spec(f) for f in selected]
    mods = [load_mod(spec) for spec in specs]
    return specs, mods


def run_proc(spec, mod):
    p = mp.Process(name=spec.name, target=spec.loader.exec_module, args=(mod,))
    jobs.append(p)
    p.start()


def run_modules(specs, modules):
    for spec, mod in zip(specs, modules):
        run_proc(spec, mod)

    while True:
        time.sleep(10)
        for i, j in enumerate(jobs):
            if "platform" not in j.name:
                port = re.search('(\d+)', j.name)[0]
                if not healthcheck(port):
                    restart_mod(j, i)
    p.join()


def main():
    parser = argparse.ArgumentParser(
        description="{} daemon manager".format("FCS"))#config.ctf_name))
    parser.add_argument("-l", action="store_true",
                        dest="show_list", help="List all daemons")
    parser.add_argument("-a", "--all", dest="run_all",
                        action="store_true", help="Run all daemons")
    parser.add_argument("-d", "--daemon-directory", action="store",
                        help="The directory which contains the daemons", default="daemons")
    parser.add_argument("modules", nargs="*", help="The daemon modules to run")

    args = parser.parse_args()

    specs, modules = load_modules(args.daemon_directory)

    if args.show_list:
        for module in modules:
            print(module.__name__)

    elif args.run_all:
        run_modules(specs, modules)

    else:
        parser.print_help()
        exit(1)


main()
