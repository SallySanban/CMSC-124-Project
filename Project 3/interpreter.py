import semantics_analyzer
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import tkinter.filedialog

symbolTable = semantics_analyzer.semantics()

BACKGROUND_COLOR = "#e0e0de"

def openFile():
    fileButton = ttk.Button(
        screen,
        text='Open File',
        command=lambda:print("open file")
    )
    fileButton.place(x=20, y=715)

def textEditor():
    textEditorLabel = ttk.Label(screen, text="Text Editor", background=BACKGROUND_COLOR)
    textEditorLabel.place(x=20, y=20)
    textEditor = Listbox(screen, height=20, width=80, state=DISABLED)
    textEditor.place(x=20, y=40)

def listOfTokens():
    tokensLabel = ttk.Label(screen, text="Tokens", background=BACKGROUND_COLOR)
    tokensLabel.place(x=520, y=20)
    listOfTokens = Listbox(screen, height=20, width=53, state=DISABLED)
    listOfTokens.place(x=520, y=40)

def symbolTable():
    symbolTableLabel = ttk.Label(screen, text="Symbol Table", background=BACKGROUND_COLOR)
    symbolTableLabel.place(x=855, y=20)
    listOfSymbolTable = Listbox(screen, height=20, width=53, state=DISABLED)
    listOfSymbolTable.place(x=855, y=40)

def console():
    symbolTableLabel = ttk.Label(screen, text="Symbol Table", background=BACKGROUND_COLOR)
    symbolTableLabel.place(x=20, y=380)
    listOfSymbolTable = Listbox(screen, height=20, width=192, state=DISABLED)
    listOfSymbolTable.place(x=20, y=380)

def run():
    runButton = ttk.Button(
        screen,
        text='Run',
        command=lambda:print("run")
    )
    runButton.place(x=1100, y=715)

#MAIN
screen = Tk()
screen.title('LOLCODE Interpreter')
screen.geometry("1200x750")
screen.configure(bg=BACKGROUND_COLOR)
screen.resizable(False, False)

style = ttk.Style()
style.theme_use('vista')

openFile()
textEditor()
listOfTokens()
symbolTable()
console()
run()

screen.mainloop()