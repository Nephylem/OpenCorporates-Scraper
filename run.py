import os, time
import numpy as np

import appv2
import config
from appv2 import initialize_browser, search, save_output

from concurrent.futures import ThreadPoolExecutor



MAX_WORKERS = len(config.proxies)

def open_terms_file(filename):
    terms = []
    with open(os.path.join(appv2.BASE_PATH, filename), "r") as file:
        for term in file.read().split("\n"):
            terms.append(term)
        file.close()
    return terms



counter1 = time.perf_counter()
if __name__ == '__main__':

    drivers = [initialize_browser(**config.proxies[proxy]) for proxy in config.proxies]
    terms = open_terms_file('terms.txt')
    split_terms = np.array_split(terms, MAX_WORKERS)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as exec:
        for result in exec.map(search, drivers, split_terms):
            save_output(result)

    
    [driver.close() for driver in drivers]
            
counter2 = time.perf_counter()

print(f"Finished in {counter2 - counter1} seconds")