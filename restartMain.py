import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--fifo", required = True)
args = parser.parse_args()

with open(args.fifo, "w") as fifo:
    
    fifo.write("1")
    fifo.flush()
    time.sleep(5)
    
    
    
