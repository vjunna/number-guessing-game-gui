import tkinter as tk
from tkinter import ttk
import sqlite3
import random
import gamedb

root = tk.Tk()
root.geometry("800x500")
root.configure(bg='#213A5C')
root.columnconfigure([0, 7], weight=1)
root.rowconfigure([0, 9], weight=1)

class difficulty:
    def easy(self):
        self.num_set = random.randint(0, 9)
        self.reward = 5
        self.count = 7
    def normal(self):
        self.num_set = random.randint(0, 15)
        self.reward = 15
        self.count = 8
    def hard(self):
        self.num_set = random.randint(0, 20)
        self.reward = 30
        self.count = 9
d = difficulty()  # Initializing class for Difficulty levels

def clear():
    userNumGuess.delete(0, "end")

def clearResLabel():
    try:
        if resLabelReTry.winfo_exists():
            print("Line 33: clear resLabel")
            resLabelReTry.grid_forget()
    except:
        pass

def gameStatusScreen(res):
    global userWinLabel, userLostLabel
    if res == "WIN":
        try:
            userNumGuess.grid_forget()
            guessSubmit.grid_forget()
            print("win")
            userWinLabel = tk.Label(guessScreen, text='You won the game ! ! ! \n\n\n Select difficulty level to play again', bg='#213A5C', fg='white', font='Raleway 14 bold')
            userWinLabel.grid(column=0, row=3, columnspan=4)
            gamedb.updateUserDB(userName, d.reward, 'win')
            updateProfileFrame()
            clearResLabel()
        except NameError as err:
            pass
    else:
        try:
            userNumGuess.grid_forget()
            guessSubmit.grid_forget()
            userLostLabel = tk.Label(guessScreen, text='Ahhh! You Lost!!! \n\n Select difficulty level to try \nyour luck again', bg='#213A5C', fg='white', font='Raleway 14 bold')
            userLostLabel.grid(column=0, row=3, columnspan=4)
            clearResLabel()
            gamedb.updateUserDB(userName, d.reward, 'lost')
            updateProfileFrame()
        except:
            pass

def userGuessSubmit():
    if d.count > 0:
        userEntry = userNumGuess.get()
        userNum = int(userNumGuess.get())
        print(f"User Entry: {userNum}")
        if d.num_set == userNum:
            gameStatusScreen('WIN')
        else:
            global resLabelReTry
            clearResLabel()
            resLabelReTry = tk.Label(guessScreen, text=f"Retry.\nThe number {userEntry} is incorrect.\nTries remaining: {d.count - 1}", bg='#213A5C', fg='white', font='Raleway 14 bold')
            resLabelReTry.grid(column=0, row=5, columnspan=4)
            d.count = d.count - 1
            clear()
            print("Try Again")
    else:
        try:
            clearResLabel()
            gameStatusScreen('LOST')
        except:
            pass

# A frame for the Play Screen
playScreen = tk.Frame(root, height=400, width=400, bg='#213A5C')

def playScreenFrame():
    playScreen.grid(column=2, row=1, columnspan=4, rowspan=9, sticky='NEWS')
    playScreen.grid_propagate(False)   # Stop frame from shrinking
    playScreen.grid_columnconfigure([0, 3], weight=1)
    playScreen.grid_rowconfigure([0, 4], weight=1)
    userPlayStr = "Please choose the difficulty level \n under Game Options to start playing."
    userPlay = tk.Label(playScreen, text=userPlayStr, font='Raleway 12', bg='#213A5C', fg="white")
    userPlay.grid(column=0, row=3, columnspan=4)

# User Name Submit Function

def userNameSubmit():
    global userName
    userName = loginEntry.get()
    gamedb.createGameDB(userName)
    gamedb.userValidation(userName)
    if gamedb.userRes == None:
        gamedb.createNewUser(userName)
    gamedb.userProfileDB(userName)
    loginScreen.grid_forget()
    loginScreenTitle.grid_forget()
    inGameScreenTitleFrame()
    playScreenFrame()
    userProfileFrame()
    diffSelectFrame()

