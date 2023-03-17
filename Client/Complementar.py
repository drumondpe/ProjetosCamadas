import numpy as np

### CRIAR HEAD ###
def cria_head(tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote):
    head = bytearray([])

    ### Tipo ###
    if tipo == 'tipo1':
        head += bytearray([1])
    elif tipo == 'tipo2':
        head += bytearray([2])
    elif tipo == 'tipo3':
        head += bytearray([3])
    elif tipo == 'tipo4':
        head += bytearray([4])
    elif tipo == 'tipo5':
        head += bytearray([5])
    elif tipo == 'tipo6':
        head += bytearray([6])

    ### Remetente ###
    if remetente == 'servidor':
        head += bytearray([1])
    else:
        head += bytearray([0])

    ### Livre ###
    head += bytearray([0])

    ### Total de Pacotes ###
    head += bytearray([total_pacotes])

    ### Número do Pacote ###
    head += bytearray([numero_pacote])

    ### ID ou Tamanho ###
    head += bytearray([id_ou_tamanho])

    ### Pacote de Erro ###
    head += bytearray([pacote_erro])

    ### Último Pacote ###
    head += bytearray([ultimo_pacote])

    ### Completa ultimos 2 bytes ###
    head += bytearray([0,0])

    return head

### CRIAR PAYLOAD ###
def cria_payload():
    payload = bytearray([])

    return payload

### CRIAR EOP ###
def cria_eop():
    eop = bytearray([170,187,204,221])
    return eop

### LE HEAD ###
def le_head(head):
    tipo = head[0]
    remetente = head[1]
    livre = head[2]
    total_pacotes = head[3]
    numero_pacote = head[4]
    id_ou_tamanho = head[5]
    pacote_erro = head[6]
    ultimo_pacote = head[7]

    return tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote

def cria_pacote2(tipo_pacote, tamanho_payload, numero_pacote, total_pacotes, payload, com3):
    # Cria o head
    head = cria_head(tipo_pacote, tamanho_payload, numero_pacote, total_pacotes, com3)

    # Cria o payload
    # payload = cria_payload(payload)

    # Cria o end
    end = cria_eop()

    # Junta tudo
    pacote = bytearray(head) + payload + bytearray(end)
    return pacote

### COMEÇO FAZ FRANGMENTAÇÃO ###
def faz_fragmentacao(payload_total, com3):
    tamanho_payload = len(payload_total)
    pacotes_totais = tamanho_payload // 50
    if tamanho_payload % 50 != 0:
        pacotes_totais += 1
    print('aqui 0')
    numero_pacote = 0
    pacotes = []
    cinquentas = 0
    total_pacotes = 0
    print('aqui 1')
    for i in range(tamanho_payload):
        if i % 50 == 0 and i != 0:
            pacote = cria_pacote2("dados", 50, numero_pacote, pacotes_totais, payload_total[i:i+50], com3)
            print('antes')
            pacotes.append(pacote)
            print('depois')
            numero_pacote += 1
            cinquentas += 1
            total_pacotes += 1
    print('aqui 2')
    if tamanho_payload % 50 != 0:
        faltando = cinquentas * 50
        pacote = cria_pacote2("dados", tamanho_payload % 50, numero_pacote, pacotes_totais, payload_total[faltando+1:], com3)
        pacotes.append(pacote)
        total_pacotes += 1
    print('aqui 3')

    return pacotes, total_pacotes
### FIM FAZ FRANGMENTAÇÃO ###