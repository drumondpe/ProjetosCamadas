from enlace import *
import time
import numpy as np
import random 
from Complementar import *

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta
serialName = "COM4"                  # Windows(variacao de)

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
        print('Gerando arquivo txt...')
        print('')
        arquivo = open('sem_intercorrencia.txt', 'w')

        #############################################   
        ### HANDSHAKE ###
        print('Recebendo Handshake')
        ocioso = True
        while ocioso:
            head = com3.getData(10)[0]
            print(head)
            tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote, crc = le_head(head)
            com3.getData(4)

            if tipo == 1 and remetente == 1:
                linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Handshake recebido' + ' /tipo1'
                arquivo.write(linha + '\n')                
                ocioso = False
                print('Handshake recebido com sucesso')
                print('')

                ## RESPONDENDO HANDSHAKE ##
                print('Respondendo Handshake')
                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10], crc
                head = cria_head('tipo2', 'servidor', 0, 1, 1, 10, 0, 0, [0,0])
                txBuffer = head

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                com3.sendData(np.asarray(txBuffer))
                print('Handshake respondido')
                print('')
                linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Resposta handshake enviada' + ' /tipo2'
                arquivo.write(linha + '\n')
                    
            else:
                time.sleep(1)
                print('Handshake não recebido, tentando novamente...')
                print('')

                print('Respondendo Handshake')
                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10], crc[2]
                head = cria_head('tipo1', 'servidor', 0, 1, 1, 10, 0, 0, [0,0])
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

        nova_imagem = []
        esperado = 1
        total_pacotes = 10
        i=0
        once = True
    
        while i < total_pacotes:
            time_start1 = time.time()
            time_start2 = time.time()
            while com3.rx.getIsEmpty() == True:
                if time.time() - time_start1 > 2:
                    print('Tempo de resposta excedido')
                    txBuffer = []
                    # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10], crc[2]
                    head = cria_head('tipo4', 'livre', 0, total_pacotes, i+1, 0, 0, 0, [0,0])
                    txBuffer = head
                    #End of Package
                    eop = cria_eop()
                    txBuffer += eop
                    print('Enviando pacote {}...'.format(i+1))
                    com3.rx.clearBuffer()
                    com3.sendData(np.asarray(txBuffer))
                    time_start1 = time.time()

                    linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Tempo excedido ' + ' /tipo4'
                    arquivo.write(linha + '\n') 

                if time.time() - time_start2 > 20:
                    txBuffer = []
                    # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10], crc[2]
                    head = cria_head('tipo5', 'livre', 0, total_pacotes, i+1, 0, 0, 0, [0,0])
                    txBuffer = head
                    #End of Package
                    eop = cria_eop()
                    txBuffer += eop
                    print('Enviando pacote {}...'.format(i+1))
                    com3.sendData(np.asarray(txBuffer))
                    print('Tempo de resposta excedido')
                    print('Encerrando comunicação')
                    linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Timeout ' + ' /tipo5'
                    arquivo.write(linha + '\n') 
                    com3.disable()
                    exit()


            print('Recebendo pacote {}'.format(i+1))
            head = com3.getData(10)[0]
            tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote, crc = le_head(head)
            payload = com3.getData(id_ou_tamanho)[0]
            eop = com3.getData(4)[0]

            linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Pacote ' + str(i+1) + ' recebido' + ' /tipo3 ' + str(id_ou_tamanho)
            arquivo.write(linha + '\n')

            if once == True and numero_pacote == 5:
                numero_pacote = 1
                once = False

            crc_chegada = calcular_CRC(payload)
            if tipo == 3 and numero_pacote == esperado and eop == b'\xaa\xbb\xcc\xdd' and  crc_chegada == crc:
                nova_imagem += payload

                print('Pacote {} recebido com sucesso'.format(i+1))
                
                ## RESPONDENDO PACOTE ##
                print('Respondendo pacote {}'.format(i+1))
                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10], crc[2]
                head = cria_head('tipo4', 'livre', 0, total_pacotes, numero_pacote, 0, 0, 0, [0,0])
                txBuffer = head

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                com3.sendData(np.asarray(txBuffer))
                print('Pacote {} respondido'.format(i+1))
                print('')

                linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Enviando confirmacao de recebimento' + ' /tipo4 '
                arquivo.write(linha + '\n')

                esperado += 1
                i += 1
            
            elif tipo == 5:
                linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Timeout' + ' /tipo5 '
                arquivo.write(linha + '\n')
                print('Matando aplicacao')
                com3.disable()
                exit()
            
            else:
                print('Pacote {} COM ERRO'.format(i+1))

                ## RESPONDENDO PACOTE ##
                print('Respondendo pacote {}'.format(i+1))
                txBuffer = []
                # Head = [tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote][10], crc[2]
                head = cria_head('tipo6', 'livre', 0, total_pacotes, numero_pacote, 0, i+1, i, [0,0])
                txBuffer = head

                #End of Package
                eop = cria_eop()
                txBuffer += eop
                com3.sendData(np.asarray(txBuffer))
                print('Pacote {} respondido'.format(i+1))
                print('')

                linha = str(time.asctime(time.localtime(time.time()))) + ' - ' + 'Pedindo reeinvio ' + ' /tipo6 '
                arquivo.write(linha + '\n')

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