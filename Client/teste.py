import crcmod

# Crie uma função para calcular o CRC
def calcular_CRC(dados):
    crc_func = crcmod.predefined.mkCrcFun('crc-16') # Escolha o tipo de CRC que você deseja calcular
    crc = crc_func(dados) # Calcule o CRC para os dados de entrada
    return crc.to_bytes(2, byteorder='big') # Retorne o CRC em bytes

# Exemplo de uso
dados = bytearray([1, 2, 3, 4, 5])
crc = calcular_CRC(dados)
print("Dados: ", dados)
print('CRC: ', crc)


