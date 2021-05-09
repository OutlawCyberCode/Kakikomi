import tkinter
import requests
import json
import pathlib
import time
import threading
import ctypes
myappid = 'ModernEra.Kakikomi'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

animeName = ""
characterName = ""
secondsPassed = 0
timerBool = False

def getQuote():
    global animeName, characterName
    r = requests.get('https://animechan.vercel.app/api/random')
    pathlib.Path('data.json').write_bytes(r.content)
    with open('data.json') as f:
        data = json.load(f)
    animeName = data["anime"]
    characterName = data["character"]
    return data["quote"]

def nextPress():
    global timerBool
    global secondsPassed
    secondsPassed = 0

    prompt.configure(text=getQuote())
    secondsTook.configure(text="")
    wordsPerMinuteLabel.configure(text="")
    animeInfoLabel.configure(text="")
    textInput.delete('1.0', tkinter.END)

    timerBool = True
    thread = threading.Thread(target=timer)
    thread.start()

def timer():
    global timerBool
    global secondsPassed
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
    wordsPerMinute = amountOfWords / (secondsPassed / 60)

    if text == prompt['text']:
        prompt.configure(text="Exact match! Good job!")
    else:
        prompt.configure(text="Something's wrong! Better luck next time.")
    timerBool = False
    secondsTook.configure(text="Time in Seconds: " + str(secondsPassed))
    wordsPerMinuteLabel.configure(text="Words Per Minute: " + str(wordsPerMinute))
    animeInfoLabel.configure(text="Quote is from \"" + animeName + "\", spoken by " + characterName)
    textInput.delete('1.0', tkinter.END)

def countWords(passage):
    wordCount = 0
    for char in passage:
        if char == " ":
            wordCount += 1
    return wordCount
    
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
    animeInfoLabel = tkinter.Label(gui, background="black", foreground="white", font=("Arial", 16))

    textInput = tkinter.Text(gui, height=2, width=50, font=("Arial", 16), wrap="word")

    checkButton = tkinter.Button(gui, text="Check!", font=("Arial", 16), fg="white", bg="grey", command=lambda: checkInput())
    nextButton = tkinter.Button(gui, text="Next!", font=("Arial", 16), fg="white", bg="grey", command=lambda: nextPress())

    prompt.pack(pady=20)
    textInput.pack()
    checkButton.pack(pady=20)
    nextButton.pack(pady=10)
    secondsTook.pack(pady=5)
    wordsPerMinuteLabel.pack(pady=5)
    animeInfoLabel.pack()

    gui.mainloop()
