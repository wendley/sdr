 Fluxo no jFed

- Login (PEM certificate)

No Nó TX:
- Upload instalar.sh (dir 'SDR')
- No terminal: chmod +x InstalarNo0.sh
- Executar com ./instalar.sh 0
- Executar: grcc -e TXOnlyLQE.grc

No Nó RX:
- Upload instalar.sh (dir 'SDR')
- No terminal: chmod +x InstalarNo1.sh
- Executar com ./instalar.sh 1
- Executar: grcc -e RXOnly.grc

_______________________________________
Para atualizar:

 rodar atualizarLOCAL.sh (localmente)

 rodar recompilarLQE.sh remotamente, para reinstalar gr-lqe
 rodar recompilarMar.sh remotamente, para reinstalar gr-802154
 rodar clone.sh remotamente para baixar os arquivos da pasta sdr


=======================================
=======================================

CENÁRIOS DE AVALIAÇÃO DO EXPERIMENTO:

1 - Sem ruído artificial
2 - Com ruído art, fonte prox Rx
    (fazer estudo da posicao da fonte de ruido)

a - KLE
b - PRR
c - LQL
d - PRR2
e - LQR3

i - Com tráfego regular (intervalo constante)
ii - Com tráfego irregular (intervalos pseudoaleatórios)

I - single sender
II - multiple senders

=======================================
=======================================

TAREFAS CURTO PRAZO:

- Ver como o Foresse 4C calcula
      - WMEWMA filter to 5 packets and α to 0.9
      - mimic the ETX calculation of 4Bit
          - window size: 5
          -  alpha = 0.9
      - RSSI, SNR e LQI + PRR c/ WMEWMA
      - usa Logistic Regression
          - sigmoid function with 5 line 1 bit shift
- Atualizar o machine learning
      - Targets duplos - DONE
      - Fit com, INICIALMENTE, 4 amostras
- Adicionar métrica tempo total e custo de entrega (reenvios x gain)
- Comparar
- Adicionar novo cenário (tráfego irregular) - feito
- Novo cenário: multiple senders - feito
- Usar Random Msg com contador para limitar a qtde de msgs - feito

- Gráfico RSSI x PRR x PRR2 x LQL x LQR3

uhd_siggen -f 2.48G -g 85 --gaussian
_______________________________________

ADD LATEX:

- ZigBee
  - Formatos frames
- Configurações/parâmetros do mac 802154


- Estrutura
  - 1: Cenários de motivação
  - 1: Desafios de pesquisa



_______________________________________

PROBLEMA ATUAL:

- RSSI está funcionando mas com muitas perdas
    - Estimativa do RSSI está quase sempre 1.0 (supondo boa qualidade...)
    - Precisa de uma nova calibração

_______________________________________

TRABS FUTUROS:

- LQE p/ redes sem acks
- ML não supervisionado com retroalimentação
- Avaliar mapeamento calibração da estimativa com gain tx não linear
- Sistema de calibração automático do RSSI


=======================================
386,00 5x
358,00
=======================================

ACESSO AOS USRPs EM TCD:
Precisa instalar:
- pip
- matplot

sudo apt-get install python-pip -y; sudo apt-get install python-matplotlib -y

* Samp modificado para 5M



MSG:

01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
0123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
