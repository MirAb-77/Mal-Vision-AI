import os
import zipfile

os.makedirs("benign", exist_ok=True)
os.makedirs("mal_like", exist_ok=True)

# ---------------------------
# 🟢 BENIGN (REALISTIC SOFTWARE-LIKE)
# ---------------------------
benign = [
"""
import json

def load_config():
    return {"mode": "safe", "version": 1.0}

def process_data(x):
    return x * 2

def main():
    cfg = load_config()
    for i in range(5):
        print("Processing:", process_data(i))

if __name__ == "__main__":
    main()
""",

"""
import logging

logging.basicConfig(level=logging.INFO)

def task_runner():
    for i in range(3):
        logging.info(f"Task {i} completed")

task_runner()
input()
""",

"""
import os

def list_files():
    files = os.listdir(".")
    for f in files:
        print("File:", f)

list_files()
input()
""",

"""
class Calculator:
    def add(self, a, b):
        return a + b

    def run(self):
        for i in range(3):
            print(self.add(i, i+1))

c = Calculator()
c.run()
input()
""",

"""
import time

def workflow():
    for i in range(5):
        time.sleep(0.1)
        print("Step:", i)

workflow()
input()
"""
]

# ---------------------------
# 🔴 MALWARE-LIKE (SAFE SYNTHETIC COMPLEXITY)
# ---------------------------
mal_like = [
"""
def alpha(x):
    return (x ^ 91) + (x * 3)

def beta(y):
    return alpha(y) ^ (y << 1)

def gamma():
    for i in range(20):
        if beta(i) % 2 == 0:
            print("signal_", beta(i))

gamma()
input()
""",

"""
def chain_a(x): return x * 7
def chain_b(x): return chain_a(x) ^ 33
def chain_c(x): return chain_b(x) + 19

for i in range(25):
    val = chain_c(i)
    if val % 3 == 0:
        print("event_flow", val)

input()
""",

"""
def dispatcher():
    data = [i for i in range(40)]
    out = []

    for d in data:
        if d % 2 == 0:
            out.append(d ^ 55)
        else:
            out.append(d * 3)

    for o in out:
        print("trace", o)

dispatcher()
input()
""",

"""
import math

def calc_entropy_like(x):
    return math.sqrt(x * 999) + (x ^ 77)

for i in range(30):
    print(calc_entropy_like(i))

input()
""",

"""
def router(x):
    if x % 5 == 0:
        return x ^ 12
    elif x % 3 == 0:
        return x * 9
    else:
        return (x << 2) ^ 21

for i in range(35):
    print("route", router(i))

input()
"""
]

# ---------------------------
# BUILD EXEs
# ---------------------------
def build(folder, code_list, prefix):
    exe_paths = []

    for i, code in enumerate(code_list):
        py_path = f"{folder}/{prefix}_{i}.py"

        with open(py_path, "w") as f:
            f.write(code)

        os.system(f"pyinstaller --onefile --noconsole {py_path}")

        exe_paths.append(f"dist/{prefix}_{i}.exe")

    return exe_paths


print("Building benign...")
benign_exe = build("benign", benign, "b")

print("Building mal-like...")
mal_exe = build("mal_like", mal_like, "m")

# ---------------------------
# ZIP OUTPUT
# ---------------------------
zip_name = "high_quality_pe_dataset.zip"

with zipfile.ZipFile(zip_name, "w") as z:
    for f in benign_exe:
        if os.path.exists(f):
            z.write(f, "benign/" + os.path.basename(f))

    for f in mal_exe:
        if os.path.exists(f):
            z.write(f, "mal_like/" + os.path.basename(f))

print("DONE ->", zip_name)