from tkinter import *
import twitter_account
import Utils

root = Tk()

label_words = Label(root, text = "Words")
label_place = Label(root, text = "Place")
label_lat = Label(root, text = "Latitude")
label_long = Label(root, text = "Longitude")

entry_words = Entry(root)
entry_lat = Entry(root)
entry_long = Entry(root)

# ORGANIZE
label_words.grid(row = 0, sticky = E) # column defualt = 0, E=align to east...
label_place.grid(row = 1) # column defualt = 0
label_lat.grid(row=2, column = 1)
label_long.grid(row=3, column=1)

entry_words.grid(row = 0, column = 1)
entry_lat.grid(row = 2, column = 2)
entry_long.grid(row = 3, column = 2)

def create():

    b = twitter_account()


button1 = Button(root, text = "Search", command= create)
button1.grid(row = 4, column = 1)

#check box
c = Checkbutton(root, text="Keep me logged in")
c.grid(columnspan = 2) # put it in the center of the two firrst columns

root.mainloop()