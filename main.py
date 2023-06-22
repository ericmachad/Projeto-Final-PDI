# Projeto Final
# Alunos: 
# Eric Machado - 2191083
# Gabriel Leão Bernarde - 2194228
# Universidade Tecnológica Federal do Paraná
# ===============================================================================

import numpy as np
import cv2
import sys
      

def main():
    img = cv2.imread("jogodavelha6.jpeg")
    if img is None:
        print('Erro ao abrir a imagem.\n')
        sys.exit()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(imgGray, 50, 150 , apertureSize = 3)
    lines = cv2.HoughLines(edges, 1, np.pi / 280, 170)

    for teste in lines:
        for r, theta in teste:
            a = np.cos(theta) 
            b = np.sin(theta)  
            x0 = a * r 
            y0 = b * r 
            x1 = int(x0 + 1000 * (-b)) 
            y1 = int(y0 + 1000 * (a)) 
            x2 = int(x0 - 1000 * (-b))   
            y2 = int(y0 - 1000 * (a)) 
            cv2.line(img,(x1,y1), (x2,y2), (0, 0, 255), 2) 

    cv2.imshow('linesDetected.jpg', img) 
    cv2.imwrite('linesDetected.jpg', img * 255)     

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()