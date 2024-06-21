import os

filename = "../logs/log1.txt"

print(os.popen(f"java Client {filename}").read())