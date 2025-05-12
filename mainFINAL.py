
"""
07/05/2025

Auteur : Gabin BLANC, Alessandro FRECINA
"""


############## IMPORTS #################

from tkinter import *  
from tkinter import filedialog
import reedsolo
from PIL import Image, ImageDraw
from datetime import *

########### GLOBAL VAR ##################

FICHIER = ""

############ QR GENERATION ################

class QR_Code :
    def __init__(self,message,version = None, negative = "black", positive = "white"):
        if version == None:
            if len(message) < (272-16)//8:
                version = 2
            elif len(message) < (440-16)//8:
                version = 3
            elif len(message) < (640-16)//8:
                version = 4
            elif len(message) < (864-16)//8:
                version = 5
            else:
                raise ValueError("Le message est trop long.")

        self.nombre_de_bits = [272,440,640,864][version-2]
        self.correction_erreur = [10,15,20,26][version-2]
        self.size = [25,29,33,37][version-2]
        self.liste = [[None for i in range(self.size)]for j in range(self.size)]
        self.version = version
        self.message = message
        self.positive = positive
        self.negative = negative
    def patternFixe(self):
       
        """
        Place tout les patternes fixe mais également place les bits de format qui ne change jamais avec l'utilisation du masque 001 et tu correction d'erreur L (11)
        """
        for i in range(8):
            for j in range(8):
                self.liste[i][j] = 0
                self.liste[-(i+1)][j] = 0
                self.liste[i][self.size-1-j] = 0
        self.liste[self.size-8][8] = 1
        def placePatternFinder(x,y):
            for i in range(7):
                for j in range(7):
                    if (j!=6 and j!=0 and i!=0 and i!=6 and (i in [1,5] or j in [1,5])) :
                        self.liste[y+j][x+i] = 0
                    else:
                        self.liste[y+j][x+i] = 1
        def placePatternTiming():
            for i in range(8,self.size-8):
                self.liste[6][i] = (i+1)%2
                self.liste[i][6] = (i+1)%2
    
        def placePatternAlignement():
            for i in range(self.size-9,self.size-4):
                for j in range(self.size-9,self.size-4):
                    self.liste[i][j] = 0
            for i in range(self.size-9,self.size-4):
                self.liste[self.size-9][i] = 1
                self.liste[self.size-5][i] = 1
                self.liste[i][self.size-9] = 1
                self.liste[i][self.size-5] = 1
            self.liste[self.size-7][self.size-7] = 1
        placePatternAlignement()
        placePatternFinder(0, 0)
        placePatternFinder(self.size-7, 0)
        placePatternFinder(0, self.size-7)
        placePatternTiming()
        format_line = '110011110100111'
        line = 0
        for k in range(len(format_line)):
        
            if line <= 8:  
                if self.liste[line][8] == 1:
                    line += 1
                self.liste[line][8] = int(format_line[k])
            if line > 8:
                if self.liste[8][16-line] == 1:
                    line += 1
                self.liste[8][16-line] = int(format_line[k])
            line += 1
        line = 1
        for k in range(len(format_line)):
            if line <= 8:
                self.liste[8][-line] = int(format_line[k])
            if line > 8:
                self.liste[-(16-line)][8] = int(format_line[k])
            line += 1
        
        return

    def placeBits(self,code : str) -> None:
        """
        Place les bits sur la liste en alternant toutes les deux colonnes en démarrant de la droite
        """
        def encodement(code : str) -> str :
            """
            Génère les bits de donnés a partir du texte donné selon la version.
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
            while len(binaire)<self.nombre_de_bits:
                binaire = binaire +liste[0]
                liste[0], liste[1] = liste[1], liste[0]
            return binaire

        def genereCorrectionErreur(data_bits : str) -> str:
            """
            Génère les bits de correction d'érreur en utilisant l'algorithme Reed-Solomon.
            """
            data_bytes = [int(data_bits[i:i+8],2) for i in range(0,len(data_bits),8)]

            rs = reedsolo.RSCodec(self.correction_erreur)
    
            data_encode = rs.encode(bytes(data_bytes))

            ec_bits = ''.join(f'{byte:08b}' for byte in data_encode[-self.correction_erreur:])
    
            return ec_bits


        message = encodement(code)
        message += genereCorrectionErreur(message)

        index = 0
        direction = -1
        row = self.size-1
        col = self.size-1
        while col > 0:
            while 0 <= row < self.size:
                for i in [0,-1]:
                    colonne = col + i
                    ligne = row
                    if 0 <= colonne < self.size and 0 <= ligne < self.size and self.liste[ligne][colonne] is None:
                        if (ligne)%2 == 0:
                            self.liste[ligne][colonne] = int(message[index])-1
                            self.liste[ligne][colonne] = -self.liste[ligne][colonne]
                        else:
                            self.liste[ligne][colonne] = int(message[index])
                        index += 1
                        if index == len(message):
                            self.liste[-9][0] = 1
                            self.liste[-9][1] = 1
                            self.liste[-11][0] = 1
                            self.liste[-11][1] = 1
                            return
                row += direction
            direction *= -1
            row += direction
            col -= 2
            if col == 6:
                col -= 1
        return

    def dessineQR(self)-> None: 
        global FICHIER
        '''
        
        Génere l'image du QRCode qui s'affiche automatiquement.
        L'image se génere avec des carrés plus petit s'il y a une image de fond
        
        '''
        self.patternFixe()
        self.placeBits(self.message)
        taille = 10
        img_taille = 10*self.size
        img = Image.new('RGBA',(img_taille,img_taille), color=(0,0,0,0))
        image = ImageDraw.Draw(img)
        
        Fichier = False
        if FICHIER != "":
            Fichier = True
            FICHIER = Image.open(FICHIER)
            FICHIER = FICHIER.resize((img_taille,img_taille))
            img.paste(FICHIER)
    
        for i in range(len(self.liste)):
            for j in range(len(self.liste[0])):
                if Fichier:
                    if self.liste[i][j]:
                        image.rectangle([(j*taille,i*taille),((j+1)*taille-3),(i+1)*taille-3],self.negative)
                    else:
                        image.rectangle([(j*taille,i*taille),((j+1)*taille-3),(i+1)*taille-3],self.positive)
                else:
                    if self.liste[i][j]:
                        image.rectangle([(j*taille,i*taille),((j+1)*taille),(i+1)*taille],self.negative)
                    else:
                        image.rectangle([(j*taille,i*taille),((j+1)*taille),(i+1)*taille],self.positive)

        
        pic = Image.new("RGBA",(img_taille+40,img_taille+40),color="white")

        pic.paste(img,(20,20))
        pic.show()
        pic.save(f'QR_Code ' + datetime.today().strftime('%Y-%m-%d %Hh%M') + '.png')


############ TKINTER ##################
    

def genereQR():
    """
    Fonction qui permet en appuyant sur le boutton "Génère QR" de parler a la classe QR_Code pour afficher le QR Code
    """
    global FICHIER
    global lbl_genere
    positive={'Orange' : 'orange', "Jaune" : 'yellow', "Blanc" : "white", "Vert" : "lime", "Bleu Clair" : "cornflowerblue","Rose" : "violet"}[couleur_claire.get()]
    negative={'Rouge' : 'darkred', "Bleu" : 'navy', "Noir" : "black", "Violet": "indigo","Vert Foncé": "darkgreen"}[couleur_sombre.get()]
    texte = T.get("1.0","end-1c")
    try:
        QR_Code(texte, None, negative, positive).dessineQR()
        FICHIER = ""
        lbl_image.config(text="")
    except ValueError as e:
        # Si on renvoie une erreur alors le message est forcément trop long avec le raise(ValueError) a la ligne 35
        lbl_genere.config(text='Le message est trop long')
        

def fichierImage():
    """
    Fonction qui permet a l'utilisateur de choisir un fichier et vérifie si ce fichier est une image en .png
    Met le chemin du fichier dans la variable globale FICHIER
    """
    global FICHIER
    global lbl_image
    FICHIER = filedialog.askopenfilename()
    if FICHIER[-3:].lower() != "png":
        lbl8.config(text="Le fichier n'est pas une image")
        FICHIER = ""
    else:
        lbl_image.config(text="L'image a bien été mise")

def removeImage():
    """
    Permet de remettre a 0 la variable globale FICHIER
    """
    global FICHIER
    global lbl_image
    FICHIER = ""
    lbl_image.config(text="L'image a été retirée")

if __name__ == "__main__":

    # On met la fenettre a la bonne taille en mettant egalement un fond gris et enlevant le fait de pouvoir la changer de taille.
    root = Tk()  
    root.geometry("300x500")
    root.resizable(False,False)  
    root['bg'] = 'gray'
    root.title("QR Code GEN")
    # root.iconbitmap("QR_Code.ico"), Utilisant Jupyter on n'a pas réussi a faire en sorte que le programme utilise l'icône

    
    # On défini les couleurs choisissable par l'utilisateur.
    couleurs_noir = ["Noir","Bleu","Rouge","Violet", "Vert Foncé"]
    couleurs_blanc = ["Orange","Jaune","Blanc","Vert","Bleu Clair", "Rose"]

    # On créer la mise en page avec les différents boutton et le champ de texte a remplir.
    Label(root,text="Générateur de QR Code",font=("Helvetica",16),bg="gray").pack()
    Label(root,text="",bg="gray").pack()
    Label(root,text="",bg="gray").pack()
    Label(root,text = "Couleurs des pixels noirs",bg="gray").pack()
    couleur_sombre = StringVar(value="Noir")
    OptionMenu(root,couleur_sombre, *couleurs_noir).pack()
    Label(root,text="",bg="gray").pack()
    Label(root,text="",bg="gray").pack()
    Label(root,text = "Couleurs des pixels blancs",bg="gray").pack()
    couleur_claire = StringVar(value="Blanc")
    OptionMenu(root,couleur_claire, *couleurs_blanc).pack()
    Label(root,text="",bg="gray").pack()
    Label(root,text="",bg="gray").pack()
    Label(root,text = "Message du QR Code",bg="gray").pack()
    T = Text(root,height = 3,width = 30)
    T.pack()
    Label(root,text="",bg="gray").pack()
    Button(root,text = "Ajouter Image de fond",command = fichierImage).pack()
    Button(root,text = "Retirer L'image",command = removeImage).pack()
    lbl_image  = Label(root,text="",bg="gray")
    lbl_image.pack()
    Label(root,text="",bg="gray").pack()
    Button(root,text = "Génère QR",command = genereQR).pack()
    lbl_genere = Label(root,text="",bg="gray")
    lbl_genere.pack()

    root.mainloop()
