import tkinter
import requests
import json
import pathlib
import time
import threading
import ctypes
import random
# api key: AIzaSyC-bYybFpAqDzuetDfKsOXBAPN_wd35HiU
# search engine id: 03f3be69e01592eca




myappid = 'ModernEra.Kakikomi'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

animeName = ""
characterName = ""
secondsPassed = 0
timerBool = False

def getQuote():
    prompts = ["Quantum Theory", "Algebra", "Video Game", "VSCode", "Python", "Programming Language","Life", "The meaning of life", "The first theorum of calculus", "The second theorum of calculus", "The first law of thermodynamics", "The second law of thermodynamics"]
    prompt = random.choice(prompts)+" definition"
    data = requests.get(f"https://www.googleapis.com/customsearch/v1?key=AIzaSyC-bYybFpAqDzuetDfKsOXBAPN_wd35HiU&cx=03f3be69e01592eca&q={prompt}")
    return data.json()['items'][random.randint(0,9)]['snippet']

def nextPress():
    global timerBool
    global secondsPassed
    secondsPassed = 0

    prompt.configure(text=getQuote())
    secondsTook.configure(text="")
    wordsPerMinuteLabel.configure(text="")
    WPMLabel.configure(text="")
    textInput.delete('1.0', tkinter.END)

    timerBool = True
    thread = threading.Thread(target=timer)
    thread.start()

def timer():
    global timerBool
    global secondsPassed
    time.sleep(2)
    while timerBool:
        secondsPassed += 1
        time.sleep(1)    

def checkInput():
    global secondsPassed, timerBool, animeName, characterName
    text = textInput.get("1.0", "end-1c")
    print(prompt['text'])
    print("\n")
    print(text)

    amountOfWords = countWords(prompt['text'])
    wordsPerMinute = round(amountOfWords / (secondsPassed / 60), 2)

    if text == prompt['text']:
        prompt.configure(text="Exact match! Good job!")
    else:
        prompt.configure(text="Something's wrong! Better luck next time.")
    timerBool = False
    secondsTook.configure(text="Time in Seconds: " + str(secondsPassed))
    wordsPerMinuteLabel.configure(text="Words Per Minute: " + str(wordsPerMinute))
    WPMLabel.configure(text=["You are absolutely garbage","You are still bad", "You are under average", "You are around average", "You might be average", "You are probably average", "You are bad but are probably average", "You are average", "You are above average... I think", "Please complete the Captcha", "You have been banned for botting."][round(wordsPerMinute//10)])
    textInput.delete('1.0', tkinter.END)

def countWords(passage):
    return len(passage.split(" "))
    
if __name__ == "__main__":
    gui = tkinter.Tk()
    gui.configure(background="black")
    gui.title("Kakikomi")
    gui.iconphoto(False, tkinter.PhotoImage(file="icon.png"))
    gui.geometry("800x550")

    prompt = tkinter.Label(gui, text = "Press 'Next!' button to start!", wraplengt=700)
    prompt.configure(background="black", foreground="white", font=("Arial", 16))
    secondsTook = tkinter.Label(gui, background="black", foreground="white", font=("Arial", 16))
    wordsPerMinuteLabel = tkinter.Label(gui, background="black", foreground="white", font=("Arial", 16))
    WPMLabel = tkinter.Label(gui, background="black", foreground="white", font=("Arial", 16))

    textInput = tkinter.Text(gui, height=2, width=50, font=("Arial", 16), wrap="word")

    checkButton = tkinter.Button(gui, text="Check!", font=("Arial", 16), fg="white", bg="grey", command=lambda: checkInput())
    nextButton = tkinter.Button(gui, text="Next!", font=("Arial", 16), fg="white", bg="grey", command=lambda: nextPress())

    prompt.pack(pady=20)
    textInput.pack()
    checkButton.pack(pady=20)
    nextButton.pack(pady=10)
    secondsTook.pack(pady=5)
    wordsPerMinuteLabel.pack(pady=5)
    WPMLabel.pack()

    gui.mainloop()
