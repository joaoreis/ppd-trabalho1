from contextlib import contextmanager
from multiprocessing import Manager, Pool
import time

class Timer(object):
    def __init__(self, *steps):
        self._time_per_step = dict.fromkeys(steps)

    def __getitem__(self, item):
        return self.time_per_step[item]

    @property
    def time_per_step(self):
        return {
            step: elapsed_time
            for step, elapsed_time in self._time_per_step.items()
            if elapsed_time is not None and elapsed_time > 0
        }

    def start_for(self, step):
        self._time_per_step[step] = -time.time()

    def stop_for(self, step):
        self._time_per_step[step] += time.time()


###############################################################################
@contextmanager
def process_pool(size):
    # Cria um pool de processos e bloqueia ate que todos os processos sejam concluidos
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()


###############################################################################
def searchInSubArray(element, array, result):
    result.append(element in array)


###############################################################################
def parallel_search(element, array, process_count):
    timer = Timer('total_time')
    timer.start_for('total_time')

    step = int(len(array)/process_count)
    manager = Manager()
    results = manager.list()
    with process_pool(process_count) as pool:
        for n in range(process_count):
            if n < process_count - 1:
                chunk = array[n * step:(n + 1) * step]
            else:
                chunk = array[n * step:]
        pool.apply_async(searchInSubArray, (element, chunk, results))
    
    timer.stop_for('total_time')
    return timer, results