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
            # Head = [tipo, tamanho, numero, total]
            head = [b'\x00', b'\x0f', b'\x00', b'\x01']
            head += [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
            txBuffer += head

            #End of Package
            eop = [b'\xff', b'\xff', b'\xff']
            txBuffer += eop
            com3.sendData(np.asarray(txBuffer))

            print('Esperando resposta do server...')
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
        total_pacotes = 0
        i=0
        for i in range(tamanho_img):
            if i % 50 == 0 or i == 0:
                txBuffer = []
                # Head = [tipo, tamanho, numero, total]
                head = [b'\x01', b'\x41', numero_pacote.to_bytes(2, byteorder='big'), pacotes_totais.to_bytes(2, byteorder='big')]
                head += [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
                txBuffer += head

                # Payload
                payload = img[i:i+50]
                txBuffer += payload

                #End of Package
                eop = [b'\xff', b'\xff', b'\xff']
                txBuffer += eop

                pacotes += [txBuffer]
                print('Pacote {} criado'.format(numero_pacote))
                numero_pacote += 1
                cinquentas += 1
                total_pacotes += 1
                i += 50

            elif tamanho_img - i % 50 < 50:
                txBuffer = []
                faltando = cinquentas * 50
                # Head = [tipo, tamanho, numero, total]
                head = [b'\x01', b'\x41', numero_pacote.to_bytes(2, byteorder='big'), pacotes_totais.to_bytes(2, byteorder='big')]
                head += [b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00', b'\x00']
                txBuffer += head

                # Payload
                payload = img[faltando:]
                txBuffer += payload

                #End of Package
                eop = [b'\xff', b'\xff', b'\xff']
                txBuffer += eop

                pacotes += [txBuffer]
                # print('Pacote {} criado'.format(numero_pacote))
        
        print('Fragmentação concluída')
        print('Pacotes criados com sucesso')
        print('')
        ### FRANGMENTAÇÃO ###

        ### ENVIO DOS PACOTES ###
        for i in range(pacotes):
            com3.sendData(np.asarray(pacotes[i]))
            print('Pacote {} enviado'.format(i+1))

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
            check = com3.getData(1)[0]
            if check == b'\x00':
                print('Pacote {} recebido com sucesso'.format(i+1))
            else:
                print('Pacote {} recebido com ERRO'.format(i+1))
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
