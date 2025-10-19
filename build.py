#!/usr/bin/env python
""" This file runs every file in ./scripts
"""
import os
import subprocess

print("Running all python scripts in ./scripts")

py_files = []
for root, _, files in os.walk("src/scripts"):
    for file in files:
        if file.endswith(".py") and not file.startswith('__'):
            py_files.append(os.path.join(root, file))

processes = []
for f in py_files:
    module = str(f).removesuffix('.py').replace('/', '.')
    print(f"  - {module}")
    p = subprocess.Popen(["python3", "-m", module])
    processes.append((module, p))

print("\nWaiting for scripts to finish")

# Wait for all to finish
for script, p in processes:
    p.wait()
    print(f"  > {script} finished with exit code {p.returncode}")

print("Finished generating .pgf plots in ./plots!")
print()
print("Now: ")
print("1. Open overleaf at https://www.overleaf.com/project/683813102d4472a9b9234233")
print("2. delete all the /plots folder on overleaf")
print("3. drag and drop ./plots into overleaf")
print("4. recompile in overleaf")
print()
