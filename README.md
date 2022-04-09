# [T02B03] : [Implementação API para previsão de preços de _stocks_]
- Nuno Capitão
- João Folhadela

## Sumário

* [Abstract](#abstract)
* [Introdução](#introducao)
  * [API REST](#api)
  * [Simulações Monte Carlos](#simulacoes)
* [Implementação](#implementacao)
  * [boot.py](#boot)
  * [button.py](#button)
  * [data.py](#data)
  * [main.py](#main)
  * [statistics.py](#statistics)
* [Resultados e considerações finais](#resultados)

## <a name= "abstract"></a> Abstract 

O objetivo deste projeto é, usando um serviço REST através do ESP32, adquirir preços de _stocks_ da Bolsa de Valores e, recorrendo a Métodos de Monte Carlo, fazer uma estimativa de qual será o preço para a semana seguinte de uma das quatro _stocks_ analisadas - _Apple, Tesla, Microsoft e Progenity_. O ESP32 irá fazer ainda mais duas funções: permitir ao utilizador escolher uma _stock_ pré-definida com os botões, análogo a um menu interativo, e automaticamente acender os LEDs conforme o resultado da previsão.
## <a name="introducao"></a> Introdução

#### <a name="api"></a> API REST

  API REST é uma interface para programação de aplicações (API) que está em conformidade com as restrições do estilo de arquitetura REST que nos permite interagir com dados pretendidos. Neste projeto recorre-se à API key gratuita do [marketstack](https://marketstack.com/) que é introduzida no programa desenvolvido com recurso à biblioteca _urequests_. O ESP32 tem as suas limitações e o número de _requests_ máximo possível não é o suficiente para se ter uma previsão rigorosa, além disso, dado que a da API key é gratuita, a obtenção de dados fica bastante restringida. Para solucionar este problema adquirimos, a partir do [yahoo! finance](https://finance.yahoo.com/), os valores de fecho semanais médios (relativos aos últimos dois anos) das _stocks_ escolhidas previamente de forma a criar uma base de dados.
 
  
#### <a name="simulacoes"></a> Simulações de Monte Carlo

  As Simulações de Monte Carlo baseiam-se na manipulação de amostras aleatórias massivas para retornar um resultado numérico. Uma vez que não existe um módulo no micropython  que permita gerar uma distribuição normal/gaussiana com parâmetros pré-definidos (como por exemplo o numpy) recorreu-se ao Teorema do Limite Central para tentar aproximar as amostras recolhidas a uma distribuição normal. A implementação destas simulações de Monte Carlo (para este projeto em concreto) são explicadas com mais detalhe na secção [main.py](#main).
  
## <a name="implementacao"></a> Implementação

A implementação do projeto é dividida em 5 ficheiros:
  * boot.py       - Define-se a ligação Wi-Fi e a lista dos preços das _stocks_ pré adquiridos
  * button.py     - Classe para o objeto botão
  * data.py       - Classe (método estático) que define o _Compound Weekly Growth Rate_ (CWGR)
  * main.py       - Modelo para simulação
  * statistics.py -  Classe (método estático) com algumas funções estatísticas 
  
#### <a name= "boot"></a> boot.py

  Este é o código que irá correr primeiramente. É aqui definida a ligação Wi-fi ao ESP32, com recurso à biblioteca _Network_ através da função _do_connect()_. 
  Neste ficheiro são ainda contidas as listas com os valores de fecho históricos das _stocks_ escolhidas previamente.
  
#### <a name= "button"></a> button.py

 Este é o ficheiro que contem a classe criada para os botões conectados ao ESP32. A classe Pin (da biblioteca _machine_) permite processar os níveis lógicos dos botões que são ativos ao nível baixo, onde todos os parâmetros necessários estão definidos na função _init()_. As funções _state()_ e _proc()_ são usadas para verificar se o botão é ou não premido.
 

#### <a name= "data"></a> data.py

 Neste ficheiro é criada a classe Data que serve para criar uma função relativa ao Compound Weekly Growth Rate (CWGR) que é simplesmente a aplicação da fórmula
 
![equation](https://latex.codecogs.com/svg.image?(\frac{v_{i}}{v_{f}})^{\frac{1}{n}})

Onde:
- Vf = valor final
- Vi = valor inicial
- n = nº de períodos  



#### <a name= "statistics"></a> statistics.py
Uma vez que não existe um módulo com funçoes estatisticas no micropython, críamos esta classe com as funções que seriam necessárias para fazer a análise. São elas a média, o desvio padrão e a variância de uma amostra:

 - **mean** - devolve a média
 - **std**  - devolve o desvio padrão
 - **var**  - devolve a variância

Onde:

![equation](https://latex.codecogs.com/svg.image?media&space;=&space;&space;&space;\frac{1}{n}\sum_{i=1}^{n}x_{i}&space;)

![equation](https://latex.codecogs.com/svg.image?variancia&space;=&space;&space;&space;\frac{1}{n-1}&space;&space;&space;(\sum_{i=1}^{n}x_{i}^{2}&space;&space;-&space;&space;\frac{1}{n}\sum_{i=1}^{n}x_{i}&space;)^2)

![equation](https://latex.codecogs.com/svg.image?std&space;=&space;&space;&space;\sqrt{\frac{1}{n-1}&space;&space;&space;(\sum_{i=1}^{n}x_{i}^{2}&space;&space;-&space;&space;\frac{1}{n}\sum_{i=1}^{n}x_{i}&space;)^2}&space;=&space;\sqrt{variancia})


#### <a name= "main"></a> main.py

Neste ficheiro está implementado o modelo criado para as simulações.

  Num loop infinito o valor lógico de cada botão é constantemente avaliado de forma a obter uma resposta caso algum seja premido.
  
  O código inicial corresponde a um pequeno menu interativo de seleção de _stock_ que irá alterar consoante as escolhas do utilizador recorrendo aos botões do microcontrolador (Esquerdo para alterar a escolha da stock, direito para selecionar). Os nomes das stocks estão contidos num dicionário, mas que neste caso é usado sobre a forma de lista de forma a permitir a manipulação por índex.

  A função _menu()_ é ativada quando o botão esquerdo é premido, reimprimindo o código inicial mas com um índex de seleção diferente.  O uso do código “global i” permite que o índex se mantenha gravado e assim mantem a coerência da contagem de seleção.
  
  No caso do botão direito ser premido, a função _veri()_ é ativada. Nesta função está implementado o API REST da marketstack, onde o último valor de fecho é pedido sobre a forma de símbolo da _stock_ selecionada pelo utilizador, também conhecidos como “_Stock Tickers_”, que se encontram no dicionário. Este valor é adicionado à lista de dados que se encontra no boot.py.

  Posteriormente é efetuado o CWGR repartido de 4 em 4 semanas para os valores da lista. A partir destes valores são feitas várias seleções aleatórias pelo método _random_ das amostras da lista, de onde se retira a média de cada uma de forma a tentar aproximar de uma distribuição normal (Teorema do Limite Central). Devido às limitações dos dados, apenas foram retiradas 15 amostras (25 é por norma o valor mínimo), com a agravante de os valores aleatórios selecionados terem uma significativa probabilidade de serem repetidos.

  Obtida esta “distribuição”, o valor de fecho obtido pelo API REST passa pelo processo de simulações de Monte Carlo, para o qual é testado 2000 vezes para os vários valores possíveis de CWGR dentro da lista de médias. Finalmente faz-se uma média para obter uma estimativa de um valor de stock para a próxima semana. 
  É de notar que apenas se usaram valores semanais de forma a diminuir a densidade de dados e permitir um exemplo de aplicação mais fluido, mas que por sua vez, tem uma imprecisão elevada.
  A função vai ainda tratar de ligar os LEDs conforme a previsão - lucro superior a 0.8% LED verde acende; perdas superiores a 0.5% LED vermelho acende; LED amarelo acende para perdas inferiores a 0.5% e para lucros inferiores a 0.8%.



## <a name="resultados"></a> Resultados e considerações finais

Com este projeto foi-nos possível conciliar conhecimentos de programação e estatística adquiridos ao longo do curso e aplicá-los aos conteúdos leccionados em EDM de modo a termos um modelo básico que estima o preço semanal futuro de uma _stock_. O modelo implementado para a simulação diverge bastante do modelo idealizado incialmente devido à limitações do micropython, do ESP32 e da API usada. Como tal, os resultados obtidos são bastante imprecisos e erráticos, ainda assim, foi possível demonstrar um exemplo de aplicação interativa entre várias das componentes do microcontrolador. De uma maneira geral, apesar de todas as imprecisões no modelo devido às adaptações feitas, os resultados obtidos estão de acordo com aquilo que é a intuição comum para previsão de subida ou descida de valores para a stock.
