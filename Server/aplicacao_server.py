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
        print('Recebendo pacotes...')
        print('')
        print('Gerando arquivo txt...')
        print('')
        arquivo = open('sem_intercorrencia.txt', 'w')

        nova_imagem = []
        esperado = 1
        total_pacotes = 10
        i=0
        while i < total_pacotes:
            print('Recebendo pacote {}'.format(i+1))
            head = com3.getData(10)[0]
            tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote = le_head(head)
            payload = com3.getData(id_ou_tamanho)[0]
            eop = com3.getData(4)[0]

            if tipo == 3 and numero_pacote == esperado and eop == b'\xaa\xbb\xcc\xdd':
                nova_imagem += payload

                print('Pacote {} recebido com sucesso'.format(i+1))
                
                ## RESPONDENDO PACOTE ##
                print('Respondendo pacote {}'.format(i+1))
                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
                head = cria_head('tipo4', 'livre', 0, total_pacotes, numero_pacote, 0, 0, 0)
                txBuffer = head

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                com3.sendData(np.asarray(txBuffer))
                print('Pacote {} respondido'.format(i+1))
                print('')

                linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Pacote ' + str(i+1) + ' enviado' + ' /tipo4 ' + str(id_ou_tamanho)
                arquivo.write(linha + '\n')

                esperado += 1
                i += 1
            
            elif tipo == 5:
                print('Matando aplicacao')
                com3.disable()
                exit()
            

            else:
                print('Pacote {} COM ERRO'.format(i+1))

                ## RESPONDENDO PACOTE ##
                print('Respondendo pacote {}'.format(i+1))
                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10]
                head = cria_head('tipo6', 'livre', 0, total_pacotes, numero_pacote, 0, i+1, i)
                txBuffer = head

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                com3.sendData(np.asarray(txBuffer))
                print('Pacote {} respondido'.format(i+1))
                print('')

        arquivo.close()

        ### criando imagem ###
        print('Criando imagem...')
        print('')
        
        imagem = open('imagem_recebida.png', 'wb')
        imagem.write(bytes(nova_imagem))
        imagem.close()

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
