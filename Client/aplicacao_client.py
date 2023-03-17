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
        pacotes_totais = tamanho_img // 114
        if tamanho_img % 114 != 0:
            pacotes_totais += 1
        print('Total de pacotes: {}'.format(pacotes_totais)) 


        ## gerando arquivo txt ##
        print('Gerando arquivo txt...')
        print('')
        arquivo = open('sem_intercorrencia.txt', 'w')
        i=0
        while i < pacotes_totais:
            
            if i != pacotes_totais-1:
                linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Pacote ' + str(i+1) + ' enviado' + ' /tipo3' + ' /114'
                arquivo.write(linha + '\n')

                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
                head = cria_head('tipo3', 'livre', 0, pacotes_totais, i+1, 114, 0, 0)
                txBuffer = head

                # Payload
                payload = bytearray(img[i*114:(i+1)*114])
                txBuffer += payload

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                print('Enviando pacote {}...'.format(i+1))
                com3.sendData(np.asarray(txBuffer))
                print('Pacote {} enviado'.format(i+1))
                print('')

            else:
                linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Pacote ' + str(i+1) + ' enviado' + ' /tipo3' + ' /' + str(tamanho_img % 114)
                arquivo.write(linha + '\n')

                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
                head = cria_head('tipo3', 'livre', 0, pacotes_totais, i+1, tamanho_img % 114, 0, 0)
                txBuffer = head

                # Payload
                payload = bytearray(img[i*114:])
                txBuffer += payload

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                print('Enviando pacote {}...'.format(i+1))
                com3.sendData(np.asarray(txBuffer))
                print('Pacote {} enviado'.format(i+1))
                print('')

            ## Recebendo resposta do server ##
            print('Recebendo resposta do server...')
            print('')
            time_start1 = time.time()
            time_start2 = time.time()
            while com3.rx.getIsEmpty() == True:
                if time.time() - time_start1 > 5:
                    print('Tempo de resposta excedido')
                    txBuffer = []
                    # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
                    head = cria_head('tipo3', 'livre', 0, pacotes_totais, i+1, 114, 0, 0)
                    txBuffer = head

                    # Payload
                    payload = bytearray(img[i*114:(i+1)*114])
                    txBuffer += payload

                    #End of Package
                    eop = cria_eop()
                    txBuffer += eop
                    print('Enviando pacote {}...'.format(i+1))
                    com3.sendData(np.asarray(txBuffer))

                    time_start1 = time.time()

                if time.time() - time_start2 > 20:
                    txBuffer = []
                    # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
                    head = cria_head('tipo5', 'livre', 0, pacotes_totais, i+1, tamanho_img % 114, 0, 0)
                    txBuffer = head

                    # Payload
                    payload = bytearray(img[i*114:])
                    txBuffer += payload

                    #End of Package
                    eop = cria_eop()
                    txBuffer += eop
                    print('Enviando pacote {}...'.format(i+1))
                    com3.sendData(np.asarray(txBuffer))

                    com3.disable()
                    exit()
                    
            head = com3.getData(10)[0]
            tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote = le_head(head)
            com3.getData(4)

            if tipo == 4:
                print('Mandar próximo pacote')
            elif tipo == 5:
                print('comunicacao timedout')
                com3.disable()
                exit()
            elif tipo == 6:
                print('Pacote errado')
                i -= 1

            i += 1
            

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
