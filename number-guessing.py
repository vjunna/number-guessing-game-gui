import tkinter as tk
from tkinter import ttk
import sqlite3
import random

root = tk.Tk()
root.geometry("800x500")
root.configure(bg = '#213A5C')
root.columnconfigure([0,7], weight = 1)
root.rowconfigure([0,9], weight = 1)

class difficulty:    
    def easy(self):
        self.num_set = random.randint(0,9)
        self.reward = 5
        self.count = 7    
    def normal(self):
        self.num_set = random.randint(0,15)
        self.reward = 15
        self.count = 8
    def hard(self):
        self.num_set = random.randint(0,20)
        self.reward = 30
        self.count = 9
d = difficulty() #Initializing class for Difficulty levels

class userDB: 
    def createGameDB(self):
        try:
            dbConnectObject = sqlite3.connect('game.db')
            dbCursorObject = dbConnectObject.cursor()
            usersTable = 'CREATE TABLE  IF NOT EXISTS users (playerID INTEGER PRIMARY KEY NOT NULL, username str NOT NULL UNIQUE, usercoins INTEGER, userwins INTEGER, userlost INTEGER, userlevel INTEGER);'
            dbCursorObject.execute(usersTable)
            dbConnectObject.commit()
            dbConnectObject.close()
        except ValueError as err:
            # print('err')
            pass
        finally:
            if dbConnectObject:
               dbConnectObject.close()            
    def createNewUser(self):
        dbConnectObject = sqlite3.connect('game.db')
        dbCursorObject = dbConnectObject.cursor()
        userCreate = f"INSERT INTO users (username, usercoins, userwins, userlost, userlevel) VALUES ('{userNameGet}', 50, 0, 0, 0);"
        dbCursorObject.execute(userCreate)
        dbConnectObject.commit()
        dbConnectObject.close()    
    def userValidation(self):      
        dbConnectObject = sqlite3.connect('game.db')
        dbCursorObject = dbConnectObject.cursor()
        print(userNameGet)
        userQuery = f"SELECT * from users WHERE username = '{userNameGet}'"
        dbCursorObject.execute(userQuery)
        userRes = dbCursorObject.fetchone()
        dbConnectObject.close()
        if userRes is None:
            db.createNewUser()
    def userProfile(self):
        dbConnectObject = sqlite3.connect('game.db')
        dbCursorObject = dbConnectObject.cursor()
        userQuery = f"SELECT playerID, username, usercoins, userwins, userlost, userlevel from users WHERE username = '{userNameGet}'"
        dbCursorObject.execute(userQuery)
        userRes = dbCursorObject.fetchall()
        for i in userRes:
            self.playerID = i[0]
            self.userName = i[1]
            self.userCoins = i[2]
            self.userWins = i[3]
            self.userLost = i[4]
            self.userLevel = i[5]
        dbConnectObject.close()
    def updateUser(self, gameResult):
        self.gameResult = gameResult     
        dbConnectObject = sqlite3.connect('game.db')
        dbCursorObject = dbConnectObject.cursor()
        #Updating Wins and losses to database
        if gameResult == 'win':
            updateWinsQuery = f"UPDATE users SET usercoins = ({db.userCoins} + {d.reward}), userwins = ({db.userWins + 1}) WHERE username = '{userNameGet}'"
            dbCursorObject.execute(updateWinsQuery)    
        elif gameResult == 'lost':
            updateLostQuery = f"UPDATE users SET userlost = ({db.userWins} + 1) WHERE username = '{userNameGet}'"
            dbCursorObject.execute(updateLostQuery)
        else: 
            pass     
        dbConnectObject.commit()
        dbConnectObject.close()
    def updateUserlevel(self): # Updating user level
        db.userValidation()
        dbConnectObject = sqlite3.connect('game.db')
        dbCursorObject = dbConnectObject.cursor()
        if db.userCoins > 55 and db.userCoins <= 70:
            l1 = updateLevelQuery = f"UPDATE users SET userlevel = 1 WHERE username = '{userNameGet}'"
            dbCursorObject.execute(l1)
        elif db.userCoins > 80 and db.userCoins <= 100:
            l2 = updateLevelQuery = f"UPDATE users SET userlevel = 2 WHERE username = '{userNameGet}'"
            dbCursorObject.execute(l2)
        elif db.userCoins > 100 and db.userCoins <= 125:
            l3 = updateLevelQuery = f"UPDATE users SET userlevel = 3 WHERE username = '{userNameGet}'"
            dbCursorObject.execute(l3)
        elif db.userCoins > 125 and db.userCoins <= 175:
            l4 = updateLevelQuery = f"UPDATE users SET userlevel = 4 WHERE username = '{userNameGet}'"
            dbCursorObject.execute(l4)
        elif db.userCoins > 175 and db.userCoins <= 250:
            l5 = updateLevelQuery = f"UPDATE users SET userlevel = 5 WHERE username = '{userNameGet}'"
            dbCursorObject.execute(l5)
        elif db.userCoins > 250 and db.userCoins <= 350:
            l6 = updateLevelQuery = f"UPDATE users SET userlevel = 6 WHERE username = '{userNameGet}'"
            dbCursorObject.execute(l6)
        else:
            l0 = updateLevelQuery = f"UPDATE users SET userlevel = 0 WHERE username = '{userNameGet}'"
            dbCursorObject.execute(l0)

        dbConnectObject.commit()
        dbConnectObject.close()
        
