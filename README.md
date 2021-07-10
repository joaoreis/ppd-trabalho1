# Trabalho T1.1 - Paralelismo de Processos e Threads

###### João Ubaldo, Renan Evangelista e Úrsula Abreu

### Hardware utilizado na avaliação

- Processador: Ryzen 9 5900X
- Sistema Operacional: Windows 10

## Executando o trabalho

### Requerimentos

- python3
- numpy (utilizado para gerar elementos do vetor e cálculo do desvio padrão)

Para execução do projeto, basta executar os comandos: 

```python
python main_merge.py {numProcessos}
```

Onde ``numProcessos`` é o número de processos, caso não seja definido, o projeto considera a execução com 1 processo. Após 10 execuções gera um output que ficará salvo em um arquivo .txt na pasta raíz. Os resultados das execuções descritas nos resultados se encontram nas pastas de *results*.

## Resultados

Consideramos o vetor de 500.000 elementos, pois a execução de vetores maiores tornava a simulação inviável, o tempo de execução está em segundos:

||1 processo|2 processos|4 processos|8 processos|
|---|---|---|---|---|
|Execução 1|38.668195|35.197648|37.807164|41.005868|
|Execução 2|37.379241|34.911235|37.785723|42.363301|
|Execução 3|37.339352|35.084786|37.803244|42.145312|
|Execução 4|37.370728|35.152831|37.779186|42.221757|
|Execução 5|37.387996|35.107308|37.693332|42.003474|
|Execução 6|37.437906|35.924203|37.725415|42.074632|
|Execução 7|37.435354|36.715642|37.937106|41.995957|
|Execução 8|37.587071|35.253196|37.693561|42.023076|
|Execução 9|37.361332|35.402068|37.547143|42.144430|
|Execução 10|37.501486|35.122042|37.788097|41.923714|
|Média|**37.546866**|**35.387096**|**37.755997**|**41.990152**|
|Desvio Padrão|**0.380422**|**0.512720**|**0.096168**|**0.349631**|

O gráfico das médias:

![](/media/chart1.png)

## Discussões

O gráfico das médias dos tempos execução do *mergesort* apresentou um comportamento inesperado, não comprovando o ganho de se usar paralelismo. Para validar nossa implementação resolvemos implementar a busca de um elemento em um vetor onde esse elemento nunca é encontrado para simular o pior caso da busca e garantir que sempre percorrerá o vetor inteiro.

Para execução dessa busca, basta executar os comandos: 

```python
python main_search.py {numProcessos}
```

Obtivemos os seguintes resultados, considerando um vetor de 5.000.000 de elementos, o tempo de execução está em segundos:

![](/media/chart2.png)

Concluímos que apesar da implementação do *mergesort* não apresentar os resultados esperados, a implementação do paralelismo está correta e apresenta um ganho nítido, indicada pelo gráfico de tempo de execução do *search*.