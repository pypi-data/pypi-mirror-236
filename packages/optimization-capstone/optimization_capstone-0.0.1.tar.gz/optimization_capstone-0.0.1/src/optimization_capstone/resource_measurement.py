import psutil
import time
from datetime import timedelta

def start() -> float:
    return time.time()

def end() -> float:
    return time.time()

def measure(start: float, end: float=time.time(), format: bool=False) -> tuple:
    elapsed_time = end - start
    formatted_time = str(timedelta(seconds=elapsed_time))[:-3]

    clock_speed = 0
    try:
        cpu_info = psutil.cpu_freq()
        if cpu_info is not None:
            clock_speed = cpu_info.current
    except Exception as e:
        print(str(e))
    estimated_cycles = round(clock_speed * 1_000_000_000 * elapsed_time)
    formatted_cycles = f"{estimated_cycles:,}" 
    
    if format:
        return formatted_time, formatted_cycles
    return elapsed_time, estimated_cycles