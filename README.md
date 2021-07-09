# Trabalho T1.1 - Paralelismo de Processos e Threads

---

João Ubaldo, Renan Evangelista e Úrsula Abreu

## Executando o trabalho

Para execução do projeto, basta executar os comandos: 

```python
python main.py {numProcessos}
```

Onde ``numProcessos`` é o número de processos, caso não seja definido, o projeto considera a exceução com 1 processo. O output da execução ficará salvo em um arquivo .txt na pasta raíz.

## Resultados

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

![](/media/chart.png)