#import tkinter
#root = tkinter.Tk(  )
#for r in range(3):
#   for c in range(4):
#      tkinter.Label(root, text='R%s/C%s'%(r,c),
#         borderwidth=10 ).grid(row=r,column=c)
#root.mainloop(  )
from tkinter import *

root = Tk()

for r in range(5,10):
    for c in range(0, 5):
        cell = Entry(root, width=10)
        cell.grid(row=r, column=c)
        cell.insert(10, '{}, {}'.format(r, c))

root.mainloop()
