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
