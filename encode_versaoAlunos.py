
#importe as bibliotecas
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
from scipy.fftpack import fft
from scipy import signal as window

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
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

def generateSin(freq, time, fs):
    n = time*fs #numero de pontos
    x = np.linspace(0.0, time, n)  # eixo do tempo
    s = np.sin(freq*x*2*np.pi)
    # plt.figure()
    # plt.plot(x,s)
    return (x, s)


#comeco da main
def main():
    
   
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # Essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # Lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # O tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Construa com amplitude 1.
    # Some as senoides. A soma será o sinal a ser emitido.
    # Utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # Grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    

    print("Inicializando encoder")

    # Definindo variáveis
    fs = 44100
    A = 1
    T = 4
    t = np.linspace(0, T, T*fs)
    NUM = input("Digite um número de 0 a 9: ")
    # Gerando tons base
    x1, y1 = generateSin(697, T, fs)
    x2, y2 = generateSin(1209, T, fs)
    x3, y3 = generateSin(770, T, fs)
    x4, y4 = generateSin(1336, T, fs)
    x5, y5 = generateSin(852, T, fs)
    x6, y6 = generateSin(1477, T, fs)
    x7, y7 = generateSin(941, T, fs)
    x8, y8 = generateSin(1633, T, fs)

    # Gerando tom referente ao símbolo
    if NUM == "1":	
        tone = y1 + y2
    elif NUM == "2":
        tone = y1 + y4
    elif NUM == "3":
        tone = y1 + y6
    elif NUM == "4":
        tone = y3 + y2
    elif NUM == "5":
        tone = y3 + y4
    elif NUM == "6":
        tone = y3 + y6
    elif NUM == "7":
        tone = y5 + y2
    elif NUM == "8":
        tone = y5 + y4
    elif NUM == "9":
        tone = y5 + y6
    elif NUM == "0":
        tone = y7 + y8
    elif NUM == "X":
        tone = y7 + y2
    elif NUM == "#":
        tone = y6 + y7
    elif NUM == "A":
        tone = y1 + y8
    elif NUM == "B":
        tone = y3 + y8
    elif NUM == "C":
        tone = y5 + y8
    elif NUM == "D":
        tone = y7 + y8
    else:
        print("Número inválido")
        exit()

    #Calculando a transformada de Fourier
    X, Y = calcFFT(tone, fs)

    # Plotando gráficos (apenas alguns períodos)
    plt.figure("Sinal no tempo")
    plt.plot(t[:1000], tone[:1000])
    # plt.plot(t, tone)
    plt.title("Sinal no tempo")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Amplitude")


    plt.figure("Transformada de Fourier")
    plt.stem(X, np.abs(Y))
    # plt.plot(t, np.abs(np.fft.fft(tone)))
    plt.title("Transformada de Fourier")
    plt.xlabel("Frequência (Hz)")
    plt.ylabel("Amplitude")
    # Exibindo informações
    sd.play(tone, fs)




    print("Aguardando usuário")
    print("Gerando Tons base")
    print("Executando as senoides (emitindo o som)")
    print("Gerando Tom referente ao símbolo : {}".format(NUM))
    sd.play(tone, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

    print("Fim da transmissão")
    

if __name__ == "__main__":
    main()
