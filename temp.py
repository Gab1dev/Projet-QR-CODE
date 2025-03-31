# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PIL import Image, ImageDraw

def DessineQR(qr_code: list,taille : int = 10 )-> None: 
    '''
    Parameters
    ----------
    qr_code : list[list[int]]
        La liste contenant chaque case du QR Code
    taille : int
        La taille du QR Code, taille 1 correspond a 21*21 et on multiplie par la taille. The default is 10.

    Returns
    -------
    None.

    '''
    img_taille = taille*25
    img = Image.new('RGB',(img_taille,img_taille), color="white")
    image = ImageDraw.Draw(img)
    
    
    for i in range(len(qr_code)):
        for j in range(len(qr_code[0])):
            if qr_code[i][j]:
                image.rectangle([(j*taille,i*taille),((j+1)*taille),(i+1)*taille],'black')
        
    img.show()
    img.save('test.png')

QR_Code = [[0 for i in range(25)]for i in range(25)]



def FixedPatterns(qr_code):
    
    for i in range(7):
        qr_code[0][i] = 1
        qr_code[6][i] = 1
        qr_code[-1][i] = 1
        qr_code[-7][i] = 1
        qr_code[0][-i] = 1
        qr_code[6][-i] = 1
        qr_code[i][0] = 1
        qr_code[i][6] = 1
        qr_code[i][-1] = 1
        qr_code[i][-7] = 1
        qr_code[-i][0] = 1
        qr_code[-i][6] = 1
    for i in range(3):
        for j in range(3):
            qr_code[2+i][2+j] = 1
            qr_code[-5+i][2+j] = 1
            qr_code[2+i][-5+j] = 1
    
    return qr_code

QR_Code = FixedPatterns(QR_Code)    
DessineQR(QR_Code,10)
