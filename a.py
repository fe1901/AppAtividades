import tkinter as tk
import tkinter.font as tkfont

root = tk.Tk()
font_families = list(tkfont.families())
root.destroy()

print("Fontes disponíveis no sistema:")
for f in font_families:
    print(f)