from tkinter import *
 
button_list = ['dummy']
class button_box :
    def __init__ (self, button, ID_number) :
        self.ID_number = ID_number
        self.button = button
 
    def clicked (self, event) :
        print (f'You pressed button number {self.ID_number}')
 
root = Tk ()
 
button_number = 1
for y in range (5) :
    for x in range (9) :
        button = Button (width = 5, height = 3, text = button_number)
        button.config (relief = 'solid', borderwidth = 1)
        button.grid (row = y, column = x)
        button_list.append (button_box (button, button_number))
        button.bind ('<Button-1>', button_list[button_number].clicked)
        button_number += 1
 
mainloop ()