db = userDB()    # Initialising userDB class

def clear():
    userNumGuess.delete(0, "end")
def clearResLabel():
    try:
        if resLabelReTry.winfo_exists():
            resLabelReTry.grid_forget()
    except:
        pass   
def gameStatusScreen(res):
    global userWin, userLost
    if res == "WIN":
        try:
            userNumGuess.grid_forget()
            guessSubmit.grid_forget()
            print("win")
            userWin = tk.Label(guessScreen, text = 'You won the game ! ! ! \n\n\n Select difficulty level to play again', bg = '#213A5C', fg = 'white', font = 'Raleway 14 bold')
            userWin.grid(column = 0, row = 3, columnspan = 4)
            db.updateUser('win')
            updateProfile()
            clearResLabel()
        except NameError as err:
            pass
    else:
        try:
            userNumGuess.grid_forget()
            guessSubmit.grid_forget()
            userLost = tk.Label(guessScreen, text = 'Ahhh! You Lost!!! \n\n Select difficulty level to try \nyour luck again', bg = '#213A5C', fg = 'white', font = 'Raleway 14 bold')
            userLost.grid(column = 0, row = 3, columnspan = 4)
            clearResLabel()
            db.updateUser('lost')
            updateProfile()
            print("Lost")
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
            resLabelReTry = tk.Label(guessScreen, text = f"Retry.\nThe number {userEntry} is incorrect.\nTries remaining: {d.count - 1}", bg = '#213A5C', fg = 'white', font = 'Raleway 14 bold')
            resLabelReTry.grid(column = 0, row = 5, columnspan = 4)
            d.count = d.count -1
            clear()    
            print("Try Again")    
    else:
        try: 
            clearResLabel()
            gameStatusScreen('LOST') 
        except:
            pass

#A frame for the Play Screen
playScreen = tk.Frame(root, height = 400, width = 400, bg = '#213A5C')
def playScreenFrame():
    playScreen.grid(column = 2, row = 1, columnspan = 4, rowspan = 9, sticky = 'NEWS')
    playScreen.grid_propagate (False)   # Stop frame from shrinking
    playScreen.grid_columnconfigure([0,3], weight = 1)
    playScreen.grid_rowconfigure([0,4], weight = 1)
    userPlayStr = "Please choose the difficulty level \n under Game Options to start playing."
    userPlay = tk.Label(playScreen, text = userPlayStr, font = 'Raleway 12', bg = '#213A5C', fg = "white")
    userPlay.grid(column = 0, row = 3, columnspan = 4)

# User Name Submit Function
def userNameSubmit():
    global userNameGet
    userNameGet = loginEntry.get()
    db.createGameDB()
    db.userValidation()
    db.userProfile()
    loginScreen.grid_forget()
    loginScreenTitle.grid_forget()
    inGameScreenTitleFrame()
    playScreenFrame()
    userProfileFrame()
    diffSelectFrame()
    
