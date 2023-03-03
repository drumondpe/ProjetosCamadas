import numpy as np
### COMEÇO CRIAR HEAD ###
# HEAD DEVE TER 12 BYTES #
def cria_head(tipo_pacote, tamanho_payload, numero_pacote, total_pacotes, com3):
    head_bytes = []
    
    # Tipo do pacote
    if tipo_pacote == "dados":
        head_bytes += [b'\x00']
    elif tipo_pacote == "comando":
        head_bytes += [b'\x01']
    elif tipo_pacote == "handshake":
        head_bytes += [b'\x02']
    else:
        print('Tipo de pacote não reconhecido')
        print('Encerrando aplicação...')
        com3.disable()
        exit()

    # Tamanho do pacote
    tamanho_pacote = tamanho_payload + 15                           # 12 do head + 3 do payload
    tamanho_pacote = tamanho_pacote.to_bytes(1, byteorder="big")    # transformando em bytes
    head_bytes += [tamanho_pacote]                                  # adicionando ao head

    # Numero do pacote
    numero_pacote = numero_pacote.to_bytes(1, byteorder="big")
    head_bytes += [numero_pacote]

    # Total de pacotes
    total_pacotes = total_pacotes.to_bytes(1, byteorder="big")
    head_bytes += [total_pacotes]
    
    # Completa o head com zeros
    for i in range(8):
        head_bytes += [b'\x00']
    
    return head_bytes
### FIM CRIAR HEAD ######

### COMEÇO LER HEAD ###
def ler_head(com3):
    # Tipo do pacote
    tipo_pacote = com3.getData(1)
    tipo_pacote = int.from_bytes(tipo_pacote[0], byteorder="big")
    if tipo_pacote == 0:
        tipo_pacote = "dados"
        print('Pacote de dados recebido')
    elif tipo_pacote == 1:
        tipo_pacote = "comando"
        print('Pacote de comando recebido')
    elif tipo_pacote == 2:
        tipo_pacote = "handshake"
        print('Pacote de handshake recebido')
    else:
        print('Tipo de pacote não reconhecido')
        print('Encerrando aplicação...')
        com3.disable()
        exit()

    # Tamanho do pacote
    tamanho_pacote = com3.getData(1)
    tamanho_pacote = int.from_bytes(tamanho_pacote[0], byteorder="big")

    # Número do pacote
    numero_pacote = com3.getData(1)
    numero_pacote = int.from_bytes(numero_pacote[0], byteorder="big")

    # Total de pacotes
    total_pacotes = com3.getData(1)
    total_pacotes = int.from_bytes(total_pacotes[0], byteorder="big")

    # Apaga o resto do head
    com3.getData(8)
    print('')
    print('Tipo do pacote: {}' .format(tipo_pacote))
    print('Tamanho do pacote: {}' .format(tamanho_pacote))
    print('Número do pacote: {}' .format(numero_pacote))
    print('')

    return tipo_pacote, tamanho_pacote, numero_pacote, total_pacotes
### FIM LER HEAD ###

### COMEÇO CRIA END ###
def cria_end():
    end_bytes = []
    for i in range(3):
        end_bytes += [b'\xFF']
    return end_bytes
### FIM CRIA END ###

### COMEÇO CRIA PAYLOAD ###
def cria_payload(payload):
    payload_bytes = []
    for i in range(len(payload)):
        payload_bytes += [payload[i].to_bytes(1, byteorder="big")]
    
    return payload_bytes
### FIM CRIA PAYLOAD ###

## COMEÇO CRIA PACOTE ###
def cria_pacote(tipo_pacote, tamanho_payload, numero_pacote, total_pacotes, payload, com3):
    # Cria o head
    head = cria_head(tipo_pacote, tamanho_payload, numero_pacote, total_pacotes, com3)

    # Cria o payload
    # payload = cria_payload(payload)

    # Cria o end
    end = cria_end()

    # Junta tudo
    pacote = head + payload + end
    return pacote
### FIM CRIA PACOTE ###

### COMEÇO LER PACOTE ###
def ler_pacote(com3):
    # Lê o head
    tipo_pacote, tamanho_pacote, numero_pacote, total_pacotes = ler_head(com3)
    tamanho_payload = tamanho_pacote - 15

    # Lê o payload
    payload = com3.getData(tamanho_payload)

    # Lê o end
    print('chegou aqui')
    end = com3.getData(3)[0]
    print('End: {}' .format(int.from_bytes(end, byteorder='big')))
    comparacao = [b'\xFF', b'\xFF', b'\xFF']
    if int.from_bytes(end, byteorder='big') != 16777215:
        print('')
        print('Erro no pacote recebido')
        print('Encerrando aplicação...')
        print('')
        com3.disable()
        exit()
    else:
        print('Pacote recebido com sucesso')
        print('')
    
    return payload, tipo_pacote, numero_pacote, total_pacotes
### FIM LER PACOTE ###

### COMEÇO FAZ FRANGMENTAÇÃO ###
def faz_fragmentacao(payload_total, com3):
    tamanho_payload = len(payload_total)
    numero_pacote = 0
    pacotes = []
    cinquentas = 0
    total_pacotes = 0

    for i in range(tamanho_payload):
        if i % 50 == 0:
            pacote = cria_pacote("dados", 50, numero_pacote, payload_total[i:i+50], com3)
            pacotes.append(pacote)
            numero_pacote += 1
            cinquentas += 1
            total_pacotes += 1

    if tamanho_payload % 50 != 0:
        faltando = cinquentas * 50
        pacote = cria_pacote("dados", tamanho_payload % 50, numero_pacote, payload_total[faltando+1:], com3)
        pacotes.append(pacote)
        total_pacotes += 1


    return pacotes, total_pacotes
### FIM FAZ FRANGMENTAÇÃO ###