from __future__ import print_function
import random
import sys
from parallel_merge_sort import *
import numpy

def get_total_processes():
    # Verifica se foi passado o numero de processos
    # Se nao passar o numero de processos, consideramos 1 processo
    total_processes = int(sys.argv[1]) if (len(sys.argv) > 1) else 1

    print('Usando {} processos'.format(total_processes))

    return total_processes


def main():
    # Armazena a quantidade de processos passado como parametro
    process_count = get_total_processes()

    length = 5_000_000

    # Cria uma lista nao ordenada de valores aleatorios
    array = list(numpy.random.randint(0, 3*length, length))
    times = []

    # O mesmo vetor e ordenado 10 vezes. O tempo de ordenacao e contado dentro da funcao
    # parallel_merge_sort, garantindo que para todas as execucoes
    # a contagem comece e termine no mesmo ponto
    for i in range(10):
        print('Comecando a ordenacao - %d' % (i + 1))
    
        parallel_time, parallel_sorted_list = parallel_merge_sort(array, process_count)

        print('Tempo de execucao: %4.6f segundos' % parallel_time['total_time'])

        times.append(parallel_time['total_time'])

    # Gerando um arquivo para salvar todos os tempos, a media e o desvio padrao
    # Utilizado para faciliar a analise e a geracao dos graficos
    filename = 'mergesort-{}.txt'.format(process_count)

    # Calculo da media
    time_avg = sum(times) / len(times)

    # Calculo do desvio padrao
    time_mdev = numpy.std(times)

    with open(filename, 'w') as result_log:
        for time in times:
            result_log.write("%f\n" % time)
        result_log.write("Media = %f\n" % time_avg)
        result_log.write("Desvio Padrao = %f\n" % time_mdev)
        

if __name__ == "__main__":
    main()
