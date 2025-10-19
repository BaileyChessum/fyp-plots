#!/usr/bin/env python

import os
import subprocess

print("Running all python scripts in ./scripts")

py_files = []
for root, _, files in os.walk("scripts"):
    for file in files:
        if file.endswith(".py") and not file.startswith('__'):
            py_files.append(os.path.join(root, file))

processes = []
for f in py_files:
    print(f"  - {f}")
    p = subprocess.Popen(["python3", str(f)])
    processes.append((f, p))

print("\nWaiting for scripts to finish\n")

# Wait for all to finish
for script, p in processes:
    p.wait()
    print(f"{script} finished with exit code {p.returncode}")

print()
print("Finished generating .pgf plots in ./plots!")









