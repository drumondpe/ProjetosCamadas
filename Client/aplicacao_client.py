#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

from Client.enlace import *
import time
import numpy as np
import random 

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta
#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com3 = enlace(serialName)
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com3.enable()

        #### Resolvendo Bug ####
        time.sleep(.2)
        com3.sendData(b'00')
        time.sleep(1)
        #### Resolvendo Bug ####

        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        

        #############################################   
        #aqui você deverá gerar os dados a serem transmitidos. 
        #seus dados a serem transmitidos são um array bytes a serem transmitidos. Gere esta lista com o 
        #nome de txBuffer. Esla sempre irá armazenar os dados a serem enviados.
        
        txBuffer = []

        comando10 = [b"\xBB"]                 #1 bytes
        comando0 = [b"\xCC"]                #1 bytes
        comando1 = [b"\x00\x00\x00\x00"]    #4 bytes
        comando2 = [b"\x00\x00\xAA\x00"]    #4 bytes
        comando3 = [b"\xAA\x00\x00"]        #3 bytes
        comando4 = [b"\x00\xAA\x00"]        #3 bytes
        comando5 = [b"\x00\x00\xAA"]        #3 bytes
        comando6 = [b"\x00\xAA"]            #2 bytes
        comando7 = [b"\xAA\x00"]            #2 bytes
        comando8 = [b"\x00"]                #1 byte
        comando9 = [b"\xFF"]                #1 byte

        print('')
        print('Gerando comandos...')
        quantidade = random.randint(10, 30)

        for i in range(quantidade):

            comando = random.randint(1, 9)
            if comando == 1:
                txBuffer += [b'\x04'] + comando1
            if comando == 2:
                txBuffer += [b'\x04'] + comando2
            if comando == 3:
                txBuffer += [b'\x03'] + comando3
            if comando == 4:
                txBuffer += [b'\x03'] + comando4
            if comando == 5:
                txBuffer += [b'\x03'] + comando5
            if comando == 6:
                txBuffer += [b'\x02'] + comando6
            if comando == 7:
                txBuffer += [b'\x02'] + comando7
            if comando == 8:
                txBuffer += [b'\x01'] + comando8
            if comando == 9:
                txBuffer += [b'\x01'] + comando9

        print('')
        print('Quantidade de comandos: {}' .format(quantidade))
        print('Quantidade de bytes: {}' .format(len(txBuffer)))
        print('Array de bytes: {}' .format(txBuffer))
        print('')
        
        # comando10 => finalizador
        # txBuffer += comando10


        
        # f = open(barquinho_entrada, 'wb')
        # f.write(txBuffer)
        # f.close()

        #############################################

        #txBuffer = imagem em bytes!
        #txBuffer = b'\x12\x13\xAA'  #isso é um array de bytes
       
        print("meu array de bytes tem tamanho {}" .format(len(txBuffer)))
        #faça aqui uma conferência do tamanho do seu txBuffer, ou seja, quantos bytes serão enviados.
       
            
        #finalmente vamos transmitir os todos. Para isso usamos a funçao sendData que é um método da camada enlace.
        #faça um print para avisar que a transmissão vai começar.
        #tente entender como o método send funciona!
        #Cuidado! Apenas trasmita arrays de bytes!
               
        
        com3.sendData(np.asarray(txBuffer))  #as array apenas como boa pratica para casos de ter uma outra forma de dados
          
        # A camada enlace possui uma camada inferior, TX possui um método para conhecermos o status da transmissão
        # O método não deve estar fincionando quando usado como abaixo. deve estar retornando zero. Tente entender como esse método funciona e faça-o funcionar.
        txSize = com3.tx.getStatus()
        print('enviou = {}' .format(txSize))
        
        #Agora vamos iniciar a recepção dos dados. Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX
        #print um aviso de que a recepção vai começar.
        
        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen
      
        #acesso aos bytes recebidos
        txLen = len(txBuffer)
        rxBuffer, nRx = com3.getData(txLen)
        print("recebeu {} bytes" .format(len(rxBuffer)))
        
        for i in range(len(rxBuffer)):
            print("recebeu {}" .format(rxBuffer[i]))
        

            
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com3.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com3.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
