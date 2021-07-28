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
def merge_sort_multiple(results, array):
  results.append(merge_sort(array))


###############################################################################
def merge_multiple(results, array_part_left, array_part_right):
  results.append(merge(array_part_left, array_part_right))


###############################################################################
def merge_sort(array):
    array_length = len(array)

    if array_length <= 1:
        return array

    middle_index = int(array_length / 2)
    left = array[0:middle_index]
    right = array[middle_index:]
    left = merge_sort(left)
    right = merge_sort(right)
    return merge(left, right)


###############################################################################
def merge(left, right):
    sorted_list = []

    # Cria copias para nao alterar os objetos originais
    left = left[:]
    right = right[:]

    while len(left) > 0 or len(right) > 0:
        if len(left) > 0 and len(right) > 0:
            if left[0] <= right[0]:
                sorted_list.append(left.pop(0))
            else:
                sorted_list.append(right.pop(0))
        elif len(left) > 0:
            sorted_list.append(left.pop(0))
        elif len(right) > 0:
            sorted_list.append(right.pop(0))
    return sorted_list


###############################################################################
@contextmanager
def process_pool(size):
    # Cria um pool de processos e bloqueia ate que todos os processos sejam concluidos
    pool = Pool(size)
    yield pool
    pool.close()
    pool.join()


###############################################################################
def parallel_merge_sort(array, process_count):
    timer = Timer('total_time')
    timer.start_for('total_time')

    # Divide a lista em pedacos, de acordo com a quantidade de processos escolhido
    step = int(len(array) / process_count)

    manager = Manager()
    results = manager.list()

    with process_pool(process_count) as pool:
        for n in range(process_count):
            if n < process_count - 1:
                chunk = array[n * step:(n + 1) * step]
            else:
                chunk = array[n * step:]
            pool.apply_async(merge_sort_multiple, (results, chunk))

    # Para uma quantidade de processos maior que 2
    # usamos o multiprocessamento novamente para mesclar os subvetores em paralelo
    while len(results) > 1:
        with process_pool(size=process_count) as pool:
            pool.apply_async(
                merge_multiple,
                (results, results.pop(0), results.pop(0))
            )

    timer.stop_for('total_time')

    final_sorted_list = results[0]

    return timer, final_sorted_list