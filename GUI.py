import tkinter as tk

def run(window, aantal_kaarten_hand):
    window.configure(background="#d6e0f5")

    for speler in range(1, 4):
        window.rowconfigure(speler, weight=1, minsize=50)

        stapels_aanmaken(window, speler, (6 + aantal_kaarten_hand if (speler != 2) else 6) if (speler < 3) else 1,
                         1 if (speler < 3) else (6 + aantal_kaarten_hand if (speler != 2) else 6), -1 if (speler < 3) else 1)

    window.mainloop()

def stapels_aanmaken(window, speler, start, stop, step):
    for stapel in range(start, stop, step):
        window.columnconfigure(stapel, weight=1, minsize=75)
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1,
        )
        frame.grid(row=speler, column=stapel, padx=100 if (stapel == 1 or stapel == 6) else 5, pady=40, ipadx=40, ipady=80, sticky="n" if (speler == 1) else (None if (speler == 2) else "s"))

        label = tk.Label(master=frame, text="Speler {}\nStapel {}".format(speler, 7 - stapel if (speler == 1) else stapel))
        label.pack(padx=5, pady=5)

run(tk.Tk(className=' Skip-Bo'), 1)
