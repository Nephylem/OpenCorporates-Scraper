import os, time
import numpy as np
from tqdm import tqdm

import appv2
import config
from appv2 import initialize_browser, search, save_output

from concurrent.futures import ThreadPoolExecutor


def open_terms_file(filename):
    terms = []
    with open(os.path.join(appv2.BASE_PATH, filename), "r") as file:
        for term in file.read().split("\n"):
            terms.append(term)
        file.close()
    return terms

if __name__ == '__main__':

    drivers = [initialize_browser(**config.accounts[account]) for account in tqdm(config.accounts, desc='Initializing Driver(s)', unit='Driver')]
       
    MAX_WORKERS = len(drivers)
    print(f'Total driver(s) initialized ==> {MAX_WORKERS}')
    terms = open_terms_file('terms.txt')
    split_terms = np.array_split(terms, MAX_WORKERS)
    
    print(f"Scraping terms with {MAX_WORKERS} workers...")
    counter1 = time.perf_counter()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as exec:
        for result in exec.map(search, drivers, split_terms):
            save_output(result)    
            
    [driver.close() for driver in drivers]

    counter2 = time.perf_counter()
    print(f"Finished scraping in {counter2 - counter1} seconds")