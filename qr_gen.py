def dessineQR(qr_code: list,taille : int = 10 )-> None: 
    '''
    Parameters
    ----------
    qr_code : list[list[int]]
        La liste contenant chaque case du QR Code
    taille : int
        La taille du QR Code, taille 1 correspond a 25*25 et on multiplie par la taille. The default is 10.

    Returns
    -------
    L'image du QRCode qui s'affiche automatiquement.

    '''
    img_taille = taille*25
    img = Image.new('RGB',(img_taille,img_taille), color="white")
    image = ImageDraw.Draw(img)
    
    
    for i in range(len(qr_code)):
        for j in range(len(qr_code[0])):
            if qr_code[i][j]:
                image.rectangle([(j*taille,i*taille),((j+1)*taille),(i+1)*taille],'black')
            else:
                image.rectangle([(j*taille,i*taille),((j+1)*taille),(i+1)*taille],'white')
                
    img.show()
    img.save('test.png')


####################################################################################################################                


def patternFixe(qr_code : list) -> None:
    """
    Place tout les patternes fixe mais également place les bits de format qui ne change jamais avec l'utilisation du masque 001 et tu correction d'erreur L (11)
    """
    for i in range(8):
        for j in range(8):
            qr_code[i][j] = 0
            qr_code[-(i+1)][j] = 0
            qr_code[i][24-j] = 0
    qr_code[17][8] = 1
    def placePatternFinder(x,y):
        for i in range(7):
            for j in range(7):
                if (j!=6 and j!=0 and i!=0 and i!=6 and (i in [1,5] or j in [1,5])) :
                    qr_code[y+j][x+i] = 0
                else:
                    qr_code[y+j][x+i] = 1
    def placePatternTiming():
        for i in range(8,25-7):
            qr_code[6][i] = (i+1)%2
            qr_code[i][6] = (i+1)%2
    
    def placePatternAlignement():
        for i in range(16,21):
            for j in range(16,21):
                qr_code[i][j] = 0
        for i in range(16,21):
            qr_code[16][i] = 1
            qr_code[20][i] = 1
            qr_code[i][16] = 1
            qr_code[i][20] = 1
        qr_code[18][18] = 1
    placePatternAlignement()
    placePatternFinder(0, 0)
    placePatternFinder(25-7, 0)
    placePatternFinder(0, 25-7)
    placePatternTiming()
    format_line = '110011110100111'
    line = 0
    for k in range(len(format_line)):
        
        if line <= 8:  
            if qr_code[line][8] == 1:
                line += 1
            qr_code[line][8] = int(format_line[k])
        if line > 8:
            if qr_code[8][16-line] == 1:
                line += 1
            qr_code[8][16-line] = int(format_line[k])
        line += 1
    line = 1
    for k in range(len(format_line)):
        if line <= 8:
            qr_code[8][-line] = int(format_line[k])
        if line > 8:
            qr_code[-(16-line)][8] = int(format_line[k])
        line += 1
        
        
    
    return


####################################################################################################################                


def placeBits(qr_code : list,message : str) -> None:
    """
    Place les bits sur la liste en alternant toutes les deux colonnes en démarrant de la droi
    """
    size = 25
    index = 0
    direction = -1
    row = 24
    col = 24
    while col > 0:
        while 0 <= row < size:
            for i in [0,-1]:
                colonne = col + i
                ligne = row
                if 0 <= colonne < 25 and 0 <= ligne < 25 and qr_code[ligne][colonne] is None:
                    if (ligne)%2 == 0:
                        qr_code[ligne][colonne] = int(message[index])-1
                        qr_code[ligne][colonne] = -qr_code[ligne][colonne]
                    else:
                        qr_code[ligne][colonne] = int(message[index])
                    index += 1
                    if index == len(message):
                        qr_code[16][0] = 1
                        qr_code[16][1] = 1
                        qr_code[14][0] = 1
                        qr_code[14][1] = 1
                        return
            row += direction
        direction *= -1
        row += direction
        col -= 2
        if col == 6:
            col -= 1
    return
    
####################################################################################################################                

def encodement(code : str) -> str :
    """
    Génère les 272 bits de donnés a partir du texte donné.
    """
    def lettrebinaire(lettre):
        binaire = str(bin(ord(lettre)))[2:]
        for i in range(8-len(binaire)):
            binaire = '0' + binaire
        return binaire
    binaire = "0100"
    longueur = bin(len(code))[2:]
    for i in range(8-len(longueur)):
        longueur = '0' + longueur
    binaire = binaire + longueur
    for i in code : 
        binaire = binaire + lettrebinaire(i)
    binaire = binaire + "0000"
    liste = ["11101100", "00010001"]
    while len(binaire)<272:
        binaire = binaire +liste[0]
        liste[0], liste[1] = liste[1], liste[0]
    return binaire

def genereCorrectionErreur(data_bits : str) -> str:
    """
    Génère les 80 bits de correction d'érreur en utilisant l'algorithme Reed-Solomon.
    """
    data_bytes = [int(data_bits[i:i+8],2) for i in range(0,len(data_bits),8)]

    rs = reedsolo.RSCodec(10)
    
    data_encode = rs.encode(bytes(data_bytes))

    ec_bits = ''.join(f'{byte:08b}' for byte in data_encode[-10:])
    print(len(ec_bits))
    return ec_bits

        
######## MAIN #########


QR_Code = [[None for i in range(25)]for i in range(25)]
patternFixe(QR_Code)
placeBits(QR_Code,encodement("Ceci est un test"))
placeBits(QR_Code,genereCorrectionErreur(encodement("Ceci est un test")))
dessineQR(QR_Code)
