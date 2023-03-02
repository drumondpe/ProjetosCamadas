### COMEÇO CRIAR HEAD ###
# HEAD DEVE TER 12 BYTES #
def cria_head(tipo_pacote, tamanho_payload, numero_pacote, com3):
    head_bytes = []
    
    # Tipo do pacote
    if tipo_pacote == "dados":
        head_bytes += [b'\x00']
    elif tipo_pacote == "comando":
        head_bytes += [b'\x01']
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
    
    # Completa o head com zeros
    for i in range(9):
        head_bytes += [b'\x00']
    
    return head_bytes
### FIM CRIAR HEAD ######

### COMEÇO LER HEAD ###
def ler_head(com3):
    # Tipo do pacote
    tipo_payload = com3.getData(1)
    tipo_payload = int.from_bytes(tipo_payload[0], byteorder="big")
    if tipo_payload == 0:
        tipo_payload = "dados"
        print('Pacote de dados recebido')
    elif tipo_payload == 1:
        tipo_payload = "comando"
        print('Pacote de comando recebido')
    else:
        print('Tipo de pacote não reconhecido')
        print('Encerrando aplicação...')
        com3.disable()
        exit()

    # Tamanho do pacote
    tamanho_pacote = com3.getData(1)
    tamanho_pacote = int.from_bytes(tamanho_pacote[0], byteorder="big")
    print('Tamanho do pacote: {}' .format(tamanho_pacote))

    # Número do pacote
    numero_pacote = com3.getData(1)
    numero_pacote = int.from_bytes(numero_pacote[0], byteorder="big")

    # Apaga o resto do head
    com3.getData(9)
    print('')
    print('Tipo do pacote: {}' .format(tipo_payload))
    print('Tamanho do payload: {}' .format(tamanho_pacote))
    print('Número do pacote: {}' .format(numero_pacote))
    print('')

    return tamanho_pacote, numero_pacote
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
def cria_pacote(tipo_pacote, tamanho_payload, numero_pacote, payload, com3):
    # Cria o head
    head = cria_head(tipo_pacote, tamanho_payload, numero_pacote, com3)

    # Cria o payload
    payload = cria_payload(payload)

    # Cria o end
    end = cria_end()

    # Junta tudo
    pacote = head + payload + end
    return pacote

### COMEÇO LER PACOTE ###
def ler_pacote(com3):
    # Lê o head
    tamanho_pacote, numero_pacote = ler_head(com3)
    tamanho_payload = tamanho_pacote - 15

    # Lê o payload
    payload = com3.getData(tamanho_pacote)

    # Lê o end
    end = com3.getData(3)
    if end != [b'\xFF', b'\xFF', b'\xFF']:
        print('')
        print('Erro no pacote recebido')
        print('Encerrando aplicação...')
        print('')
        com3.disable()
        exit()
    else:
        print('Pacote recebido com sucesso')
        print('')
    
    return payload