# Login Screen Title Frame
loginScreenTitle = tk.Frame(root, bg = 'black')
loginScreenTitle.grid(column = 2, row = 0, columnspan = 6, sticky = 'NEWS')
loginScreenTitle.columnconfigure(0, weight = 1)
loginScreenTitle.rowconfigure(0, weight = 1)
loginScreenLabel = tk.Label(loginScreenTitle, text = 'Number Guessing Game', bg = 'black', fg = 'white', font = ('Raleway 24 bold'))
loginScreenLabel.grid(column = 0, row = 0)

# In game Title
def inGameScreenTitleFrame():
    inGameScreenTitle = tk.Frame(root, bg = 'black')
    inGameScreenTitle.grid(column = 2, row = 0, columnspan = 4, sticky = 'NEWS')
    inGameScreenTitle.columnconfigure(0, weight = 1)
    inGameScreenTitle.rowconfigure(0, weight = 1)
    userWelcome = tk.Label(inGameScreenTitle, text = f"Welcome, {db.userName}", font = 'Raleway 22 bold', bg = 'black', fg = "white")
    userWelcome.grid(column = 0, row = 0, columnspan = 4)

# Login Screen
loginScreen = tk.Frame(root, height = 400, width = 600, bg = '#213A5C')
loginScreen.grid(column = 2, row = 1, columnspan = 6, rowspan = 9, sticky = 'NEWS')
loginScreen.grid_propagate (False)  # Stop frame from shrinking
loginScreen.columnconfigure([0,5], weight = 1)
loginScreen.rowconfigure([0,3], weight = 1)
loginTitle = tk.Label(loginScreen, text = "Lets play the numbers game", font = 'Raleway 22 bold', bg = '#213A5C', fg = "white")
loginTitle.grid(column = 0, row = 0, columnspan = 6)
loginLabel = tk.Label(loginScreen, text = "Please enter your first name:", font = 'Raleway 16', bg = '#213A5C', fg = "white")
loginLabel.grid(column = 0, row = 1, columnspan = 6)
userNameEntry = tk.StringVar()
loginEntry = tk.Entry(loginScreen, textvariable=userNameEntry, bg = 'white', fg = "black")
loginEntry.grid(column = 0, row = 2, columnspan = 6)
loginSubmit = tk.Button(loginScreen, text = "Submit", command = userNameSubmit , bg = '#213A5C', fg = "white")
loginSubmit.grid(column = 0, row = 3, columnspan = 6)

# Play Game Function
guessScreen = tk.Frame(root, height = 400, width = 400, bg = '#213A5C')
def guessFunc():
    guessScreen.grid(column = 2, row = 1, columnspan = 4, rowspan = 9, sticky = 'NEWS')
    guessScreen.grid_propagate (False)   # Stop frame from shrinking
    guessScreen.columnconfigure([0,3], weight = 1)
    guessScreen.rowconfigure([0,6], weight = 1) 
    playScreen.grid_forget()
    userNumEntry = tk.StringVar()
    global userNumGuess
    userNumGuess = tk.Entry(guessScreen, textvariable=userNumEntry, bg = 'white', fg = "black")
    userNumGuess.grid(column = 0, row = 2, columnspan = 4, pady = 10)
    global guessSubmit
    guessSubmit = tk.Button(guessScreen, text = "Guess", command = userGuessSubmit , bg = '#213A5C', fg = "white")
    guessSubmit.grid(column = 0, row = 4, columnspan = 4, pady = 10)

