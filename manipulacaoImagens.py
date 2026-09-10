import numpy as np
from pathlib import Path

def carregarImagem(caminhoImagem):
    with open(caminhoImagem, "r") as arquivo:
        # Código do formato de imagem
        codigoFormato = arquivo.readline().strip()

        # Pulando linhas de comentário, caso existam
        while True:
            linha = arquivo.readline().strip()
            if not linha.startswith("#"):
                break

        # Resolução da imagem
        largura, altura = map(int, linha.split())

        # Máximo de níveis de intensidade (se for uma imagem PGM ou PPM)
        if codigoFormato != "P1":
            maxNiveis = int(arquivo.readline().strip())
        else:
            maxNiveis = 1

        # Leitura dos valores dos pixels da imagem
        listaPixels = arquivo.read().split()
        
        # Criação da matriz vazia para a nova imagem
        matrizPixels = np.empty((altura, largura))

        indicePixel = 0
        for y in range(largura):
            for x in range(altura):
                matrizPixels[y][x] = listaPixels[indicePixel]
                indicePixel += 1

        imagem = {
            "codigoFormato" : codigoFormato,
            "largura" : largura,
            "altura" : altura,
            "maxNiveis" : maxNiveis,
            "matrizPixels" : matrizPixels
        }

        return imagem

def salvarImagem(nomeImagem, conteudo):
    nomeArquivo = f"img/{nomeImagem}"

    Path("img").mkdir(exist_ok=True)

    with open(nomeArquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)

    print(f"{nomeImagem}: Arquivo salvo.")

def converterNiveisIntensidade(caminhoImagem, novaQuantBits):
    # Carrega a imagem mantendo a quantidade original de níveis de cinza
    imagem = carregarImagem(caminhoImagem)

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
    conteudo = f"P2\n{imagem['largura']} {imagem['altura']}\n{maxNiveisNova}\n"

    # Conversão do valor de cada pixel de acordo com os novos níveis de intensidade
    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            conteudo += f"{round(pixel * fatorConversao)} "
        conteudo += "\n"

    # Salvando o arquivo com as intensidades convertidas
    nomeImagem = f"{imagem['largura']}x{imagem['altura']}-{novaQuantBits}bits.pgm"
    salvarImagem(nomeImagem, conteudo)

def amplificarBrilho(caminhoImagem, porcentagemBrilho):
    # Carregando a imagem
    imagem = carregarImagem(caminhoImagem)

    # Cálculo do fator do brilho
    fatorBrilho = 1 + (porcentagemBrilho / 100)

    # Definição do cabeçalho do arquivo
    conteudo = f"P2\n{imagem['largura']} {imagem['altura']}\n{imagem['maxNiveis']}\n"

    # Amplificação do brilho de cada pixel da imagem
    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            pixelMaisClaro = round(pixel * fatorBrilho)

            # Caso o valor com brilho amplificado ultrapasse o nível máximo de intensidade (ex.: 255),
            # o pixel recebe o valor do nível máximo de intensidade ao invés do resultado da amplificação
            conteudo += f"{pixelMaisClaro if pixelMaisClaro <= imagem['maxNiveis'] else imagem['maxNiveis']} "
        conteudo += "\n"

    # Salvando a imagem com o brilho amplificado
    nomeImagemOriginal = caminhoImagem.replace("img/", "").replace(".pgm", "")
    nomeImagem = f"{nomeImagemOriginal}-{porcentagemBrilho}maisBrilho.pgm"
    salvarImagem(nomeImagem, conteudo)

def converterPGMparaPBM(caminhoImagem):
    # Carregando a imagem
    imagem = carregarImagem(caminhoImagem)

    # Cálculo do limiar a partir da quantidade de níveis de intensidade
    # para definir o valor de um pixel como 0 ou 1
    limiar = (imagem["maxNiveis"] + 1) / 2

    # Definição do cabeçalho do arquivo
    conteudo = f"P1\n{imagem['largura']} {imagem['altura']}\n"

    # Verificação do valor do pixel para defini-lo como 0 ou 1
    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            # Como o 1 está atuando como o preto, 0 é o branco
            conteudo += f"{1 if pixel <= limiar else 0} "
        conteudo += "\n"
    
    # Salvando a imagem no formato PBM
    nomeImagemOriginal = caminhoImagem.replace("img/", "").replace(".pgm", "")
    nomeImagem = f"{nomeImagemOriginal}.pbm"
    salvarImagem(nomeImagem, conteudo)

def aplicarNegativoPBM(caminhoImagem):
    imagem = carregarImagem(caminhoImagem)

    conteudo = f"P1\n{imagem['largura']} {imagem['altura']}\n"

    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            conteudo += f"{0 if pixel == 1 else 1} "
        conteudo += "\n"

    # Salvando a imagem PBM negativa
    nomeImagemOriginal = caminhoImagem.replace("img/", "").replace(".pbm", "")
    nomeImagem = f"{nomeImagemOriginal}-Negativo.pbm"
    salvarImagem(nomeImagem, conteudo)

# Execução das funções

# converterNiveisIntensidade("Entrada_EscalaCinza.pgm", 5)
# amplificarBrilho("img/800x800-5bits.pgm", 20)
converterPGMparaPBM("Entrada_EscalaCinza.pgm")
aplicarNegativoPBM("img/Entrada_EscalaCinza.pbm")