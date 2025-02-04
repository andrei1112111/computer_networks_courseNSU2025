import os
import subprocess
import re

import pandas as pd


df = pd.read_csv("hostnames.csv")


for i in df.index:
    if os.system(f"ping -c 1 {df.at[i, 'hostname']}") != 0:
        df.at[i, "ping_status"] = 'err'
        df.at[i, "time"] = '-1'
    else:
        df.at[i, "ping_status"] = 'ok'

        output = subprocess.check_output(f"ping -c 1 {df.at[i, 'hostname']}", shell=True)
        df.at[i, "time"] = re.findall(r"time\S+", str(output))[0][5:]


df.to_csv("hostnames.csv", index=False)
