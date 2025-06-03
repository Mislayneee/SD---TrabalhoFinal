# SD---TrabalhoFinal

# PASID Validator - Experimentos com IA Distribuída

Este projeto tem como objetivo avaliar o desempenho de diferentes configurações de serviços de inteligência artificial (IA) em um sistema distribuído baseado em containers Docker. Utilizando a ferramenta PASID-VALIDATOR, foi implementada uma infraestrutura que simula um ambiente com múltiplos nós, balanceadores de carga e serviços de IA, para medir o Tempo Médio de Resposta (MRT) em diferentes cenários.

## Arquitetura do Sistema

A arquitetura é composta por três nós principais que interagem de forma sequencial para processar cada requisição:

- **Nó 01 - Source:** atua como gerador de requisições. Ele envia as mensagens para o primeiro balanceador de carga e também é responsável por coletar os tempos de resposta para análise posterior.
- **Nó 02 - LoadBalancer1:** recebe as requisições do Source e as distribui entre um ou dois serviços de IA leve, dependendo da configuração escolhida. Esses serviços realizam um primeiro estágio de processamento.
- **Nó 03 - LoadBalancer2:** recebe os dados processados do Nó 02 e os distribui entre um ou dois serviços de IA pesada, responsáveis pelo processamento final da requisição.

Cada requisição enviada pelo Source é monitorada em tempo real, e os dados de tempo de resposta são coletados para análise de desempenho.

## Cenários Avaliados

Foram testadas quatro configurações distintas:

- **IA Leve 1:** modelo leve executado em uma única instância.
- **IA Leve 2:** modelo leve executado em duas instâncias com balanceamento de carga.
- **IA Pesada 1:** modelo pesado executado em uma única instância.
- **IA Pesada 2:** modelo pesado executado em duas instâncias com balanceamento de carga.

## Gráfico de Desempenho

Durante os testes, variou-se a taxa de geração de requisições (de 5 até 25 requisições por segundo) e foram coletados os tempos médios de resposta (MRT) em cada configuração.

Abaixo está o gráfico gerado com os resultados obtidos:

![Gráfico MRT](graficoMRT.png)

Os resultados mostram que o uso de réplicas melhora significativamente o desempenho, principalmente quando utilizado com modelos leves. Já os modelos pesados apresentaram tempos médios mais altos, mas também se beneficiaram do balanceamento de carga.
