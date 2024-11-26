from cmu_graphics import * 
from classes import * 
# import random

BACKGROUND_IMAGE_URL = r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\CMUPic.png"
CMU_RUSH_IMG_URL = r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\CMURUSH.png"

#############
# Main Menu
##################

def main_onAppStart(app):
    app.fillColour1 = None
    app.fillColour2 = None
    app.fillColour3 = None
    app.showTutorial = False


def main_redrawAll(app):
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
        drawLabel("Press up arrow once to jump twice to double Jump")
        drawLabel("After double jump you will have to land to jump again.")
        drawLabel("After the double jump you can hold the up key to hover")
        drawLabel("collect powerups, avoid the black circles (Quizzez)")
        drawLabel("You will die if your health becomes zero")


    

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
    


def reset(app):
    app.paused = False
    app.pauseButtonPressed =  False # This is the physcical pause button check
    app.action = "Run"
    app.mainSpriteIndex = 0
    animate(app)
    app.mainChar = MainChar(app)
    app.mainChar.hover = False
    app.poles = Poles()
    app.quizzes = Quizzes()
    app.collectibles = collectibles()
    app.sliding = False
    app.jumpCount = 0
    app.poleTimer = 0
    app.stepMode = False
    app.gameOver = False


def game_onAppStart(app):
    reset(app)
    

def game_onKeyPress(app, key):
    if key == "p" or app.pauseButtonPressed == True:
        app.paused = not app.paused
    if key == "r":
        reset(app)
    
    if app.paused == False:
        if key == "d":
            # print(app.poles.poles)
            print(app.quizzes.quizzes)
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

def game_onKeyHold(app, keys):
    if app.paused == False:

        if "up" in keys:
            if app.jumpCount > 2:
                app.animation = "Hover"
                app.mainChar.hover = True

        if "down" in keys and not app.jumping:
            app.sliding = True
            app.action = "Slide"
    


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
    

def game_redrawAll(app):
    if app.paused == False:
        drawImage(BACKGROUND_IMAGE_URL, app.width/2, app.height/2, width=app.width, height=app.height, align ="center")
        drawLine(0, app.mainChar.ground, app.width, app.mainChar.ground)
        app.mainChar.draw(app)
        drawImage(app.mainSpriteImages[app.mainSpriteIndex], app.mainChar.pos[0], app.mainChar.pos[1], align='center', width=app.mainSpriteWidth/6, height=app.mainSpriteHeight/6)
        app.poles.drawPole(app)
        app.quizzes.draw(app)
        app.collectibles.drawCollectible(app)
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
            app.mainChar.onStep(app)
            app.poles.onStep(app)
            app.quizzes.onStep(app)
            app.collectibles.onStep(app)


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

runAppWithScreens(width=764, height=425, initialScreen='main')