def rulesFrameFunc():
    rulesFrame = tk.Frame(root, height = 500, width = 200, bg = '#000033')
    rulesFrame.grid(column = 0, row = 0, rowspan = 10, columnspan = 2, sticky = 'NEWS')
    rulesFrame.columnconfigure([0,1], weight = 1)
    rulesFrame.rowconfigure([0,9], weight = 1)
    rulesLabel0 = tk.Label(rulesFrame, text = "How to Play:", bg = '#000033', fg = 'white', font = "Raleway 18 bold")
    rulesLabel0.grid(column = 0, row = 0, columnspan = 2, pady = 0)
    rulesLabel1 = tk.Label(rulesFrame, text = "Try your luck by\n guessing the correct \nnumber.", bg = '#000033', fg = '#CCFF00', font = "Raleway 10")
    rulesLabel1.grid(column = 0, row = 1, columnspan = 2)
    rulesLabel2 = tk.Label(rulesFrame, text = "Tries \n and rewards depend \n on the difficulty level", bg = '#000033', fg = '#CCFF00', font = "Raleway 10")
    rulesLabel2.grid(column = 0, row = 2, columnspan = 2)
    easyLabelFrame = tk.LabelFrame(rulesFrame, text = "Easy: ", bg = '#000033', fg = 'white', font = "Raleway 10")
    easyLabelFrame.grid(column = 0, row = 4, columnspan = 2)
    easyLabel = tk.Label(easyLabelFrame, bg = '#000033', fg = 'white', text = "Num Range:  0 to 9\nCoins: 5\nTries: 7")
    easyLabel.grid(column = 0, row = 4)
    normalLabelFrame = tk.LabelFrame(rulesFrame, text = "Normal: ", bg = '#000033', fg = 'white', font = "Raleway 10")
    normalLabelFrame.grid(column = 0, row = 5, columnspan = 2)
    normalLabel = tk.Label(normalLabelFrame, bg = '#000033', fg = 'white', text = "Num Range: 0 to 15\nCoins: 15\nTries: 8")
    normalLabel.grid(column = 0, row = 5)
    hardLabelFrame = tk.LabelFrame(rulesFrame, text = "Hard: ", bg = '#000033', fg = 'white', font = "Raleway 10")
    hardLabelFrame.grid(column = 0, row = 6, columnspan = 2)
    hardLabel = tk.Label(hardLabelFrame, bg = '#000033', fg = 'white', text = "Num Range: 0 to 20\nCoins: 30\nTries: 9")
    hardLabel.grid(column = 0, row = 6)
rulesFrameFunc() # Initializing frame for rules

def updateProfile():
    db.userProfile()        
    # for i in range(len(profileStats)):
    #     statsLabel = 'labelStats' + pLabelName[i]
    #     statsLabel.config(text = f'{profileStats[i]}')
    # profileStats = [db.userName, db.userCoins, db.userWins, db.userLost, db.userLevel]
    # profileLabels = ['Username :', 'Coins :', 'Wins :', 'Lost :', 'Level :']
    
    labelStatsUsername.config(text = db.userName)
    labelStatsCoins.config(text = db.userCoins)
    labelStatsWins.config(text = db.userWins)
    labelStatsLost.config(text = db.userLost)
    labelStatsLevel.config(text = db.userLevel)
    db.updateUserlevel() 

###### User Profile Frame #######
def createProfileLabels(): 
    for i in range(len(profileLabels)):
        curLabel = 'label' + pLabelName[i]
        curLabel = tk.Label(userFrame, text = profileLabels[i], bg = '#000033', fg = 'white', font = 'Raleway 12')
        curLabel.grid(column = 0, row = i + 1, sticky = 'E', padx = 10)     
    # for i in range(len(profileStats)):
    #     statsLabel = 'labelStats' + pLabelName[i]  
    #     print(f"{statsLabel} : {profileStats[i]}")
    #     statsLabel = tk.Label(userFrame, text = profileStats[i], bg = '#000033', fg = 'white', font = 'Raleway 12')
    #     statsLabel.grid(column = 1, row = i + 1, sticky = 'W')

