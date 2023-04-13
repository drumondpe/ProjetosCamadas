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