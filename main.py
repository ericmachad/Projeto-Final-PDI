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

    img = cv2.imread("jogodavelha4.jpeg")
    if img is None:
        print('Erro ao abrir a imagem.\n')
        sys.exit()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(imgGray, 50, 150, apertureSize=3)
    """ lines = cv2.HoughLines(edges, 1, np.pi / 180, 140) """
    lines = cv2.HoughLinesP(edges, 1, np.pi / 200, 110,
                            minLineLength=500, maxLineGap=220)

    linhas_horizontais = []
    linhas_verticais = []
    angle_threshold = 10

    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / \
            np.pi  # Cálculo do ângulo em graus
        if np.abs(angle - 90) < angle_threshold:
            linhas_verticais.append(Linhas(x1, x2, y1, y2))
        else:
            linhas_horizontais.append(Linhas(x1, x2, y1, y2))

    """Unificar linhas Verticais"""
    linhas_verticais.sort(key=get_x1)
    soma_x1 = get_x1(linhas_verticais[0])
    soma_x2 = get_x2(linhas_verticais[0])
    x1_base = get_x1(linhas_verticais[0])
    x2_base = get_x2(linhas_verticais[0])
    qtd_linhas = 1
    menor_y1 = get_y1(linhas_verticais[0])
    maior_y2 = get_y2(linhas_verticais[0])
    media_linhas = []

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
                media_linhas.append(Linhas(
                    round(soma_x1 / qtd_linhas), round(soma_x2 / qtd_linhas), menor_y1, maior_y2))
                qtd_linhas = 1
                soma_x1 = get_x1(linhas_verticais[i])
                x1_base = get_x1(linhas_verticais[i])
                soma_x2 = get_x2(linhas_verticais[i])
                x2_base = get_x2(linhas_verticais[i])
        if (i == len(linhas_verticais) - 1):
            print('chegu')
            if (qtd_linhas == 1):
                print('Não foi identificado o tabuleiro')
            else:
                media_linhas.append(Linhas(
                    round(soma_x1 / qtd_linhas), round(soma_x2 / qtd_linhas), menor_y1, maior_y2))
    for i in media_linhas:
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
    media_linhas = []

    for i in linhas_horizontais:
        print('X1: ' + str(get_x2(i)))
        """ print('X2: ' + str(get_x2(i))) """
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
                media_linhas.append(Linhas(menor_x1, maior_x2,
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
                media_linhas.append(Linhas(menor_x1, maior_x2,  round(
                    soma_y1 / qtd_linhas), round(soma_y2 / qtd_linhas),))
    for i in media_linhas:
        cv2.line(img, (get_x1(i), get_y1(i)),
                 (get_x2(i), get_y2(i)), (0, 255, 0), 2)
    print(menor_x1)
    print(maior_x2)
    cv2.imshow('linesDetected.jpg', img)
    cv2.imwrite('linesDetected.jpg', img * 255)

    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
