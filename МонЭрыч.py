import os
import subprocess
import json

wallet_address = input("Enter your Monero wallet address: ")
print("Please choose a pool from the following options:")
print("1. pool.minexmr.com:4444")
print("2. xmrpool.eu:9999")
print("3. monerohash.com:5555")
print("4. pool.supportxmr.com:5555")
pool_choice = input("Enter the number of the pool you want to mine on: ")
power_percent = input("Enter the percentage of mining power you want to use (0-100): ")

try:
    power_percent = int(power_percent)
except ValueError:
    print("Invalid input for mining power. Please enter an integer between 0 and 100.")
    exit()

if power_percent < 0 or power_percent > 100:
    print("Invalid input for mining power. Please enter an integer between 0 and 100.")
    exit()

if pool_choice == "1":
    pool_address = "pool.minexmr.com:4444"
elif pool_choice == "2":
    pool_address = "xmrpool.eu:9999"
elif pool_choice == "3":
    pool_address = "monerohash.com:5555"
elif pool_choice == "4":
    pool_address = "pool.supportxmr.com:5555"
else:
    print("Invalid input for pool choice. Please enter a number between 1 and 4.")
    exit()

xmrig_path = input("Enter the path to the XMRig executable file (e.g. C:/xmrig/xmrig.exe): ")

# Configure XMRig automatically based on user inputs
config_path = os.path.join(os.getcwd(), "config.json")

config = {
    "pools": [
        {
            "url": f"stratum+tcp://{pool_address}",
            "user": f"{wallet_address}",
            "pass": "x"
        }
    ],
    "cpu": {
        "enabled": True,
        "threads": 0,
        "priority": 5
    },
    "opencl": False,
    "cuda": False,
    "donate-level": 0,
    "log-file": "log.txt",
    "print-time": 60,
    "retry-pause": 5,
    "syslog": False,
    "threads": [
        {
            "index": 0,
            "mode": "auto",
            "intensity": power_percent
        }
    ]
}

with open(config_path, "w") as f:
    f.write(json.dumps(config))

command = f"{xmrig_path} -c {config_path}"

# Run XMRig
process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# Open the pool website
pool_website = f"https://{pool_address.split(':')[0]}/"
os.system(f"start {pool_website}")

# Monitor output from XMRig
while True:
    output = process.stdout.readline().decode("utf-8").strip()
    if output == "":
        break
    print(output)
