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

    # Tamanho do payload
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
def ler_head(pacote, com3):
    # Tipo do pacote
    tipo_payload = com3.getData(1)
    tipo_payload = int.from_bytes(tipo_payload[0], byteorder="big")
    if tipo_payload == 0:
        tipo_payload = "dados"
    elif tipo_payload == 1:
        tipo_payload = "comando"
    else:
        print('Tipo de pacote não reconhecido')
        print('Encerrando aplicação...')
        com3.disable()
        exit()

    # Tamanho do payload
    tamanho_payload = com3.getData(1)
    tamanho_payload = int.from_bytes(tamanho_payload[0], byteorder="big")

    # Número do pacote
    numero_pacote = com3.getData(1)
    numero_pacote = int.from_bytes(numero_pacote[0], byteorder="big")

    # Apaga o resto do head
    com3.getData(9)
    print('')
    print('Tipo do pacote: {}' .format(tipo_payload))
    print('Tamanho do payload: {}' .format(tamanho_payload))
    print('Número do pacote: {}' .format(numero_pacote))
    print('')

    return tipo_payload, tamanho_payload, numero_pacote
### FIM LER HEAD ###

