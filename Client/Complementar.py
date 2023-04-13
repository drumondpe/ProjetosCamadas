import numpy as np

### CRIAR HEAD ###
def cria_head(tipo, remetente, livre, total_pacotes, numero_pacote, id_ou_tamanho, pacote_erro, ultimo_pacote, crc):
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

    ### CRC ###
    head += bytearray([crc])

    return head

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

### FAZ CRC ###
def crc(data: bytes) -> int:
    crc = 0xFFFF  # valor inicial do CRC
    polynomial = 0x1021  # polinômio usado para cálculo do CRC

    for byte in data:
        crc ^= byte << 8  # XOR com o byte deslocado 8 bits à esquerda
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1

    return crc & 0xFFFF  # retorna o CRC com 16 bits