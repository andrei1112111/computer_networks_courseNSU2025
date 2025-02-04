import os
import pandas as pd


df = pd.read_csv("hostnames.csv")


for i in df.index:
    if os.system(f"ping -c 1 {df.at[i, 'hostname']}") != 0:
        df.at[i, "ping_status"] = 'err'
    else:
        df.at[i, "ping_status"] = 'ok'


df.to_csv("hostnames.csv", index=False)
