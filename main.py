from cmu_graphics import * 
import sys
from classes import * 
from functions import *
 # import random


def onJoyPress(app, button, joystick):
    if button == '5':
        sys.exit(0)

BACKGROUND_IMAGE_URL = r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\CMUPic.png"
CMU_RUSH_IMG_URL = r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\CMURUSH.png"

LEVEL_ATTRIBUTES = {
    "Easy": {
        "ddy": 1.15,
        "obstacleFrequency": 120,
        "bonusMeterEnabled": False,
        "obstacleSpeed": 8,
        "attackerSpeed" : 20,
        "attackerFrequency": 120,
        "collectibleFrequency" : 180,
        "bonusDuration": None
    },
    "Medium": {
        "ddy": 1.2,
        "obstacleFrequency": 100,
        "bonusMeterEnabled": True,
        "obstacleSpeed": 10,
        "attackerSpeed" : 20,
        "attackerFrequency": 100,
        "collectibleFrequency" : 360,
        "bonusDuration": 120
    },
    "Hard": {
        "ddy": 1.25,
        "obstacleFrequency": 80,
        "bonusMeterEnabled": True,
        "obstacleSpeed": 12,
        "attackerSpeed" : 20,
        "attackerFrequency": 80,
        "collectibleFrequency" : 400,
        "bonusDuration": 120
    },
    "Free Play": {
        "ddy": 1.15,
        "obstacleFrequency": 100,
        "bonusMeterEnabled": False,
        "attackerSpeed" : 20,
        "obstacleSpeed": 9,
        "attackerFrequency": 120,
        "collectibleFrequency" : 180,
        "bonusDuration": None
    }
}


#############
# Main Menu
##################

def onAppStart(app):
    print("started")
    app.difficulty = "Hard"
    app.fillColour1 = None
    app.fillColour2 = None
    app.fillColour3 = None
    app.showTutorial = False


def main_redrawAll(app):
    if app.showTutorial == False:
        drawRect(0, 0, app.width, app.height, fill="mediumSeaGreen")
        drawImage(CMU_RUSH_IMG_URL, app.width/2, app.height/4, width=300, height=200, align="center")
        # drawRect()
        drawLabel(f'High Score: {0}', app.width/2, 150, size=24)
        drawLabel('Freeplay', app.width/2, 200, size=24, bold=True)
        # Note: we can access app.highScore (and all app variables) from any screen
        drawLabel('Tutorial', app.width/2, 250, size=16, bold=True) # Will add challenge mode once it is developed
        drawLabel('Quit', app.width/2, 300, size=16, bold=True)

        drawRect(app.width/2, 200, 110, 30, align="center", fill=app.fillColour1, opacity=30)
        drawRect(app.width/2, 250, 80, 25, align="center", fill=app.fillColour2, opacity=30)
        drawRect(app.width/2, 300, 60, 25, align="center", fill=app.fillColour3)

    if app.showTutorial == True:
        drawLabel("Press up arrow once to jump twice to double Jump", 382, 40, size=12)
        drawLabel("After double jump you will have to land to jump again.", 382, 80, size=12)
        drawLabel("After the double jump you can hold the up key to hover", 382, 120, size=12)
        drawLabel("Collect powerups, avoid the black circles (Quizzes)", 382, 160, size=12)
        drawLabel("You will die if your health becomes zero", 382, 200, size=12)
        drawLabel("Press R to reset and press P to open pause menu", 382, 240, size=12)
        drawLabel("Return back to main screen from pause menu", 382, 280, size=12)
        drawLabel("Return Back ,Press m to return ! ", 382, 340, size=12)



    

def main_onMouseMove(app, mouseX, mouseY):
    if app.width/2 - 55 <= mouseX <= app.width/2 + 55 and 200 <= mouseY <= 200+30:
        app.fillColour1 = "grey"
    else:
        app.fillColour1 = None

    if app.width/2 - 40 <= mouseX <= app.width/2 + 40 and 250 <= mouseY <= 250+25:
        app.fillColour2 = "grey"
    else:
        app.fillColour2 = None

    