# Login Screen Title Frame
loginScreenTitle = tk.Frame(root, bg='black')
loginScreenTitle.grid(column=2, row=0, columnspan=6, sticky='NEWS')
loginScreenTitle.columnconfigure(0, weight=1)
loginScreenTitle.rowconfigure(0, weight=1)
loginScreenLabel = tk.Label(loginScreenTitle, text='Number Guessing Game', bg='black', fg='white', font=('Raleway 24 bold'))
loginScreenLabel.grid(column=0, row=0)

# In game Title
def inGameScreenTitleFrame():
    inGameScreenTitle = tk.Frame(root, bg='black')
    inGameScreenTitle.grid(column=2, row=0, columnspan=4, sticky='NEWS')
    inGameScreenTitle.columnconfigure(0, weight=1)
    inGameScreenTitle.rowconfigure(0, weight=1)
    userWelcome = tk.Label(inGameScreenTitle, text=f"Welcome, {userName}", font='Raleway 22 bold', bg='black', fg="white")
    userWelcome.grid(column=0, row=0, columnspan=4)

# Login Screen
loginScreen = tk.Frame(root, height=400, width=600, bg='#213A5C')
loginScreen.grid(column=2, row=1, columnspan=6, rowspan=9, sticky='NEWS')
loginScreen.grid_propagate(False)  # Stop frame from shrinking
loginScreen.columnconfigure([0, 5], weight=1)
loginScreen.rowconfigure([0, 3], weight=1)
loginTitle = tk.Label(loginScreen, text="Lets play the numbers game", font='Raleway 22 bold', bg='#213A5C', fg="white")
loginTitle.grid(column=0, row=0, columnspan=6)
loginLabel = tk.Label(loginScreen, text="Please enter your first name:", font='Raleway 16', bg='#213A5C', fg="white")
loginLabel.grid(column=0, row=1, columnspan=6)
userNameEntry = tk.StringVar()
loginEntry = tk.Entry(loginScreen, textvariable=userNameEntry, bg='white', fg="black")
loginEntry.grid(column=0, row=2, columnspan=6)
loginSubmit = tk.Button(loginScreen, text="Submit", command=userNameSubmit, bg='#213A5C', fg="white")
loginSubmit.grid(column=0, row=3, columnspan=6)

# Play Game Function
guessScreen = tk.Frame(root, height=400, width=400, bg='#213A5C')

def guessFunc():
    global userNumGuess, guessSubmit
    guessScreen.grid(column=2, row=1, columnspan=4, rowspan=9, sticky='NEWS')
    guessScreen.grid_propagate(False)   # Stop frame from shrinking
    guessScreen.columnconfigure([0, 3], weight=1)
    guessScreen.rowconfigure([0, 6], weight=1)
    playScreen.grid_forget()
    userNumEntry = tk.StringVar()
    userNumGuess = tk.Entry(guessScreen, textvariable=userNumEntry, bg='white', fg="black")
    userNumGuess.grid(column=0, row=2, columnspan=4, pady=10)
    guessSubmit = tk.Button(guessScreen, text="Guess", command=userGuessSubmit, bg='#213A5C', fg="white")
    guessSubmit.grid(column=0, row=4, columnspan=4, pady=10)

