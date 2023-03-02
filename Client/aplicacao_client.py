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
        time.sleep(.2)
        com3.sendData(b'00')
        time.sleep(1)
        #### Resolvendo Bug ####

        print("Abriu a comunicação")
        print("")

        #############################################   
        # Handshake
        # cria_pacote(tipo_pacote, tamanho_payload, numero_pacote, payload, com3)
        handshake = True
        while handshake:
            pergunta = [b'\xEE', b'\xEE', b'\xEE']
            txBuffer = cria_pacote('comando', 3, 0, pergunta, com3)

            # Envia a pergunta
            print('Enviando pergunta...')
            com3.sendData(np.asarray(txBuffer))
            print('Esperando resposta do server...')
            print('')

            time_start = time.time()
            while com3.rx.getIsEmpty() == True:
                if time.time() - time_start > 5:
                    print('Tempo de resposta excedido')
                    tentar_novamente = input('Deseja tentar novamente? (s/n)')
                    if tentar_novamente == 'n':
                        print('Encerrando aplicação...')
                        com3.disable()
                        exit()
                    elif tentar_novamente == 's':
                        break
            
            if com3.rx.getIsEmpty() == False:
                handshake = False

        ##### Servidor vivo #####
        print('Servidor vivo')
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
