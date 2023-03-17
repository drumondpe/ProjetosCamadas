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
        ### HANDSHAKE ###
        print("Iniciando Handshake")

        handshake = True
        while handshake:
            txBuffer = []
            # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
            head = cria_head('tipo1', 'servidor', 0, 1, 1, 10, 0, 0)
            txBuffer = head

            #End of Package
            eop = cria_eop()
            txBuffer += eop
            print('Enviando handshake...')
            com3.sendData(np.asarray(txBuffer))
            print('Handshake enviado')
            print('')
            time.sleep(1)

            ## Verificando se o server respondeu ##
            head = com3.getData(10)[0]
            tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote = le_head(head)
            if tipo == 2:
                print('Handshake recebido com sucesso')
                print('')
                handshake = False
            else:
                print('Handshake não recebido')
                print('')
                time.sleep(1)
        
        ### DADOS ###
        print('Começando a enviar os pacotes...')
        print('')
        




        com3.disable()
        exit()
            
            # ###############################################################
            # print('Esperando resposta do server...')
            # time_start = time.time()
            # while com3.rx.getIsEmpty() == True:
            #     if time.time() - time_start > 5:
            #         print('Tempo de resposta excedido')
            #         tentar_novamente = input('Deseja tentar novamente? (s/n)')
            #         if tentar_novamente == 'n':
            #             print('Encerrando aplicação...')
            #             com3.disable()
            #             exit()
            #         elif tentar_novamente == 's':
            #             break
            
            # if com3.rx.getIsEmpty() == False:
            #     handshake = False

        ## Recebendo resposta do server ##
        print('Recebendo resposta do server...')
        tipo_pacote = com3.getData(1)[0]
        if tipo_pacote == b'\x00':
            print('Handshake realizado com sucesso')
            print('')
        else:
            print('Handshake não realizado com sucesso')
            com3.disable()
            exit()
        
        tamanho_pacote = com3.getData(1)[0]
        tamanho_pacote = int.from_bytes(tamanho_pacote, byteorder='big')
        print('Tamanho do pacote: {}'.format(tamanho_pacote))
        com3.getData(tamanho_pacote - 2)
        print('Handshake recebido com sucesso')
        print('')
        ### HANDSHAKE ###

        ### FRANGMENTAÇÃO ###
        print('Iniciando fragmentação')
        print('')
        sorriso = 'sorriso.png'
        with open(sorriso, 'rb') as f:
            img = f.read()
        img = bytearray(img)
        tamanho_img = len(img)
        print('Tamanho da imagem: {}'.format(tamanho_img))

        # Definindo tamanho do pacote
        pacotes_totais = tamanho_img // 50
        if tamanho_img % 50 != 0:
            pacotes_totais += 1
        print('Total de pacotes: {}'.format(pacotes_totais)) 

        numero_pacote = 1
        pacotes = []
        cinquentas = 0
        i=0
        while i < tamanho_img:
            if i % 50 == 0 and i < 1300:
                # Head = [tipo, tamanho, numero, total]
                head = bytearray([1, 65])
                head += bytearray([numero_pacote, pacotes_totais])
                head += bytearray([0,0,0,0,0,0,0,0])
                txBuffer = bytearray(head)

                # Payload
                payload = img[i:i+50]
                txBuffer += payload

                #End of Package
                eop = bytearray([255,255,255])
                txBuffer += eop

                pacotes += [txBuffer]
                print('Pacote {} criado'.format(numero_pacote))
                numero_pacote += 1
                cinquentas += 1
                

            elif i % 1300 == 0 and i != 0:
                faltando = tamanho_img - i
                # Head = [tipo, tamanho, numero, total]
                head = bytearray([1, faltando+15])
                head += bytearray([numero_pacote, pacotes_totais])
                head += bytearray([0,0,0,0,0,0,0,0])
                txBuffer = bytearray(head)

                # Payload
                payload = img[i:]
                txBuffer += payload

                #End of Package
                eop = bytearray([255,255,255])
                txBuffer += eop

                pacotes += [txBuffer]
                # print('Pacote {} criado'.format(numero_pacote))
                break
            
            i += 1
        
        print('Fragmentação concluída')
        print('Pacotes criados com sucesso')
        print('')
        ### FRANGMENTAÇÃO ###

        ### ENVIO DOS PACOTES ###
        for i in range(len(pacotes)):
            print('')
            com3.sendData(np.asarray(pacotes[i]))
            print(np.asarray(pacotes[i]))
            print('Pacote {} enviado'.format(i+1))
            print('Tamanho pacote: {}'.format(len(pacotes[i])))
            time.sleep(1)

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

            com3.getData(12)
            check = int.from_bytes(com3.getData(1)[0], byteorder='big')
            if check == 0:
                print('Pacote {} recebido com sucesso'.format(i+1))
            else:
                print('Pacote {} recebido com ERRO'.format(i+1))
                com3.disable()
                exit()
            com3.getData(3)



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
