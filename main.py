# Projeto Final
# Alunos:
# Eric Machado - 2191083
# Gabriel Leão Bernarde - 2194228
# Universidade Tecnológica Federal do Paraná
# ===============================================================================

import numpy as np
import cv2
import sys


class Linhas:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

def verificar_ponto_mais_alto(ponto1,ponto2):
    if(ponto1<=ponto2):
        return ponto1
    if(ponto2<ponto1):
        return ponto2
    
def verificar_ponto_mais_baixo(ponto1,ponto2):
    if(ponto1>=ponto2):
        return ponto1
    if(ponto2>ponto1):
        return ponto2    

def verificar_ponto_mais_esquerda(ponto1,ponto2):
    if(ponto1<=ponto2):
        return ponto1
    if(ponto2<ponto1):
        return ponto2    

def verificar_ponto_mais_direita(ponto1,ponto2):
    if(ponto1>=ponto2):
        return ponto1
    if(ponto2>ponto1):
        return ponto2
         
def gera_simbolo_casa(dp,validacao):
    if(dp>=10.4 and validacao):
        return 'O'
    if(dp < 10.4):
        return ' '
    else:
        return 'X'
    
def calculate_roundness(contour):
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    circularity = (4 * np.pi * area) / (perimeter ** 2)
    return circularity    
 
def verificar_elemento_circular(imagem):
    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(cinza, (13, 13), 0)
    # Aplicar o limiar (threshold)
    threshold = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(threshold, 30, 100)
    # Encontrar os contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_contour = None
    max_area = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    if max_contour is not None:
        circularity = calculate_roundness(max_contour)
        if circularity > 0.2:
            return True
        else:
            return False

        cv2.drawContours(imagem, [max_contour], -1, (0, 255, 0), 2)
        cv2.imshow('Imagem com o maior contorno', imagem)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        return False
def gera_matriz(casa1,casa2,casa3,casa4,casa5,casa6,casa7,casa8,casa9):
    print("",casa1,"|",casa2,"|",casa3,"\n","__________\n",casa4,"|",casa5,"|",casa6,"\n","__________\n",casa7,"|",casa8,"|",casa9)

def define_vencedor(casa1,casa2,casa3,casa4,casa5,casa6,casa7,casa8,casa9):
    contvencedor = 0
    if(casa1==casa2 and casa2==casa3 and casa1!=' '):
        vencedor = casa1
        contvencedor=contvencedor+1
    if(casa4==casa5 and casa5==casa6 and casa4!=' '):
        vencedor = casa4
        contvencedor=contvencedor+1
    if(casa7==casa8 and casa8==casa9 and casa7!=' '):
        vencedor = casa7
        contvencedor=contvencedor+1
    if(casa1==casa4 and casa4==casa7 and casa1!=' '):
        vencedor = casa1
        contvencedor = contvencedor+1
    if(casa2==casa5 and casa5==casa8 and casa2!=' '):
        vencedor = casa2
        contvencedor = contvencedor+1
    if(casa3==casa6 and casa6==casa9 and casa3!=' '):
        vencedor = casa3
        contvencedor = contvencedor+1
    if(casa1==casa5 and casa5==casa9 and casa1!=' '):
        vencedor = casa1
        contvencedor = contvencedor+1
    if(casa3==casa5 and casa5==casa7 and casa3!=' '):
        vencedor = casa3
        contvencedor = contvencedor+1
    if(contvencedor==0):
        print("Não tem vencedor")
    if(contvencedor==1):
        print("O vencedor é o simbolo: ",vencedor)
    if(contvencedor>1):
        print("O jogo está invalido, pois tem mais de 1 vencedor")                
def encontrar_intersecao(x1, y1, x2, y2, x3, y3, x4, y4):
        if (y4 - y3) * (x2 - x1) == (y2 - y1) * (x4 - x3):
            return None

        x = ((x2 - x1) * (x4 * y3 - x3 * y4) - (x4 - x3) * (x2 * y1 -
             x1 * y2)) / ((x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1))
        y = ((y2 - y1) * (x4 * y3 - x3 * y4) - (y4 - y3) * (x2 * y1 -
             x1 * y2)) / ((x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1))

        return abs(round(x)), abs(round(y))
