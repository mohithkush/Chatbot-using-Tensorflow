from tkinter import *

BORDER_COLOR = "#E7D9EA"
BG_COLOR = "#343A40"
TEXT_COLOR = "#ECF4F3"

FONT = "Garamond 14"
FONT_BOLD = "Garamond 14 bold"

#Creating a Dimension using a Tkinter
root = Tk()
root.title("ChatBot")
root.geometry('470x550')
root.resizable(width=False, height=False)
root.configure(bg=BG_COLOR)

#Creating a Menu Bar
main_menu = Menu(root)
main_menu.add_command(label = "File")
main_menu.add_command(label = "Edit")
main_menu.add_command(label = "Quit")

root.config(menu = main_menu)

#Creating a Head Label
mylabel = Label(root, bg = BG_COLOR, fg = TEXT_COLOR, text = 'Hi,Welcome to our ChatBot!', font = FONT_BOLD, pady = 10)

#Creating a Border Line
Border = Label(root, width=450, bg=BORDER_COLOR)

#Creating a Chatwindow
Chatwindow = Text(root, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
Chatwindow.configure(cursor="arrow", state=DISABLED)

#Creating a Scrollbar
scrollbar = Scrollbar(Chatwindow)
scrollbar.configure(command=Chatwindow.yview)

#Creating a Bottom label
bottom_label = Label(root, bg=BORDER_COLOR, height=80)

#Creating a Message Window
Messagewindow = Text(bottom_label, bg="#222831", fg=TEXT_COLOR, font=FONT, insertbackground = 'White')


send_button = Button(bottom_label, text="Send", font=('Times',15), width=20, bg=BORDER_COLOR, activebackground = '#C6FFC1')


#Place all the components on the screen

mylabel.place(relwidth = 1)
Border.place(relwidth=1, rely=0.07, relheight=0.012)
Chatwindow.place(relheight=0.745, relwidth=1, rely=0.08)
scrollbar.place(relheight=1, relx=0.974)
bottom_label.place(relwidth=1, rely=0.825)
Messagewindow.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

root.mainloop()