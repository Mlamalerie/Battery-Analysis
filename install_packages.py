import os
import sys
import subprocess
os.system("python -m pip install --upgrade pip")

commandinstall = "pip install "

listes = ['pandas','psutil','time','datetime','psutil','plyer']

for mod in listes:
    if mod not in sys.modules:
        os.system(commandinstall + mod)
    else:
        print(mod + " est installe ouiii")