def main():
    def get_x1(linhas):
        return linhas.x1

    def get_x2(linhas):
        return linhas.x2

    def get_y1(linhas):
        return linhas.y1

    def get_y2(linhas):
        return linhas.y2

    img = cv2.imread("jogodavelha2.jpg")
    img_quadrados = img.copy()
    if img is None:
        print('Erro ao abrir a imagem.\n')
        sys.exit()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(imgGray, 50, 80, apertureSize=3)
    cv2.imshow('edges.jpg', edges)
    cv2.imwrite('edges.jpg', edges * 255)
    """ lines = cv2.HoughLines(edges, 1, np.pi / 180, 140) """
    lines = cv2.HoughLinesP(edges, 1, np.pi / 200, 100,
                            minLineLength=300, maxLineGap=220)
    linhas_horizontais = []
    linhas_verticais = []
    angle_threshold = 15

    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1)
        graus = np.degrees(angle)
        if np.abs(graus - 90) < angle_threshold:
            linhas_verticais.append(Linhas(x1, x2, y1, y2))
        elif np.abs(graus) >= 0 and np.abs(graus) < angle_threshold :
            linhas_horizontais.append(Linhas(x1, x2, y1, y2))


    linhas_verticais.sort(key=get_x1)
    soma_x1 = get_x1(linhas_verticais[0])
    soma_x2 = get_x2(linhas_verticais[0])
    x1_base = get_x1(linhas_verticais[0])
    x2_base = get_x2(linhas_verticais[0])
    qtd_linhas = 1
    menor_y1 = get_y1(linhas_verticais[0])
    maior_y2 = get_y2(linhas_verticais[0])
    linhas_verticais_tabuleiro = []

    for i in range(0, len(linhas_verticais)):
        if (i > 0):
            if (get_x1(linhas_verticais[i]) - x1_base) < 12 * i or (get_x2(linhas_verticais[i]) - x2_base) < 12 * i:
                soma_x1 += get_x1(linhas_verticais[i])
                soma_x2 += get_x2(linhas_verticais[i])
                if (menor_y1 > get_y1(linhas_verticais[i])):
                    menor_y1 = get_y1(linhas_verticais[i])
                if (maior_y2 < get_y2(linhas_verticais[i])):
                    maior_y2 = get_y2(linhas_verticais[i])
                qtd_linhas += 1
            else:
                linhas_verticais_tabuleiro.append(Linhas(
                    round(soma_x1 / qtd_linhas), round(soma_x2 / qtd_linhas), menor_y1, maior_y2))
                qtd_linhas = 1
                soma_x1 = get_x1(linhas_verticais[i])
                x1_base = get_x1(linhas_verticais[i])
                soma_x2 = get_x2(linhas_verticais[i])
                x2_base = get_x2(linhas_verticais[i])
        if (i == len(linhas_verticais) - 1):
            if (qtd_linhas == 1):
                print('Não foi identificado o tabuleiro')
            else:
                linhas_verticais_tabuleiro.append(Linhas(
                    round(soma_x1 / qtd_linhas), round(soma_x2 / qtd_linhas), menor_y1, maior_y2))
    for i in linhas_verticais_tabuleiro:
        cv2.line(img, (get_x1(i), get_y1(i)),
                 (get_x2(i), get_y2(i)), (0, 255, 0), 2)

    """Unificar linhas Horizontais"""
    linhas_horizontais.sort(key=get_y1)
    soma_y1 = get_y1(linhas_horizontais[0])
    soma_y2 = get_y2(linhas_horizontais[0])
    y1_base = get_y1(linhas_horizontais[0])
    y2_base = get_y2(linhas_horizontais[0])
    qtd_linhas = 1
    menor_x1 = get_x1(linhas_horizontais[0])
    maior_x2 = get_x2(linhas_horizontais[0])
    linhas_horizontais_tabuleiro = []

    for i in range(0, len(linhas_horizontais)):
        if (i > 0):
            if (get_y1(linhas_horizontais[i]) - y1_base) < 12 * i or (get_y2(linhas_horizontais[i]) - y2_base) < 12 * i:
                soma_y1 += get_y1(linhas_horizontais[i])
                soma_y2 += get_y2(linhas_horizontais[i])
                if (menor_x1 > get_x1(linhas_horizontais[i])):
                    menor_x1 = get_x1(linhas_horizontais[i])
                if (maior_x2 < get_x2(linhas_horizontais[i])):
                    maior_x2 = get_x2(linhas_horizontais[i])
                qtd_linhas += 1
            else:
                linhas_horizontais_tabuleiro.append(Linhas(menor_x1, maior_x2,
                                                           round(soma_y1 / qtd_linhas), round(soma_y2 / qtd_linhas),))
                qtd_linhas = 1
                soma_y1 = get_y1(linhas_horizontais[i])
                y1_base = get_y1(linhas_horizontais[i])
                soma_y2 = get_y2(linhas_horizontais[i])
                y2_base = get_y2(linhas_horizontais[i])
        if (i == len(linhas_horizontais) - 1):
            if (qtd_linhas == 1):
                print('Não foi identificado o tabuleiro')
            else:
                linhas_horizontais_tabuleiro.append(Linhas(menor_x1, maior_x2,  round(
                    soma_y1 / qtd_linhas), round(soma_y2 / qtd_linhas),))
    if(len(linhas_horizontais_tabuleiro) < 2 or len(linhas_verticais_tabuleiro) < 2):
        print('Não foi identificado um tabuleiro')
        return
    for i in linhas_horizontais_tabuleiro:
        cv2.line(img, (get_x1(i), get_y1(i)),
                 (get_x2(i), get_y2(i)), (0, 255, 0), 2)

    

    intersecao1 = encontrar_intersecao(get_x1(linhas_horizontais_tabuleiro[0]), get_y1(linhas_horizontais_tabuleiro[0]),
                                       get_x2(linhas_horizontais_tabuleiro[0]), get_y2(linhas_horizontais_tabuleiro[0]),
                                       get_x1(linhas_verticais_tabuleiro[0]), get_y1(linhas_verticais_tabuleiro[0]),
                                       get_x2(linhas_verticais_tabuleiro[0]), get_y2(linhas_verticais_tabuleiro[0]))
    
    intersecao2 = encontrar_intersecao(get_x1(linhas_horizontais_tabuleiro[0]), get_y1(linhas_horizontais_tabuleiro[0]),
                                       get_x2(linhas_horizontais_tabuleiro[0]), get_y2(linhas_horizontais_tabuleiro[0]),
                                       get_x1(linhas_verticais_tabuleiro[1]), get_y1(linhas_verticais_tabuleiro[1]),
                                       get_x2(linhas_verticais_tabuleiro[1]), get_y2(linhas_verticais_tabuleiro[1]))
    
    intersecao3 = encontrar_intersecao(get_x1(linhas_horizontais_tabuleiro[1]), get_y1(linhas_horizontais_tabuleiro[1]),                                       
                                       get_x2(linhas_horizontais_tabuleiro[1]), get_y2(linhas_horizontais_tabuleiro[1]),
                                       get_x1(linhas_verticais_tabuleiro[0]), get_y1(linhas_verticais_tabuleiro[0]),
                                       get_x2(linhas_verticais_tabuleiro[0]), get_y2(linhas_verticais_tabuleiro[0]))
    
    intersecao4 = encontrar_intersecao(get_x1(linhas_horizontais_tabuleiro[1]), get_y1(linhas_horizontais_tabuleiro[1]),
                                       get_x2(linhas_horizontais_tabuleiro[1]), get_y2(linhas_horizontais_tabuleiro[1]),
                                       get_x1(linhas_verticais_tabuleiro[1]), get_y1(linhas_verticais_tabuleiro[1]),
                                       get_x2(linhas_verticais_tabuleiro[1]), get_y2(linhas_verticais_tabuleiro[1]))
    pontomaisalto=verificar_ponto_mais_alto(get_y1(linhas_verticais_tabuleiro[0]),get_y1(linhas_verticais_tabuleiro[1]))
    pontomaisbaixo=verificar_ponto_mais_baixo(get_y2(linhas_verticais_tabuleiro[0]),get_y2(linhas_verticais_tabuleiro[1]))
    pontomaisesquerda=verificar_ponto_mais_esquerda(get_x1(linhas_horizontais_tabuleiro[0]),get_x1(linhas_horizontais_tabuleiro[1]))
    pontomaisdireita=verificar_ponto_mais_direita(get_x2(linhas_horizontais_tabuleiro[0]),get_x2(linhas_horizontais_tabuleiro[1]))
    quadrado1 = img_quadrados[pontomaisalto: intersecao1[1] - 10,
                    get_x1(linhas_horizontais_tabuleiro[0]): intersecao1[0] - 25]

    
    quadrado2 = img_quadrados[pontomaisalto: intersecao2[1] - 10,
                intersecao1[0] + 10: intersecao2[0] - 10]
    
    quadrado3 = img_quadrados[pontomaisalto: intersecao2[1] -10,
                intersecao2[0] + 10: pontomaisdireita]
    

    quadrado4 = img_quadrados[intersecao1[1] + 20: intersecao3[1] - 10,
                    pontomaisesquerda: intersecao3[0] - 25]

    
    quadrado5 = img_quadrados[intersecao2[1] + 15: intersecao4[1] - 10,
                intersecao3[0] + 10: intersecao4[0] - 15]
    
    quadrado6 = img_quadrados[intersecao2[1] + 15: intersecao4[1] - 10,
                intersecao4[0] + 10: pontomaisdireita - 10]
    
    quadrado7 = img_quadrados[get_y1(linhas_horizontais_tabuleiro[1]) + 15: pontomaisbaixo,
                pontomaisesquerda + 10: intersecao3[0] - 10]
    
    quadrado8 = img_quadrados[intersecao3[1] + 15: pontomaisbaixo,
                intersecao3[0] + 10: intersecao4[0] - 10]
    
    quadrado9 = img_quadrados[intersecao4[1] + 15: pontomaisbaixo,
                intersecao4[0] + 15: pontomaisdireita - 10]

    cv2.circle(img, (abs(intersecao1[0]), abs(intersecao1[1])),
               0, (0, 0, 0), 20)
    cv2.circle(img, (abs(intersecao2[0]), abs(intersecao2[1])),
               0, (0, 0, 0), 20) 
    cv2.circle(img, (abs(intersecao3[0]), abs(intersecao3[1])),
               0, (0, 0, 0), 20) 
    cv2.circle(img, (abs(intersecao4[0]), abs(intersecao4[1])),
               0, (0, 0, 0), 20) 
    cv2.imshow('quadrado.jpg', quadrado1)
    cv2.imwrite('quadrado.jpg', quadrado1 * 255)
    cv2.imshow('quadrado2.jpg', quadrado2)
    cv2.imwrite('quadrado2.jpg', quadrado2 * 255)
    cv2.imshow('quadrado3.jpg', quadrado3)
    cv2.imwrite('quadrado3.jpg', quadrado3 * 255)
    cv2.imshow('quadrado4.jpg', quadrado4)
    cv2.imwrite('quadrado4.jpg', quadrado4 * 255)
    cv2.imshow('quadrado5.jpg', quadrado5)
    cv2.imwrite('quadrado5.jpg', quadrado5 * 255)
    cv2.imshow('quadrado6.jpg', quadrado6)
    cv2.imwrite('quadrado6.jpg', quadrado6 * 255)
    cv2.imshow('quadrado7.jpg', quadrado7)
    cv2.imwrite('quadrado7.jpg', quadrado7 * 255)
    cv2.imshow('quadrado8.jpg', quadrado8)
    cv2.imwrite('quadrado8.jpg', quadrado8 * 255)
    cv2.imshow('quadrado9.jpg', quadrado9)
    cv2.imwrite('quadrado9.jpg', quadrado9 * 255)
    img = cv2.resize(img, (800, 800))
    cv2.imshow('img.jpg', img)
    cv2.imwrite('img.jpg', img * 255)

    DPQUAD1 = np.std(quadrado1)
    DPQUAD2 = np.std(quadrado2)
    DPQUAD3 = np.std(quadrado3)
    DPQUAD4 = np.std(quadrado4)
    DPQUAD5 = np.std(quadrado5)
    DPQUAD6 = np.std(quadrado6)
    DPQUAD7 = np.std(quadrado7)
    DPQUAD8 = np.std(quadrado8)
    DPQUAD9 = np.std(quadrado9)
    """ print("X: ",DPQUAD1)
        print("O: ",DPQUAD2)
        print("X: ",DPQUAD3)
        print("O: ",DPQUAD4)
        print("O: ",DPQUAD5)
        print("X: ",DPQUAD6)
        print("X: ",DPQUAD7)
        print("X: ",DPQUAD8)
        print("O: ",DPQUAD9) """
    elered1=verificar_elemento_circular(quadrado1)
    elered2=verificar_elemento_circular(quadrado2)
    elered3=verificar_elemento_circular(quadrado3)
    elered4=verificar_elemento_circular(quadrado4)
    elered5=verificar_elemento_circular(quadrado5)
    elered6=verificar_elemento_circular(quadrado6)
    elered7=verificar_elemento_circular(quadrado7)
    elered8=verificar_elemento_circular(quadrado8)
    elered9=verificar_elemento_circular(quadrado9)
    casa1=gera_simbolo_casa(DPQUAD1,elered1)
    casa2=gera_simbolo_casa(DPQUAD2,elered2)
    casa3=gera_simbolo_casa(DPQUAD3,elered3)
    casa4=gera_simbolo_casa(DPQUAD4,elered4)
    casa5=gera_simbolo_casa(DPQUAD5,elered5)
    casa6=gera_simbolo_casa(DPQUAD6,elered6)
    casa7=gera_simbolo_casa(DPQUAD7,elered7)
    casa8=gera_simbolo_casa(DPQUAD8,elered8)
    casa9=gera_simbolo_casa(DPQUAD9,elered9)

    gera_matriz(casa1,casa2,casa3,casa4,casa5,casa6,casa7,casa8,casa9)
    define_vencedor(casa1,casa2,casa3,casa4,casa5,casa6,casa7,casa8,casa9)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