def rulesFrameFunc():
    rulesFrame = tk.Frame(root, height=500, width=200, bg='#000033')
    rulesFrame.grid(column=0, row=0, rowspan=10, columnspan=2, sticky='NEWS')
    rulesFrame.columnconfigure([0, 1], weight=1)
    rulesFrame.rowconfigure([0, 9], weight=1)
    rulesLabel0 = tk.Label(rulesFrame, text="How to Play:", bg='#000033', fg='white', font="Raleway 18 bold")
    rulesLabel0.grid(column=0, row=0, columnspan=2, pady=0)
    rulesLabel1 = tk.Label(rulesFrame, text="Try your luck by\n guessing the correct \nnumber.", bg='#000033', fg='#CCFF00', font="Raleway 10")
    rulesLabel1.grid(column=0, row=1, columnspan=2)
    rulesLabel2 = tk.Label(rulesFrame, text="Tries \n and rewards depend \n on the difficulty level", bg='#000033', fg='#CCFF00', font="Raleway 10")
    rulesLabel2.grid(column=0, row=2, columnspan=2)
    easyLabelFrame = tk.LabelFrame(rulesFrame, text="Easy: ", bg='#000033', fg='white', font="Raleway 10")
    easyLabelFrame.grid(column=0, row=4, columnspan=2)
    easyLabel = tk.Label(easyLabelFrame, bg='#000033', fg='white', text="Num Range:  0 to 9\nCoins: 5\nTries: 7")
    easyLabel.grid(column=0, row=4)
    normalLabelFrame = tk.LabelFrame(rulesFrame, text="Normal: ", bg='#000033', fg='white', font="Raleway 10")
    normalLabelFrame.grid(column=0, row=5, columnspan=2)
    normalLabel = tk.Label(normalLabelFrame, bg='#000033', fg='white', text="Num Range: 0 to 15\nCoins: 15\nTries: 8")
    normalLabel.grid(column=0, row=5)
    hardLabelFrame = tk.LabelFrame(rulesFrame, text="Hard: ", bg='#000033', fg='white', font="Raleway 10")
    hardLabelFrame.grid(column=0, row=6, columnspan=2)
    hardLabel = tk.Label(hardLabelFrame, bg='#000033', fg='white', text="Num Range: 0 to 20\nCoins: 30\nTries: 9")
    hardLabel.grid(column=0, row=6)

rulesFrameFunc()  # Initializing frame for rules

def updateProfileFrame():
    gamedb.userProfileDB(userName)
    # for i in range(len(profileStats)):
    #     statsLabel = 'labelStats' + pLabelName[i]
    #     statsLabel.config(text = f'{profileStats[i]}')
    # profileStats = [db.userName, db.userCoins, db.userWins, db.userLost, db.userLevel]
    # profileLabels = ['Username :', 'Coins :', 'Wins :', 'Lost :', 'Level :']

    labelStatsUsername.config(text=userName)
    labelStatsCoins.config(text=gamedb.userCoins)
    labelStatsWins.config(text=gamedb.userWins)
    labelStatsLost.config(text=gamedb.userLost)
    labelStatsLevel.config(text=gamedb.userLevel)
    gamedb.updateUserlevel(userName)

###### User Profile Frame #######
def createProfileLabels():
    for i in range(len(profileLabels)):
        curLabel = 'label' + pLabelName[i]
        curLabel = tk.Label(userFrame, text=profileLabels[i], bg='#000033', fg='white', font='Raleway 12')
        curLabel.grid(column=0, row=i + 1, sticky='E', padx=10)
    # for i in range(len(profileStats)):
    #     statsLabel = 'labelStats' + pLabelName[i]
    #     print(f"{statsLabel} : {profileStats[i]}")
    #     statsLabel = tk.Label(userFrame, text = profileStats[i], bg = '#000033', fg = 'white', font = 'Raleway 12')
    #     statsLabel.grid(column = 1, row = i + 1, sticky = 'W')