def main_onMousePress(app, mouseX, mouseY):
    if app.width/2 - 15 <= mouseX <= app.width/2 + 15 and 200 <= mouseY <= 200+30: 
        setActiveScreen('game')

    if app.width/2 - 40 <= mouseX <= app.width/2 + 40 and 250 <= mouseY <= 250+25:
        app.showTutorial = True

    if app.showTutorial == True:
        # CHeck for returning back
        pass

def main_onKeyPress(app, key):
    if key == "m":
        app.showTutorial = False


def reset(app):
    levelConfig = LEVEL_ATTRIBUTES[app.difficulty]
    app.ddy = levelConfig["ddy"]
    app.obstacleFrequency = levelConfig["obstacleFrequency"]
    app.bonusMeterEnabled = levelConfig["bonusMeterEnabled"]
    app.obstacleSpeed = levelConfig["obstacleSpeed"]
    app.attackerSpeed = levelConfig["attackerSpeed"]
    app.attackerFrequency = levelConfig["attackerFrequency"]
    app.collectibleFrequency = levelConfig["collectibleFrequency"]
    app.bonusDuration = levelConfig["bonusDuration"]

    app.scrollX = 0
    app.steps = 0
    app.score = 0
    app.paused = False
    app.pauseButtonPressed =  False # This is the physcical pause button check
    app.action = "Run"
    app.mainSpriteIndex = 0
    animate(app)
    app.swinging = False
    app.mainChar = MainChar(app)
    app.attacker = Attacker()
    app.swingingPivots = swingingPivot()
    app.pivots = pivots(app)
    app.mainChar.hover = False
    app.poles = Poles()
    app.quizzes = Quizzes()
    app.collectibles = collectibles()
    app.boulder = Boulder()
    app.batarangAngle = 0
    app.batarangs = Batarang(app)
    app.frames = Frames()
    app.jumping = False
    app.sliding = False
    app.jumpCount = 0
    app.poleTimer = 0
    app.stepMode = False
    app.gameOver = False
    app.bonusMeter = 0
    app.deanTrickReady = False
    app.deanTrickActive = False
    app.deanTrickTimer = 0
    app.deanPower = DeanPower()



def game_onAppStart(app):
    reset(app)
    

def game_onKeyPress(app, key):
    if key == "p" or app.pauseButtonPressed == True:
        app.paused = not app.paused
    if key == "r":
        reset(app)
    
    if app.paused == False:
        if app.deanTrickReady and key == "d":  # Activate DEAN Trick
            app.deanTrickActive = True
            app.deanTrickReady = False
            app.deanTrickTimer = 0  # Start the timer
            app.bonusMeter = 0  # Reset the bonus meter
        if key == "up" and not app.sliding:
            app.jumpCount += 1
            if app.jumpCount <= 2:
                app.mainChar.jump(app)
            else:
                app.action = "Jump"
        elif not app.sliding:
            app.action = "Run"
        
        if key == "s":
            if app.stepMode == True:
                takeStep(app)
        if key == "S":
            app.stepMode = not app.stepMode
        if key == "left":
            app.batarangs.throwBatarang(app)

def game_onKeyHold(app, keys):
    if app.paused == False:

        if "up" in keys:
            if app.jumpCount > 2:
                app.animation = "Hover"
                app.mainChar.hover = True

        if "down" in keys and not app.jumping:
            app.sliding = True
            app.action = "Slide"

        if "space" in keys and not app.swinging:  
            # Check if player is near enough to start swinging
            for pivot in app.pivots.pivots:
                if abs(app.mainChar.pos[0] - pivot[0]) < 100:
                    app.swingingPivots.startSwinging(pivot[0], pivot[1])

    


def game_onKeyRelease(app, key):
    if app.paused == False:
        if key == "up":
            app.jumping = False
            app.hovering = False
            app.mainChar.hover =  False
            app.action = "Run"

        if key == "down":
            app.sliding = False
            app.action = "Run"

        if key == "space":
            app.swingingPivots.stopSwinging()
        
    

