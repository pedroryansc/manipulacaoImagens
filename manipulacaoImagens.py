import cv2
import numpy as np
from pathlib import Path

def carregarImagem(caminhoImagem):
    with open(caminhoImagem, "rb") as arquivo:
        # Código do formato de imagem
        codigoFormato = arquivo.readline().decode("utf-8").strip()

        # Pulando linhas de comentário, caso existam
        while True:
            linha = arquivo.readline().decode("utf-8").strip()
            if not linha.startswith("#"):
                break

        # Resolução da imagem
        largura, altura = map(int, linha.split())

        # Máximo de níveis de intensidade
        maxNiveis = int(arquivo.readline().decode("utf-8").strip())

        listaPixels = list(arquivo.read())

        conteudo = f"{codigoFormato}\n{largura} {altura}\n{maxNiveis}"
        
        print(conteudo)
        
        # Criação da matriz vazia para a nova imagem
        matrizPixels = np.empty((altura, largura))
        '''
        for y in largura:
            for x in altura:
                print(x)
        '''

# Por enquanto, funciona apenas com imagens PGM com 8 ou 16 bits de intensidade, que são os formatos identificados pelo OpenCV
def converterNiveisIntensidade(caminhoImagem, novaQuantBits):
    # Carrega a imagem mantendo a quantidade original de níveis de cinza
    imagem = carregarImagem(caminhoImagem)

    # Identificação da resolução da imagem
    largura = imagem.shape[1]
    altura = imagem.shape[0]

    # Identificação do máximo de níveis de cinza da imagem original
    maxNiveisOriginal = imagem["maxNiveis"]
    print(f"Máx. Níveis (Original): {maxNiveisOriginal}")
    
    # Cálculo do máximo de níveis de cinza a partir da nova quantidade de bits
    maxNiveisNova = (2 ** novaQuantBits) - 1
    print(f"Máx. Níveis (Nova): {maxNiveisNova}")

    # Cálculo do fator de conversão
    fatorConversao = maxNiveisNova / maxNiveisOriginal
    print(f"Fator de conversão: {fatorConversao}")

    # Definição do cabeçalho do arquivo
    conteudo = f"P2\n{largura} {altura}\n{maxNiveisNova}\n"

    # Conversão do valor de cada pixel de acordo com os novos níveis de intensidade
    for linha in imagem:
        for pixel in linha:
            conteudo += f"{round(pixel * fatorConversao)} "
        conteudo += "\n"

    # Salvando o arquivo com as intensidades convertidas
    nomeImagem = f"{largura}x{altura}-{novaQuantBits}bits.pgm"
    nomeArquivo = f"img/{nomeImagem}"

    Path("img").mkdir(exist_ok=True)

    with open(nomeArquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

    print(f"{nomeImagem}: Arquivo salvo.")

def amplificarBrilho(caminhoImagem, porcentagemBrilho):
    imagem = cv2.read(caminhoImagem, cv2.IMREAD_UNCHANGED)

    fatorBrilho = 1 + (porcentagemBrilho / 100)

# Execução das funções
# converterNiveisIntensidade("img/800x800-5bits.pgm", 5)
carregarImagem("Entrada_EscalaCinza.pgm")
# carregarImagem("img/800x800-5bits.pgm")