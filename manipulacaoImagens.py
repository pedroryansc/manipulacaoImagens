import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt

def carregarImagem(caminhoImagem):
    with open(caminhoImagem, "r") as arquivo:
        # Código do formato de imagem
        codigoFormato = arquivo.readline().strip()

        # Pulando linhas de comentário ou linhas vazias, caso existam
        while True:
            linha = arquivo.readline().strip()
            if linha and (not linha.startswith("#")):
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

        # Criação da matriz vazia para preencher com os valores da imagem
        if codigoFormato != "P3":
            matrizPixels = np.empty((altura, largura))
        else:
            # Se for uma imagem PPM, cada pixel é um array com 3 posições (RGB)
            matrizPixels = np.empty((altura, largura, 3))

        indicePixel = 0
        for y in range(altura):
            for x in range(largura):
                if codigoFormato != "P3":
                    matrizPixels[y][x] = listaPixels[indicePixel]
                    indicePixel += 1
                else:
                    for z in range(3):
                        matrizPixels[y][x][z] = listaPixels[indicePixel]
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
    # Carregando a imagem
    imagem = carregarImagem(caminhoImagem)

    conteudo = f"P1\n{imagem['largura']} {imagem['altura']}\n"

    # Invertendo o valor de cada pixel da imagem
    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            conteudo += f"{0 if pixel == 1 else 1} "
        conteudo += "\n"

    # Salvando a imagem PBM negativa
    nomeImagemOriginal = caminhoImagem.replace("img/", "").replace(".pbm", "")
    nomeImagem = f"{nomeImagemOriginal}-Negativo.pbm"
    salvarImagem(nomeImagem, conteudo)

def converterParaPGM_Binario(caminhoImagem):
    # Carregando a imagem
    imagem = carregarImagem(caminhoImagem)

    # Cabeçalho da imagem PGM "binária" (Ex: Imagem de 8 bits -> 0 ou 255)
    conteudo = f"P2\n{imagem['largura']} {imagem['altura']}\n{imagem['maxNiveis']}\n"

    # Cálculo do limiar (Ex: 8 bits -> Limiar = 128)
    limiar = (imagem["maxNiveis"] + 1) / 2

    # Definindo os pixels a partir do limiar
    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            conteudo += f"{0 if pixel <= limiar else imagem['maxNiveis']} "
        conteudo += "\n"
    
    # Salvando a imagem PGM binária
    nomeImagemOriginal = caminhoImagem.replace(".pgm", "")
    nomeImagem = f"{nomeImagemOriginal}-Binario.pgm"
    salvarImagem(nomeImagem, conteudo)

def converterPPMparaPGM(caminhoImagem):
    # Carregando a imagem PPM
    imagem = carregarImagem(caminhoImagem)

    # Cabeçalho da imagem PGM
    conteudo = f"P2\n{imagem['largura']} {imagem['altura']}\n{imagem['maxNiveis']}\n"

    # Cálculo da média dos valores RGB de cada pixel
    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            mediaRGB = round(sum(pixel) / 3)

            conteudo += f"{mediaRGB} "
        conteudo += "\n"

    # Salvando a imagem convertida para PGM
    nomeImagemOriginal = caminhoImagem.replace(".ppm", "")
    nomeImagem = f"{nomeImagemOriginal}.pgm"
    salvarImagem(nomeImagem, conteudo)

def aplicarEscalaCinza(caminhoImagem):
    # Carregando a imagem PPM
    imagem = carregarImagem(caminhoImagem)

    # Cabeçalho da nova imagem
    conteudo = f"P3\n{imagem['largura']} {imagem['altura']}\n{imagem['maxNiveis']}\n"

    # Cálculo da média dos valores RGB de cada pixel
    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            mediaRGB = round(sum(pixel) / 3)

            # Atribuindo a média para cada um dos 3 valores do pixel (RGB)
            for valor in pixel:
                conteudo += f"{mediaRGB} "
        conteudo += "\n"

    # Salvando a imagem PPM com a escala de cinza aplicada
    nomeImagemOriginal = caminhoImagem.replace(".ppm", "")
    nomeImagem = f"{nomeImagemOriginal}-EscalaCinza.ppm"
    salvarImagem(nomeImagem, conteudo)

def alterarValoresRGB(caminhoImagem, valorR=-1, valorG=-1, valorB=-1):
    # Carregando a imagem
    imagem = carregarImagem(caminhoImagem)

    # Cabeçalho da nova imagem
    conteudo = f"P3\n{imagem['largura']} {imagem['altura']}\n{imagem['maxNiveis']}\n"

    # Alterando (ou mantendo) as cores a partir dos parâmetros passados
    for linha in imagem["matrizPixels"]:
        for pixel in linha:
            for cor in range(3):
                # Se for o valor de Red e se Red deve ser alterado,
                if(cor == 0 and valorR >= 0):
                    conteudo += f"{valorR} "
                # Se for o valor de Green e se Green deve ser alterado,
                elif(cor == 1 and valorG >= 0):
                    conteudo += f"{valorG} "
                # Se for o valor de Blue e se Blue deve ser alterado,
                elif(cor == 2 and valorB >= 0):
                    conteudo += f"{valorB} "
                # Se a cor X não deve ser alterada, mantém o valor original
                else:
                    conteudo += f"{int(pixel[cor])} "
        conteudo += "\n"

    # Salvando a imagem
    nomeImagemOriginal = caminhoImagem.replace(".ppm", "")
    nomeImagem = f"{nomeImagemOriginal}-{valorR if valorR >= 0 else 'R'}-{valorG if valorG >= 0 else 'G'}-{valorB if valorB >= 0 else 'B'}.ppm"
    salvarImagem(nomeImagem, conteudo)

def histogramaValoresPixels(caminhoImagem):
    imagem = carregarImagem(caminhoImagem)

    listaPixels = [pixel for linha in imagem["matrizPixels"] for pixel in linha]
        
    if imagem["codigoFormato"] != "P3":
        fig, ax = plt.subplots(1, 1)
        
        ax.hist(listaPixels, rwidth=0.95, color="gray")
    else:
        valoresR = [pixel[0] for pixel in listaPixels]
        valoresG = [pixel[1] for pixel in listaPixels]
        valoresB = [pixel[2] for pixel in listaPixels]

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

        ax1.hist(valoresR, rwidth=0.95, color="red")
        ax2.hist(valoresG, rwidth=0.95, color="green")
        ax3.hist(valoresB, rwidth=0.95, color="blue")
    
    fig.suptitle("Frequência dos valores dos pixels")
    fig.supxlabel("Valores dos pixels")
    fig.supylabel("Frequência")
    
    plt.tight_layout()
    plt.show()

# Execução das funções

# converterNiveisIntensidade("Entrada_EscalaCinza.pgm", 5)
# amplificarBrilho("img/800x800-5bits.pgm", 20)
# converterPGMparaPBM("Entrada_EscalaCinza.pgm")
# aplicarNegativoPBM("img/Entrada_EscalaCinza.pbm")
# converterParaPGM_Binario("Entrada_EscalaCinza.pgm")
# converterPPMparaPGM("Fig1.ppm")
# converterPPMparaPGM("Fig4.ppm")
# aplicarEscalaCinza("Fig4.ppm")
# alterarValoresRGB("Fig4.ppm", valorG=0, valorB=0)
histogramaValoresPixels("Entrada_EscalaCinza.pgm")
histogramaValoresPixels("Fig1.ppm")