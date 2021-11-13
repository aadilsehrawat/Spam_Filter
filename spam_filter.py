# Importing all the modules we will need
from datetime import datetime
from os import remove
from tkinter.constants import ANCHOR, BOTTOM, E, END, NW, SUNKEN, TRUE, W
from nltk import tokenize
from nltk.chunk.util import accuracy
from nltk.util import pr, unweighted_minimum_spanning_tree
import pandas as pd
import string
import nltk
import tkinter as tk
import tkinter.messagebox as mb
import time
import datetime
import subprocess
from PIL import Image, ImageTk


# GUI Window
root = tk.Tk()
canvas = tk.Canvas(root, width=650, height=690)
canvas.pack(fill="both", expand=TRUE)
root.minsize(width=650, height=690)
root.maxsize(width=650, height=690)
root.iconbitmap('images/spamLogo.ico')
root.title("Simple Spam Filter")


global number
number=1

def comingSoon(function):
    mb.showinfo(function, "Application is still under build \nThis feature will be added soon !" )

def myFunc():
    pass

def appearance():
    pass

# Opening the LOG FILE from menu bar
def log_file():
    print("LOG FILE WAS OPENED")
    # subprocess.call('X://MY CODING/Python/InHousePractical/files/Log File.txt', shell=True)
    subprocess.call('files\Log File.txt', shell=True)

# Opening the DATASET FILE from menu bar
def ds_file():
    print("DATASET WAS OPENED")
    # subprocess.call('X://MY CODING/Python/InHousePractical/files/SampleSpamTextCollection.txt', shell=True)
    subprocess.call('files\SampleSpamTextCollection.txt', shell=True)


mainmenu = tk.Menu(root)
m1 = tk.Menu(mainmenu, tearoff=0)
m1.add_command(label="New File", command= lambda: comingSoon("New File"))
m1.add_command(label="Open File", command= lambda: comingSoon("Open File"))
m1.add_separator()
m1.add_command(label="Open Log File", command=log_file)
m1.add_command(label="Open Dataset", command=ds_file)
m1.add_separator()
m1.add_command(label="Save", command= lambda: comingSoon("Save File"))
m1.add_command(label="Save As", command= lambda: comingSoon("Save File As"))
m1.add_separator()
m1.add_command(label="Exit", command=quit)
root.config(menu=mainmenu)
mainmenu.add_cascade(label="File", menu=m1)

m2 = tk.Menu(mainmenu, tearoff=0)
m2.add_command(label="Help", command= lambda: comingSoon("Help"))
m2.add_separator()
m2.add_command(label="Rate us", command= lambda: comingSoon("Rate Us"))
m2.add_command(label="Suggestion", command= lambda: comingSoon("Suggestion"))
m2.add_separator()
m2.add_command(label="Exit", command=quit)
root.config(menu=mainmenu)
mainmenu.add_cascade(label="Options", menu=m2)

m3 = tk.Menu(mainmenu, tearoff=0)
m3.add_command(label="About", command= lambda: comingSoon("About"))
m3.add_command(label="Version Info", command= lambda: comingSoon("Version Info"))
m3.add_separator()
m3.add_command(label="Appearance", command= lambda: comingSoon("Appearance"))
m3.add_command(label="Discussion Forum", command= lambda: comingSoon("Discussion"))
m3.add_separator()
m3.add_command(label="Exit", command=quit)
root.config(menu=mainmenu)
mainmenu.add_cascade(label="Miscellaneous", menu=m3)


# Importing our Background
background = tk.PhotoImage(file="images/bg.png")


# Importing our NO-SPAM logo
logo = tk.PhotoImage(file="images/spamLogo.png")


# Reading the dataset (.csv file)
data = pd.read_csv("files/SampleSpamTextCollection.txt", sep="\t", header=None, names=['label', 'text'])


# Downloading updated stopwords and punctuations everytime the program is run
# To remove these later from the input as a part of pre processing
nltk.download('stopwords')
nltk.download('punkt')
stopwords = nltk.corpus.stopwords.words('english')
punctuation = string.punctuation


# Logic and code behind pre processing the data (input by the user)
def preProcess(text):
    lowercase = "".join([char.lower() for char in text if char not in punctuation])
    tokenize = nltk.tokenize.word_tokenize(lowercase)
    removeStopWords = [word for word in tokenize if word not in stopwords]
    return removeStopWords


# Adding a new column which contains the pre processed data
data['processed'] = data['text'].apply(lambda x: preProcess(x))


# Categorizing all the tokens (words) into spam or ham (not spam)
def categorize():
    spam_words = []
    ham_words = []

    # Counting total SPAM words
    for text in data['processed'][data['label']=='spam']:
        for word in text:
            spam_words.append(word) 
    
    # Counting total HAM words
    for text in data['processed'][data['label']=='ham']:
        for word in text:
            ham_words.append(word)
    
    return spam_words, ham_words