def game_redrawAll(app):
    if app.paused == False:
        # drawImage(BACKGROUND_IMAGE_URL, app.width/2, app.height/2, width=app.width, height=app.height, align ="center")
        app.frames.drawFrames(app)
        drawLine(0, app.mainChar.ground, app.width, app.mainChar.ground)
        drawLabel(f"Score : {app.score}", 50, 55, size=20)
        app.mainChar.draw(app)
        app.poles.drawPole(app)
        app.quizzes.draw(app)
        app.pivots.drawPivot(app)
        app.collectibles.drawCollectible(app)
        app.batarangs.drawBatarangs(app)
        app.batarangs.drawBatarangCount(app)
        app.attacker.draw()
        if app.difficulty != "Easy":
            app.boulder.draw()
        if app.difficulty == "Hard":
            app.deanPower.draw(app)


    else:
        drawRect(0, 0, app.width, app.height, fill="lightSteelBlue")
        drawLabel("Game Paused !", app.width/2, 150, size=24)
        drawLabel('Continue', app.width/2, 200, size=24, bold=True)
        ## Note: we can access app.highScore (and all app variables) from any screen
        drawLabel('Back to Home Screen', app.width/2, 250, size=16, bold=True) # Will add challenge mode once it is developed
        drawLabel('Quit', app.width/2, 300, size=16, bold=True)

        drawRect(app.width/2, 200, 110, 30, align="center", fill=app.fillColour1, border="black", opacity=30)
        drawRect(app.width/2, 250, 200, 25, align="center", fill=app.fillColour2, border="black", opacity=30)
        drawRect(app.width/2, 300, 60, 25, align="center", fill=app.fillColour3, border="black")

    if app.gameOver:
        drawLabel('Game Over', app.width // 2, app.height // 2, size=24)


def takeStep(app):
    app.mainChar.onStep(app)
    app.poles.onStep(app)
    app.quizzes.onStep(app)

    

def game_onStep(app):
    # app.mainChar.jump(app)
    if app.paused == False:
        if not app.stepMode and not app.gameOver:
            app.steps += 1
            app.mainChar.onStep(app)
            app.poles.onStep(app)
            app.attacker.onStep(app)
            app.quizzes.onStep(app)
            app.collectibles.onStep(app)
            app.batarangs.onStep(app)
            app.swingingPivots.onStep(app)
            app.pivots.onStep(app)
            if app.difficulty != "Easy":
                app.boulder.onStep(app)

            if app.difficulty == "Hard":
                app.deanPower.onStep(app)


        if app.steps % 20 == 0:
            app.score += 1



def game_onMouseMove(app, mouseX, mouseY):
    if app.paused:
        if app.width/2 - 55 <= mouseX <= app.width/2 + 55 and 200 <= mouseY <= 200+30:
            app.fillColour1 = "grey"
        else:
            app.fillColour1 = None

        if app.width/2 - 100 <= mouseX <= app.width/2 + 100 and 250 <= mouseY <= 250+25:
            app.fillColour2 = "grey"
        else:
            app.fillColour2 = None

        # Need to do the third one both here and up in main as well

    

def game_onMousePress(app, mouseX, mouseY):
    if app.paused:
        if app.width/2 - 15 <= mouseX <= app.width/2 + 15 and 200 <= mouseY <= 200+30: 
            app.paused = not app.paused

        if app.width/2 - 100 <= mouseX <= app.width/2 + 100 and 250 <= mouseY <= 250+25:
            setActiveScreen("main")



# runApp(width=764, height=425)


print("""For now there is a start screen. The square can jump and then move 
onto the coming poles. There are new poles appearing as well as some black
balls which represent quizzes for now
There is a health bar that changes after it is hit 
by one of the black balls I am in the process of implementing the swinging
mechanism using hangers but haven't finished. The game is over when the 
health becomes zero.""")
print("jjh")
runAppWithScreens(width=800, height=425, initialScreen='main')