def userProfileFrame():
    global profileLabels, profileStats, userFrame, pLabelName
    userFrame = tk.Frame(root, height = 250, width = 200, bg = '#000033')
    userFrame.grid(column = 6, row = 0, columnspan = 2, rowspan = 5, sticky = 'NEWS')
    userFrame.grid_propagate (False)    # Stop frame from shrinking
    userFrame.columnconfigure([0,1], weight = 1)
    userFrame.rowconfigure([0,6], weight = 1)
    playerLabel = tk.Label(userFrame, text = "Player Profile", bg = '#000033', fg = 'white', font = 'Raleway 18 bold')
    playerLabel.grid(column = 0, row = 0, columnspan = 2) 
    profileLabels = ['Username :', 'Coins :', 'Wins :', 'Lost :', 'Level :']
    pLabelName = ['Username', 'Coins', 'Wins', 'Lost', 'Level']
    profileStats = [db.userName, db.userCoins, db.userWins, db.userLost, db.userLevel]
    createProfileLabels()
    
    global labelStatsUsername, labelStatsCoins, labelStatsWins, labelStatsLost, labelStatsLevel
    labelStatsUsername = tk.Label(userFrame, text = db.userName, bg = '#000033', fg = 'white', font = 'Raleway 12')
    labelStatsUsername.grid(column = 1, row = 1, sticky = 'W', padx = 10) 
    labelStatsCoins = tk.Label(userFrame, text = db.userCoins, bg = '#000033', fg = 'white', font = 'Raleway 12')
    labelStatsCoins.grid(column = 1, row = 2, sticky = 'W', padx = 10)
    labelStatsWins = tk.Label(userFrame, text = db.userWins, bg = '#000033', fg = 'white', font = 'Raleway 12')
    labelStatsWins.grid(column = 1, row = 3, sticky = 'W', padx = 10)
    labelStatsLost = tk.Label(userFrame, text = db.userLost, bg = '#000033', fg = 'white', font = 'Raleway 12')
    labelStatsLost.grid(column = 1, row = 4, sticky = 'W', padx = 10)
    labelStatsLevel = tk.Label(userFrame, text = db.userLevel, bg = '#000033', fg = 'white', font = 'Raleway 12')
    labelStatsLevel.grid(column = 1, row = 5, sticky = 'W', padx = 10)

#A Frame for Difficulty Selection
def delResLabels():
    try:
        if userWin.winfo_exists():
            userWin.grid_forget()
        if userLost.winfo_exists():
            userLost.grid_forget()
    except NameError as err: 
        pass

def diffSelectFrame():
    def playGame():
        diff_select = diff_level.get()
        diffLabel = tk.Label(diffFrame)
        diffLabel.grid(column = 0, row = 5, columnspan = 2, pady = 10)       
        if diff_select == "easy":
            delResLabels()
            diffLabel.config(text = f"Level: {diff_select}", bg = 'white', fg ='black') 
            d.easy()
            guessFunc()       
        if diff_select == "normal":
            delResLabels()
            diffLabel.config(text = f"Level: {diff_select}", bg = '#9b59b6')       
            d.normal()
            guessFunc()
        if diff_select == "hard":
            delResLabels()
            diffLabel.config(text = f"Level: {diff_select}", bg = '#9b59b6')
            d.hard()
            guessFunc()
    diffFrame = tk.Frame(root, height = 250, width = 200, bg = '#000033')
    diffFrame.grid(column = 6, row = 5, columnspan = 2, rowspan = 5, sticky = 'NEWS')
    diffFrame.grid_propagate (False) # Stop frame from shrinking
    diffFrame.columnconfigure([0,1], weight = 1)
    diffFrame.rowconfigure([0,6], weight = 1)
    diffFrameTitle = tk.Label(diffFrame, text = "Game Options", bg = '#000033', fg = 'white', font = 'Raleway 18 bold')
    diffFrameTitle.grid(column = 0, row = 0, columnspan = 2)
    diffStr = tk.StringVar()
    diff_level = ttk.Combobox(diffFrame, justify= 'center', width = 12, background='#000033', foreground= '#1a0600', textvariable = diffStr, values = ["easy", "normal", "hard"])
    diff_level.grid(column = 0, row = 2, columnspan = 2, pady = 10)
    diff_level.set("Pick Difficulty")  
    diffBtn = tk.Button(diffFrame, text="Select",command = playGame, bg = 'black', fg = 'red')
    diffBtn.grid(column = 0, row = 3, columnspan = 2)

root.mainloop()
