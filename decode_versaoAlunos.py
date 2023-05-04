
#Importe todas as bibliotecas
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time

#funcao para transformas intensidade acustica em dB, caso queira usar
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def calcFFT(signal, fs):
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
    N  = len(signal)
    W = window.hamming(N)
    T  = 1/fs
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
    yf = fft(signal*W)
    return(xf, np.abs(yf[0:N//2]))

def plotFFT(signal, fs):
    x,y = calcFFT(signal, fs)
    plt.figure()
    plt.plot(x, np.abs(y))
    plt.title('Fourier')




def main():
    #*****************************instruções********************************
    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    # algo como:
    signal = signalMeu() 
       
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    sd.default.samplerate = 44100  #taxa de amostragem
    sd.default.channels = 1   #voce pode ter que alterar isso dependendo da sua placa
    tempo = 4
    duration = tempo # #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic
    
    #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes) durante a gracação. Para esse cálculo você deverá utilizar a taxa de amostragem e o tempo de gravação
    numAmostras = int(sd.default.samplerate * duration)
    freqDeAmostragem = sd.default.samplerate

    #faca um print na tela dizendo que a captacao comecará em n segundos. e entao 
    #use um time.sleep para a espera
    print("...     INICIO EM 3 SEGUNDOS")
    time.sleep(3)
   
    #Ao seguir, faca um print informando que a gravacao foi inicializada
    print("...     INICIO")

    #para gravar, utilize
    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    audio_limpo = []
    for i in range(len(audio)):
        audio_limpo.append(audio[i][0])

    print("...     FIM")

    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista, isso dependerá so seu sistema, drivers etc...
    #extraia a parte que interessa da gravação (as amostras) gravando em uma variável "dados". Isso porque a variável audio pode conter dois canais e outas informações). 
    
    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    tempo = np.linspace(0, duration, numAmostras, endpoint=False)
    print("tempo: {}" .format(tempo))
  
    # plot do áudio gravado (dados) vs tempo! Não plote todos os pontos, pois verá apenas uma mancha (freq altas).
    plt.plot(tempo, audio)
    plt.title("Audio vs Tempo")
    plt.xlabel("Tempo")
    plt.ylabel("Audio")
       
    ## Calcule e plote o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = signal.calcFFT(audio_limpo, freqDeAmostragem)
    plotFFT(yf, freqDeAmostragem)
    
    #agora, voce tem os picos da transformada, que te informam quais sao as frequencias mais presentes no sinal. Alguns dos picos devem ser correspondentes às frequencias do DTMF!
    #Para descobrir a tecla pressionada, voce deve extrair os picos e compara-los à tabela DTMF
    #Provavelmente, se tudo deu certo, 2 picos serao PRÓXIMOS aos valores da tabela. Os demais serão picos de ruídos.

    # para extrair os picos, voce deve utilizar a funcao peakutils.indexes(,,)
    # Essa funcao possui como argumentos dois parâmetros importantes: "thres" e "min_dist".
    # "thres" determina a sensibilidade da funcao, ou seja, quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    #"min_dist" é relatico tolerancia. Ele determina quao próximos 2 picos identificados podem estar, ou seja, se a funcao indentificar um pico na posicao 200, por exemplo, só identificara outro a partir do 200+min_dis. Isso evita que varios picos sejam identificados em torno do 200, uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.   
    # Comece com os valores:

    index = peakutils.indexes(yf,0.3,50)
    digits = {
    "1":[1209,697], "2":[1336,697], "3":[1477,697], "4":[1209,770], 
    "5":[1336,770], "6":[1477,852], "7":[1209,852], "8":[1336,852],
    "9":[1477,852], "0":[1336,941]
    }

    tolerancia = 10
    resposta = []
    for pico in index:
        print("Pico",xf[pico])
        if 1477-tolerancia <= xf[pico] <= 1477+tolerancia:
            resposta.append(1477)
        if 1336-tolerancia <= xf[pico] <= 1336+tolerancia:
            resposta.append(1336)
        if 1209-tolerancia <= xf[pico] <= 1209+tolerancia:
            resposta.append(1209)
        if 941-tolerancia <= xf[pico] <= 941+tolerancia:
            resposta.append(941)
        if 852-tolerancia <= xf[pico] <= 852+tolerancia:
            resposta.append(852)
        if 770-tolerancia <= xf[pico] <= 770+tolerancia:
            resposta.append(770)
        if 697-tolerancia <= xf[pico] <= 697+tolerancia:
            resposta.append(697)      
    for digit in digits:
        valor = digits[str(digit)]
        if valor[0] in resposta and valor[1] in resposta:
            print(digit)

    #print o valor tecla!!!
    #Se acertou, parabens! Voce construiu um sistema DTMF
    #Se nao acertou, tente entender o porque, reveja conceitos, analise bem os dados etc.

    #Você pode tentar também identificar a tecla de um telefone real! Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

      
    ## Exiba gráficos do fourier do som gravados 
    plt.show()

if __name__ == "__main__":
    main()
