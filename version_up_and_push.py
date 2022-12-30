import re
import subprocess

with open('setup.py', 'r') as f:
    setup_py = f.read()
ver_number = re.findall(r"version\='(.*)'", setup_py)[0]
new_ver_number = str(float(ver_number)+0.0001)
setup_py = setup_py.replace(str(ver_number), new_ver_number)
with open('setup.py', 'w') as f:
    f.write(setup_py)
subprocess.call(f'.\commit_and_push.bat {new_ver_number}')