def userProfileFrame():
    gamedb.userProfileDB(userName)
    global profileLabels, profileStats, userFrame, pLabelName
    userFrame = tk.Frame(root, height=250, width=200, bg='#000033')
    userFrame.grid(column=6, row=0, columnspan=2, rowspan=5, sticky='NEWS')
    userFrame.grid_propagate(False)    # Stop frame from shrinking
    userFrame.columnconfigure([0, 1], weight=1)
    userFrame.rowconfigure([0, 6], weight=1)
    playerLabel = tk.Label(userFrame, text="Player Profile", bg='#000033', fg='white', font='Raleway 18 bold')
    playerLabel.grid(column=0, row=0, columnspan=2)
    profileLabels = ['Username :', 'Coins :', 'Wins :', 'Lost :', 'Level :']
    pLabelName = ['Username', 'Coins', 'Wins', 'Lost', 'Level']
    profileStats = [userName, gamedb.userCoins, gamedb.userWins, gamedb.userLost, gamedb.userLevel]
    createProfileLabels()

    global labelStatsUsername, labelStatsCoins, labelStatsWins, labelStatsLost, labelStatsLevel
    labelStatsUsername = tk.Label(userFrame, text=userName, bg='#000033', fg='white', font='Raleway 12')
    labelStatsUsername.grid(column=1, row=1, sticky='W', padx=10)
    labelStatsCoins = tk.Label(userFrame, text=gamedb.userCoins, bg='#000033', fg='white', font='Raleway 12')
    labelStatsCoins.grid(column=1, row=2, sticky='W', padx=10)
    labelStatsWins = tk.Label(userFrame, text=gamedb.userWins, bg='#000033', fg='white', font='Raleway 12')
    labelStatsWins.grid(column=1, row=3, sticky='W', padx=10)
    labelStatsLost = tk.Label(userFrame, text=gamedb.userLost, bg='#000033', fg='white', font='Raleway 12')
    labelStatsLost.grid(column=1, row=4, sticky='W', padx=10)
    labelStatsLevel = tk.Label(userFrame, text=gamedb.userLevel, bg='#000033', fg='white', font='Raleway 12')
    labelStatsLevel.grid(column=1, row=5, sticky='W', padx=10)

# A Frame for Difficulty Selection
def delResLabels():
    try:
        if userWinLabel.winfo_exists(): 
            print("A1")
            userWinLabel.grid_forget()       
    except NameError as err:
        print(err)
    try:
        if userLostLabel.winfo_exists(): 
            print("A1")
            userLostLabel.grid_forget()        
    except NameError as err:
        print(err)

def playGame():
    delResLabels()
    diff_select = diffLevel.get()
    diffLabel = tk.Label(diffFrame)
    diffLabel.grid(column=0, row=5, columnspan=2, pady=10)
    if diff_select == "easy":
        diffLabel.config(text=f"Level: {diff_select}", bg='white', fg='black')
        d.easy()
        guessFunc()
    if diff_select == "normal":
        diffLabel.config(text=f"Level: {diff_select}", bg='#9b59b6')
        d.normal()
        guessFunc()
    if diff_select == "hard":
        diffLabel.config(text=f"Level: {diff_select}", bg='#9b59b6')
        d.hard()
        guessFunc()

def diffSelectFrame():
    global diffLevel, diffFrame
    diffFrame = tk.Frame(root, height=250, width=200, bg='#000033')
    diffFrame.grid(column=6, row=5, columnspan=2, rowspan=5, sticky='NEWS')
    diffFrame.grid_propagate(False)  # Stop frame from shrinking
    diffFrame.columnconfigure([0, 1], weight=1)
    diffFrame.rowconfigure([0, 6], weight=1)
    diffFrameTitle = tk.Label(
        diffFrame, text="Game Options", bg='#000033', fg='white', font='Raleway 18 bold')
    diffFrameTitle.grid(column=0, row=0, columnspan=2)
    diffStr = tk.StringVar()
    diffLevel = ttk.Combobox(diffFrame, justify='center', width=12, background='#000033', foreground='#1a0600', textvariable=diffStr, values=["easy", "normal", "hard"])
    diffLevel.grid(column=0, row=2, columnspan=2, pady=10)
    diffLevel.set("Pick Difficulty")
    diffBtn = tk.Button(diffFrame, text="Select", command=playGame, bg='black', fg='red')
    diffBtn.grid(column=0, row=3, columnspan=2)

root.mainloop()
