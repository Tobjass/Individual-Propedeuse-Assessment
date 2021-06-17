import tkinter as tk
from PIL import ImageTk, Image

def run(window, bovenste_kaart_stok, aantal_kaarten_stok, aantal_kaarten_hand):
    window.configure(background="#d6e0f5")

    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_aanmaken(window, speler, bovenste_kaart_stok, aantal_kaarten_stok, 7 + aantal_kaarten_hand,
                         (6 + aantal_kaarten_hand if (speler != 2) else 6) if (speler < 3) else 1,
                         1 if (speler < 3) else (6 + aantal_kaarten_hand if (speler != 2) else 6),
                         -1 if (speler < 3) else 1)

    window.mainloop()

def stapels_aanmaken(window, speler, bovenste_kaart_stok, aantal_kaarten_stok, aantal_kaarten_hand, start, stop, step):
    for stapel in range(start, stop, step):
        window.columnconfigure(stapel, weight=1, minsize=75)

        temp_stapel = aantal_kaarten_hand - stapel if (speler != 3) else stapel

        if speler == 2 and stapel == 6:
            image = ImageTk.PhotoImage(Image.open("Images/Trekstapel.png"))

            label = tk.Label(window, image=image, background="#d6e0f5")
            label.image = image
            label.grid(row=speler, column=stapel, padx=100)
        elif speler != 2 and temp_stapel == 1:
            Image.open("Images/{}/{} ({}).png".format(bovenste_kaart_stok, bovenste_kaart_stok,
                                                      5 if (aantal_kaarten_stok > 5) else aantal_kaarten_stok))
            image = ImageTk.PhotoImage(image.rotate(180 if (speler == 1) else 0))

            label = tk.Label(window, image=image, background="#d6e0f5")
            label.image = image
            label.grid(row=speler, column=stapel, padx=100, pady=40,
                       sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))
        else:
            frame = tk.Frame(
                master=window,
                relief=tk.RAISED,
                borderwidth=1,
            )
            frame.grid(row=speler, column=stapel, padx=5, pady=40, ipadx=40, ipady=80,
                       sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))

            label = tk.Label(master=frame, text="Speler {}\nStapel {}".format(speler, temp_stapel))
            label.pack(padx=5, pady=5)

run(tk.Tk(className=' Skip-Bo'), 1, 1, 0)
