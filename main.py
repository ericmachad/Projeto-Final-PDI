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


def main():
    def get_x1(linhas):
        return linhas.x1

    def get_x2(linhas):
        return linhas.x2

    def get_y1(linhas):
        return linhas.y1

    def get_y2(linhas):
        return linhas.y2

    img = cv2.imread("jogodavelha7.jpeg")
    if img is None:
        print('Erro ao abrir a imagem.\n')
        sys.exit()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(imgGray, 50, 80, apertureSize=3)
    """ cv2.imshow('edges.jpg', edges)
    cv2.imwrite('edges.jpg', edges * 255) """
    """ lines = cv2.HoughLines(edges, 1, np.pi / 180, 140) """
    lines = cv2.HoughLinesP(edges, 1, np.pi / 200, 110,
                            minLineLength=300, maxLineGap=220)
    linhas_horizontais = []
    linhas_verticais = []
    angle_threshold = 13

    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1)
        graus = np.degrees(angle)
        if np.abs(graus - 90) < angle_threshold:
            linhas_verticais.append(Linhas(x1, x2, y1, y2))
        elif np.abs(graus) >= 0 and np.abs(graus) < angle_threshold :
            linhas_horizontais.append(Linhas(x1, x2, y1, y2))

    """for i in linhas_horizontais:
        cv2.line(img, (get_x1(i), get_y1(i)),
                 (get_x2(i), get_y2(i)), (0, 0, 255), 2)
    for i in linhas_verticais:
        cv2.line(img, (get_x1(i), get_y1(i)),
                 (get_x2(i), get_y2(i)), (255, 0, 255), 2)
        
      COLOCAR NOS SLIDES ESSA IMAGEM
    cv2.imshow('img.jpg', img)
    cv2.imwrite('img.jpg', img * 255) """
    """Unificar linhas Verticais"""
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
            if (get_x1(linhas_verticais[i]) - x1_base) < 12 * i and (get_x2(linhas_verticais[i]) - x2_base) < 12 * i:
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
            if (get_y1(linhas_horizontais[i]) - y1_base) < 12 * i and (get_y2(linhas_horizontais[i]) - y2_base) < 12 * i:
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
    for i in linhas_horizontais_tabuleiro:
        cv2.line(img, (get_x1(i), get_y1(i)),
                 (get_x2(i), get_y2(i)), (0, 255, 0), 2)

    cv2.circle(img, (get_x1(linhas_horizontais_tabuleiro[0]), get_y1(linhas_verticais_tabuleiro[0])),
               0, (0, 0, 255), 5)

    def encontrar_intersecao(x1, y1, x2, y2, x3, y3, x4, y4):
        if (y4 - y3) * (x2 - x1) == (y2 - y1) * (x4 - x3):
            return None

        x = ((x2 - x1) * (x4 * y3 - x3 * y4) - (x4 - x3) * (x2 * y1 -
             x1 * y2)) / ((x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1))
        y = ((y2 - y1) * (x4 * y3 - x3 * y4) - (y4 - y3) * (x2 * y1 -
             x1 * y2)) / ((x2 - x1) * (y4 - y3) - (x4 - x3) * (y2 - y1))

        return abs(round(x)), abs(round(y))

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

    quadrado1 = img[get_y1(linhas_verticais_tabuleiro[0]): intersecao1[1] - 10,
                    get_x1(linhas_horizontais_tabuleiro[0]): intersecao1[0] - 25]

    
    quadrado2 = img[get_y1(linhas_verticais_tabuleiro[0]): intersecao2[1] - 10,
                intersecao1[0] + 10: intersecao2[0] - 10]
    
    quadrado3 = img[get_y1(linhas_verticais_tabuleiro[0]): intersecao2[1] -10,
                intersecao2[0] + 10: get_x2(linhas_horizontais_tabuleiro[0])]
    

    quadrado4 = img[intersecao1[1] + 15: intersecao3[1] - 10,
                    get_x1(linhas_horizontais_tabuleiro[1]): intersecao3[0] - 25]

    
    quadrado5 = img[intersecao2[1] + 15: intersecao4[1] - 10,
                intersecao3[0] + 10: intersecao4[0] - 10]
    
    quadrado6 = img[intersecao2[1] + 15: intersecao4[1] - 10,
                intersecao4[0] + 10: get_x2(linhas_horizontais_tabuleiro[1]) - 10]
    
    quadrado7 = img[get_y1(linhas_horizontais_tabuleiro[1]) + 15: get_y2(linhas_verticais_tabuleiro[0]),
                get_x1(linhas_horizontais_tabuleiro[1]) + 10: intersecao3[0] - 10]
    
    quadrado8 = img[intersecao3[1] + 15: get_y2(linhas_verticais_tabuleiro[0]),
                intersecao3[0] + 10: intersecao4[0] - 10]
    
    quadrado9 = img[intersecao4[1] + 15: get_y2(linhas_verticais_tabuleiro[1]),
                intersecao4[0] + 15: get_x2(linhas_horizontais_tabuleiro[1]) - 10]

    cv2.circle(img, (abs(intersecao1[0]), abs(intersecao1[1])),
               0, (0, 0, 255), 5)
    cv2.circle(img, (abs(intersecao2[0]), abs(intersecao2[1])),
               0, (255, 0, 0), 5) 
    cv2.circle(img, (abs(intersecao3[0]), abs(intersecao3[1])),
               0, (255, 0, 0), 5) 
    cv2.circle(img, (abs(intersecao4[0]), abs(intersecao4[1])),
               0, (255, 0, 0), 5) 
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
    cv2.imshow('img.jpg', img)
    cv2.imwrite('img.jpg', img * 255)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
