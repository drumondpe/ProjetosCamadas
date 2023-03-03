#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################

from enlace import *
import time
import numpy as np
import random 
import sys
sys.path.insert(1, './ProjetosCamadas')
from Complementar import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta
serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        print("Iniciou o main")
        com3 = enlace(serialName)
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com3.enable()

        #### Resolvendo Bug ####
        
        print('esperando 1 byte de sacrificio')
        rxBuffer, nRx = com3.getData(1)
        com3.rx.clearBuffer()
        time.sleep(1)
        #### Resolvendo Bug ####

        print("Abriu a comunicação")
        print('')

        #############################################   
        payload, tipo_pacote, numero_pacote, total_pacotes = ler_pacote(com3)
        if tipo_pacote == 'handshake':
            print('Handshake realizado com sucesso')
            print('')
        else:
            print('Handshake não realizado com sucesso')
            com3.disable()
            exit()

        volta_handshake = cria_pacote('handshake', 0, 0, payload, com3)
        com3.sendData(np.asarray(volta_handshake))
        time.sleep(1)

        ### RECEBENDO PACOTES ###
        print('Recebendo pacotes...')
        print('')
        pacotes = []
        
        pacote_esperado = 0
        payload, tipo_pacote, numero_pacote, total_pacotes = ler_pacote(com3)
        while numero_pacote <= total_pacotes:
            pacotes += [payload]
            payload, tipo_pacote, numero_pacote, total_pacotes = ler_pacote(com3)
            
            if pacote_esperado == numero_pacote:
                print('Pacote recebido com sucesso')
                confirmacao = cria_pacote('comando', 0, 0, np.asarray[b'\x00'], com3)
                com3.sendData(np.asarray(confirmacao))
                pacote_esperado += 1
                print('Confirmação enviada')
            else:
                print('Pacote recebido com erro')
                confirmacao = cria_pacote('comando', 0, 0, np.asarray[b'\x01'], com3)
                com3.sendData(np.asarray(confirmacao))
                print('Confirmação de erro enviada')

   
        print('Pacotes recebidos com sucesso')
        print('')

        ### TRANSFORMANDO BYTES EM IMAGEM ###
        print('Transformando bytes em imagem...')
        print('')
        imagem = b''.join(pacotes)
        print('Imagem transformada com sucesso')
        print('')

        ### SALVANDO IMAGEM ###
        print('Salvando imagem...')
        print('')
        with open('imagem_recebida.png', 'wb') as f:
            f.write(imagem)
        print('Imagem salva com sucesso')
        print('Imagem salva como: imagem_recebida.png')
        print('')

        ### ENVIANO CONFIRMAÇÃO DE RECEBIMENTO ###
        print('Enviando confirmação de recebimento...')
        print('')
        confirmacao = cria_pacote('comando', 0, 0, np.asarray[b'\x00'], com3)
        com3.sendData(np.asarray(confirmacao))
        print('Confirmação de recebimento enviada')
        print('')

        #############################################
    
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
