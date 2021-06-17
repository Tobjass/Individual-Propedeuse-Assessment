import tkinter as tk

window = tk.Tk()

for speler in range(1, 3):
    window.rowconfigure(speler, weight=1, minsize=50)

    for stapel in range(1, 6):
        window.columnconfigure(stapel, weight=1, minsize=75)
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=1
        )
        frame.grid(row=speler, column=stapel, padx=100 if (stapel == 1) else 5, pady=40, ipadx=40, ipady=80,
                   sticky="n" if (speler == 1) else "s")

        label = tk.Label(master=frame, text="Speler {}\nStapel {}".format(speler, stapel))
        label.pack(padx=5, pady=5)

window.mainloop()
