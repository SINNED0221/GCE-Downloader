from tkinter import *

INGREDIENTS = ['cheese', 'ham', 'pickle', 'mustard', 'lettuce']


def print_ingredients(*args):
    values = [(ingredient, var.get()) for ingredient, var in data.items()]
    print(values)


data = {}  # dictionary to store all the IntVars

top = Tk()

mb = Menubutton(top, text="Ingredients", relief=RAISED)
mb.menu = Menu(mb, tearoff=0)
mb["menu"] = mb.menu

for ingredient in INGREDIENTS:
    var = IntVar()
    mb.menu.add_checkbutton(label=ingredient, variable=var)
    print(ingredient)
    data[ingredient] = var  # add IntVar to the dictionary

btn = Button(top, text="Print", command=print_ingredients)
btn.pack()

mb.pack()

top.mainloop()