spam_words, ham_words = categorize()


# Simply checking the occurances of all words 
# To determine whether the input given by the user is a spam or ham
def predict(userInput):
    spamCount=0
    hamCount=0

    for word in userInput:
        spamCount+=spam_words.count(word)
        hamCount+=ham_words.count(word)

    print("=== RESULT ===")
    
    if spamCount<hamCount:
        # Calculating the accuracy of our filter for ham messages with this dataset
        accuracy = round((hamCount/(hamCount+spamCount))*100,2)
        check = f"The message is not SPAM with {accuracy}% certainity"
        print(check)
        r = 0
        return check,r,accuracy

    elif spamCount>hamCount:
        # Calculating the accuracy of our filter for spam messages with this dataset
        accuracy = round((spamCount/(hamCount+spamCount))*100,2)
        check = f" The message is a SPAM with {accuracy}% certainity "
        r = 1
        print(check)
        return check,r,accuracy

    else:
        check = f"          Could be a SPAM with 50% certainity         "
        print(check)
        r = "Undetermined"
        accuracy=0
        return check,r,accuracy


        
                        # GUI Starts from Here #  


# Opening statement of our log file:
# Inserting Session Details in our log file each time the program runs
session=datetime.datetime.now()
session="Session:     |" + session.strftime(f"  %d-%m-%y  | %H:%M:%S")
with open("files/Log File.txt", "a") as file:
    file.write("___________________________________________\n\n")
    file.write(session+"\n")
    file.write("LABEL        | CERTAINITY | USER-INPUT-TEXT\n\n")


# Displaying our imported background
canvas.create_image(0,0, image=background, anchor=NW)


# Displaying our imported logo
canvas.create_image(225,40, image=logo, anchor=NW)


# Instructions to user
canvas.create_text(325,300, text="Input a text, to check whether it's a SPAM or HAM (not spam):", font="Arial 11 bold", fill="white")


# Storing User Input text to check whether spam or ham
user_text_value = tk.StringVar()
text_box = tk.Text(root, height=3, width=50, padx=15, pady=15, font="Calibri")
text_box.tag_configure("center", justify="left")
text_box.tag_add("center", 1.0, "end")
canvas.create_window(111,333, anchor=NW, window=text_box)


# Function to invoke when user presses the "Check" button
# This further calls all the spam filter functions in their order of occurances
def checkSpam():
    user_text_value = text_box.get(1.0, 'end')
    statusvar.set(" Checking... |")
    sbar.update()

    if user_text_value!="\n":
        processedInput = preProcess(user_text_value)
        check,result,accuracy=predict(processedInput)

        if result==0:
            displayResult=tk.Label(text=check, font=26, fg="#118811", padx=10, pady=5, relief=SUNKEN)
            canvas.create_window(150,565, anchor=NW, window=displayResult)
            accuracy='%.2f'%accuracy
            with open("files/Log File.txt", "a") as file:
                file.write(f"Not Spam     |   {accuracy}    | {user_text_value}")

        elif result==1:
            displayResult=tk.Label(text=check, font=26, fg="#DD1010", padx=10, pady=5, relief=SUNKEN)
            canvas.create_window(149,565, anchor=NW, window=displayResult)
            accuracy='%.2f'%accuracy
            with open("files/Log File.txt", "a") as file:
                file.write(f"Spam         |   {accuracy}    | {user_text_value}")
    
        else:
            displayResult=tk.Label(text=check, font=26, padx=10, pady=5, relief=SUNKEN)
            canvas.create_window(150,565, anchor=NW, window=displayResult)
            accuracy=50
            accuracy='%.2f'%accuracy
            with open("files/Log File.txt", "a") as file:
                file.write(f"Undetermined |   {accuracy}    | {user_text_value}")

    else:
        displayResult=tk.Label(text="!!! Text Box is Empty, Please Input a Valid Text !!!" , font=26, padx=10, pady=5, relief=SUNKEN)
        canvas.create_window(148,565, anchor=NW, window=displayResult)

    time.sleep(0.5)
    statusvar.set(" Ready\t   |\t\t\t\t\t\t\t           Last Search = 0.5 seconds")


# Check Button which calls a funciton 
# Which further calls all the spam filter functions in their order of occurances
checkButton = tk.Button(root, text="Check", command=lambda:checkSpam(), font="Raleway", bg="#20bebe", fg="white", height=2, width=15)
canvas.create_window(253,453, anchor=NW, window=checkButton)


# Status Bar
statusvar = tk.StringVar()
statusvar.set(" Ready\t   |")
sbar = tk.Label(canvas, textvariable=statusvar, bd=1, relief=SUNKEN, anchor=W)
sbar.pack(side=BOTTOM, fill="x")

root.mainloop()

# Closing statement of our log file as "***SESSION EXPIRED***"
with open("files/Log File.txt", "a") as file:
    file.write("\n         ***SESSION EXPIRED***\n\n")
