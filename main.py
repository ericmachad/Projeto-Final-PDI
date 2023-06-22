# Projeto Final
# Alunos: 
# Eric Machado - 2191083
# Gabriel Leão Bernarde - 2194228
# Universidade Tecnológica Federal do Paraná
# ===============================================================================

import numpy as np
import cv2
import sys
from matplotlib import pyplot as plt
    
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
    tabuleiro = {
        "verticalEsquerda": 0,
        "verticalDireita": 0,
        "horizontalCima": 0,
        "horizontalBaixo": 0,
    }


    img = cv2.imread("jogodavelha4.jpeg")
    if img is None:
        print('Erro ao abrir a imagem.\n')
        sys.exit()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(imgGray, 50, 150 , apertureSize = 3)
    cv2.imshow('ed.jpg', edges) 
    """ lines = cv2.HoughLines(edges, 1, np.pi / 180, 140) """
    lines = cv2.HoughLinesP(edges, 1, np.pi / 200, 110, minLineLength = 300, maxLineGap = 220)
    
    """ Hough prob """
    linhas_horizontais = []
    linhas_verticais   = []
    angle_threshold = 10

    for line in lines:
        x1,y1,x2,y2 = line[0]
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi  # Cálculo do ângulo em graus
        if np.abs(angle - 90) < angle_threshold:
            linhas_horizontais.append(Linhas(x1,x2,y1,y2))
        else:
            linhas_verticais.append(line)

    linhas_horizontais.sort(key=get_x1)

    """ for line in linhas_horizontais:
        if(np.abs(line.get_x1(line) - tabuleiro['verticalEsquerda'] > 12) and line.get_x1(line) < tabuleiro['verticalDireita']) :
            tabuleiro['verticalEsquerda'] = line.get_x1(line)
        if(np.abs(line.get_x1(line) - tabuleiro['verticalDireita'] > 12) and line.get_x1(line) > tabuleiro['verticalDireita']) :
            tabuleiro['verticalDireita'] = line.get_x1(line)
 """
    cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 1)        
        
    cv2.imshow('linesDetected.jpg', img) 
    cv2.imwrite('linesDetected.jpg', img * 255) 

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()