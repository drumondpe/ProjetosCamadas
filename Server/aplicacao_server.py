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
        
        print('esperando 1 byte de sacrificio')
        rxBuffer, nRx = com3.getData(1)
        com3.rx.clearBuffer()
        time.sleep(1)
        #### Resolvendo Bug ####

        print("Abriu a comunicação")
        print('')

        #############################################   
        ### HANDSHAKE ###
        print('Recebendo Handshake')
        ocioso = True
        while ocioso:
            head = com3.getData(10)[0]
            print(head)
            tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote = le_head(head)
            com3.getData(4)

            if tipo == 1 and remetente == 1:                
                ocioso = False
                print('Handshake recebido com sucesso')
                print('')

                ## RESPONDENDO HANDSHAKE ##
                print('Respondendo Handshake')
                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
                head = cria_head('tipo2', 'servidor', 0, 1, 1, 10, 0, 0)
                txBuffer = head

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                com3.sendData(np.asarray(txBuffer))
                print('Handshake respondido')
                print('')
                    
            else:
                time.sleep(1)
                print('Handshake não recebido, tentando novamente...')
                print('')

                print('Respondendo Handshake')
                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
                head = cria_head('tipo1', 'servidor', 0, 1, 1, 10, 0, 0)
                txBuffer = head

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                com3.sendData(np.asarray(txBuffer))
                print('Handshake respondido')
                print('')
            

        ### DADOS ###



        com3.disable()
        exit()
        
        tamanho_pacote = com3.getData(1)[0]
        tamanho_pacote = int.from_bytes(tamanho_pacote, byteorder='big')
        print('Tamanho do pacote: {}'.format(tamanho_pacote))
        com3.getData(tamanho_pacote - 2)
        print('Handshake recebido com sucesso')
        print('')

        ## Respondendo Handshake ##
        print('Respondendo Handshake')
        txBuffer = []
        # Head = [tipo, tamanho, numero, total]
        head = [b'\x00', b'\x0f', b'\x00', b'\x01']
        head += [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
        txBuffer += head

        #End of Package
        eop = [b'\xff', b'\xff', b'\xff']
        txBuffer += eop
        com3.sendData(np.asarray(txBuffer))
        print('Handshake enviado com sucesso')
        print('')
        ### HANDSHAKE ###

        ### RECEBENDO PACOTES ###
        print('Recebendo pacotes...')
        
        nova_imagem = []
        esperado = 1
        total_pacotes = 10
        i=0
        while i < total_pacotes:
            print('Recebendo pacote {}'.format(i))
            tipo_pacote = com3.getData(1)[0]
            tamanho_pacote = int.from_bytes(com3.getData(1)[0], byteorder='big')
            numero_pacote = int.from_bytes(com3.getData(1)[0], byteorder='big')
            total_pacotes = int.from_bytes(com3.getData(1)[0], byteorder='big')
            com3.getData(tamanho_pacote - 4)

            if numero_pacote == esperado:
                payload = com3.getData(tamanho_pacote - 15)[0]
                nova_imagem += payload
                if com3.getData(3) == b'\xff\xff\xff':
                    print('Pacote {} recebido com sucesso'.format(i))
                    print('')
                    esperado += 1
                    i += 1

                    # Head = [tipo, tamanho, numero, total]
                    head = [b'\x00', b'\x0f', b'\x00', b'\x01']
                    head += [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
                    txBuffer += head
                    # Payload
                    payload = [b'\x00']
                    txBuffer += payload
                    #End of Package
                    eop = [b'\xff', b'\xff', b'\xff']
                    txBuffer += eop
                    com3.sendData(np.asarray(txBuffer))

                else:
                    print('Pacote {} não recebido'.format(i))
                    print('')

                    # Head = [tipo, tamanho, numero, total]
                    head = [b'\x00', b'\x0f', b'\x00', b'\x01']
                    head += [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
                    txBuffer += head
                    # Payload
                    payload = [b'\x01']
                    txBuffer += payload
                    #End of Package
                    eop = [b'\xff', b'\xff', b'\xff']
                    txBuffer += eop
                    com3.sendData(np.asarray(txBuffer))
                    print('Encerrando comunicação')
                    com3.disable()
                    exit()
            else:
                # Head = [tipo, tamanho, numero, total]
                head = [b'\x00', b'\x0f', b'\x00', b'\x01']
                head += [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
                txBuffer += head
                # Payload
                payload = [b'\x01']
                txBuffer += payload
                #End of Package
                eop = [b'\xff', b'\xff', b'\xff']
                txBuffer += eop
                com3.sendData(np.asarray(txBuffer))
                print('Encerrando comunicação')
                com3.disable()
                exit()
            




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
