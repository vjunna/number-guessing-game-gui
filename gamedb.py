import sqlite3

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
def createNewUser(userName):
    dbConnectObject = sqlite3.connect('game.db')
    dbCursorObject = dbConnectObject.cursor()
    userCreate = f"INSERT INTO users (username, usercoins, userwins, userlost, userlevel) VALUES ('{userName}', 50, 0, 0, 0);"
    dbCursorObject.execute(userCreate)
    dbConnectObject.commit()
    dbConnectObject.close()    
def userValidation(userName):      
    global userRes
    dbConnectObject = sqlite3.connect('game.db')
    dbCursorObject = dbConnectObject.cursor()
    print(userName)
    userQuery = f"SELECT * from users WHERE username = '{userName}'"
    dbCursorObject.execute(userQuery)
    userRes = dbCursorObject.fetchone()
    dbConnectObject.close()
    # if userRes is None:
    #     db.createNewUser()
def userProfileDB(userName):    
    global playerID, userCoins, userWins, userLost, userLevel
    # self.playerID = playerID
    dbConnectObject = sqlite3.connect('game.db')
    dbCursorObject = dbConnectObject.cursor()
    userQuery = f"SELECT playerID, username, usercoins, userwins, userlost, userlevel from users WHERE username = '{userName}'"
    dbCursorObject.execute(userQuery)
    userRes = dbCursorObject.fetchall()
    print(userRes)
    for i in userRes:
        playerID = i[0]
        userName = i[1]
        userCoins = i[2]
        userWins = i[3]
        userLost = i[4]
        userLevel = i[5]
    dbConnectObject.close()
    # print(playerID, userCoins, userWins, userLost, userLevel)
def updateUserDB(userName, reward, gameResult):
    # self.gameResult = gameResult     
    dbConnectObject = sqlite3.connect('game.db')
    dbCursorObject = dbConnectObject.cursor()
    #Updating Wins and losses to database
    if gameResult == 'win':
        updateWinsQuery = f"UPDATE users SET usercoins = ({userCoins} + {reward}), userwins = ({userWins + 1}) WHERE username = '{userName}'"
        dbCursorObject.execute(updateWinsQuery)    
    elif gameResult == 'lost':
        updateLostQuery = f"UPDATE users SET userlost = ({userWins} + 1) WHERE username = '{userName}'"
        dbCursorObject.execute(updateLostQuery)
    else: 
        pass     
    dbConnectObject.commit()
    dbConnectObject.close()
def updateUserlevel(userName): # Updating user level
    # userValidation()
    dbConnectObject = sqlite3.connect('game.db')
    dbCursorObject = dbConnectObject.cursor()
    if userCoins > 55 and userCoins <= 70:
        l1 = updateLevelQuery = f"UPDATE users SET userlevel = 1 WHERE username = '{userName}'"
        dbCursorObject.execute(l1)
    elif userCoins > 80 and userCoins <= 100:
        l2 = updateLevelQuery = f"UPDATE users SET userlevel = 2 WHERE username = '{userName}'"
        dbCursorObject.execute(l2)
    elif userCoins > 100 and userCoins <= 125:
        l3 = updateLevelQuery = f"UPDATE users SET userlevel = 3 WHERE username = '{userName}'"
        dbCursorObject.execute(l3)
    elif userCoins > 125 and userCoins <= 175:
        l4 = updateLevelQuery = f"UPDATE users SET userlevel = 4 WHERE username = '{userName}'"
        dbCursorObject.execute(l4)
    elif userCoins > 175 and userCoins <= 250:
        l5 = updateLevelQuery = f"UPDATE users SET userlevel = 5 WHERE username = '{userName}'"
        dbCursorObject.execute(l5)
    elif userCoins > 250 and userCoins <= 350:
        l6 = updateLevelQuery = f"UPDATE users SET userlevel = 6 WHERE username = '{userName}'"
        dbCursorObject.execute(l6)
    else:
        l0 = updateLevelQuery = f"UPDATE users SET userlevel = 0 WHERE username = '{userName}'"
        dbCursorObject.execute(l0)

    dbConnectObject.commit()
    dbConnectObject.close()
