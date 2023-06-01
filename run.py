from dataclasses import dataclass, field
from datetime import datetime
import psutil
from statistics import mean
from time import sleep
import argparse
from os import path

@dataclass
class ServerResources:
    
    ts: datetime = datetime.now()
    cpu_usage : list[float] = field(default_factory=list)
    mem_usage_percent: float = 0
    mem_usage_swap : float = 0

    def total_cpu(self) -> float:
        return mean(self.cpu_usage)
    

parser = argparse.ArgumentParser(description='Simple Python Script for cpu and memory usage logging')

parser.add_argument("-n", help="Interval in seconds", default=2, required=False)

parser.add_argument("-t", help="Time period to run in hours", default=False, required=False)

parser.add_argument("-f", help="File name", default='log.txt', required=False)

parser.add_argument("-sep", help="Separator", default=';', required=False)

parser.add_argument("-i", help="Number of iterations if not given run only once", default=1, required=False)

args = parser.parse_args()

header_c = True

iter = int(args.i)

if args.t :

    iter = int(int(args.t)*60*60 / int(args.n))


print(f'N of interations {iter}')

for i in range(iter):

    x = ServerResources(
        cpu_usage = psutil.cpu_percent(0.5,percpu=True),
        mem_usage_percent = psutil.virtual_memory().percent,
        mem_usage_swap = psutil.swap_memory().percent,
    )

    if path.exists(args.f) :

        header_c = False
    

    with open(args.f,'a+') as f:


        if header_c :
            header = f"ts{args.sep}{f'{args.sep}'.join(str(f'cpu_{num}') for num,x in enumerate(x.cpu_usage))}{args.sep}cpu_total{args.sep}mem_per{args.sep}swap{args.sep}\n"
            f.write(header)
        
        
        data = f'{x.ts.isoformat()}{args.sep}{f"{args.sep}".join(str(x) for x in x.cpu_usage)}{args.sep}{x.total_cpu():.4f}{args.sep}{x.mem_usage_percent:.4f}{args.sep}{x.mem_usage_swap:.4f}\n'
        f.write(data)

    sleep(int(args.n))

