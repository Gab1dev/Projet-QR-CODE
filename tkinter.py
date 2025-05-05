from tkinter import *  

root = Tk()  
root.geometry("300x400")
root.resizable(False,False)  
root['bg'] = 'gray'
root.title("QR Code GEN")
root.iconbitmap("Qr_code.ico")


def genere_qr():
    print(couleur_sombre.get())
    print(couleur_claire.get())
    print(int(ver.get()[0]))
    print(T.get("1.0","end-1c"))
    


T = Text(root,height = 3,width = 30)


couleurs_noir = ["Noir","Bleu","Rouge"]

couleurs_blanc = ["Orange","Jaune","Blanc"]

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

lbl7  = Label(root,text = "Message du QR Code",bg="gray").pack()

T.pack()
Label(root,text="",bg="gray").pack()

Button(root,text = "Génère QR",command = genere_qr).pack()

root.mainloop()
