from cmu_graphics import * 
import sys
from classes import * 
from functions import *
 # import random


def onJoyPress(app, button, joystick):
    if button == '5':
        sys.exit(0)

CMU_RUSH_IMG_URL = "./Images/CMURUSH.png"

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
    app.steps = 0
    app.progress = 0
    app.loading = False
    app.fillColour1 = None
    app.fillColour2 = None
    app.fillColour3 = None
    app.fillColour4 = None
    app.fillColour5 = None
    app.showTutorial = False
    app.showChallengeOptions = False
    with open('./High Score.txt') as f:
        app.highScore = f.readline()

def main_onAppStart(app):
    with open('./High Score.txt') as f:
        app.highScore = f.readline()

def main_redrawAll(app):
    # if app.showTutorial:
    #     pass
    # elif app.showChallengeOptions:
    #     pass
    # else:
    # Gradient background

    

    for i in range(0, app.height, 5):
        color = rgb(135 - i // 10, 206 - i // 15, 250 - i // 20)  # Sky blue gradient
        drawRect(0, i, app.width, 5, fill=color)
    
    # Game title
    drawLabel("CMU RUSH", app.width / 2, app.height / 6, size=40, fill="darkBlue", bold=True)

    # High Score
    drawLabel(f"High Score : {app.highScore}", app.width / 2, app.height / 3, size=25)


    # Buttons
    button_specs = [
        ("Freeplay", app.width / 2, app.height / 3 + 50, app.fillColour2),
        ("Challenge Mode", app.width / 2, app.height / 3 + 100, app.fillColour3),
        ("Instructions", app.width / 2, app.height / 3 + 150, app.fillColour4),
        ("Quit", app.width / 2, app.height / 3 + 200, app.fillColour5),
    ]

    for text, x, y, fill in button_specs:
        drawRect(x, y, 200, 40, fill=fill, border="black", align="center")
        drawLabel(text, x, y, size=20, fill="black", bold=True)

    # Footer
    drawLabel("Hover over buttons to highlight, click to select!", app.width / 2, app.height - 20, size=12, fill="darkGray")

    if app.loading:  # Show loading screen
        drawRect(0, 0, app.width, app.height, fill="green")

        # Loading title
        drawLabel("Get Ready for Freeplay!", app.width / 2, app.height / 4, size=30, fill="white", bold=True)

        # Theme message
        drawLabel("Strive to survive as long as you can.", app.width / 2, app.height / 3, size=20, fill="lightGray")
        drawLabel("Be careful about your health!", app.width / 2, app.height / 3 + 30, size=20, fill="lightGray")

        # Progress Bar
        
        barWidth = app.progress * 300
        drawRect(app.width / 2 , app.height / 2, 300, 20, fill="gray", border="white", align="center")
        drawRect(app.width / 2 , app.height / 2, barWidth + 0.1, 20, fill="lightGreen", align="center")

        
def main_onMouseMove(app, mouseX, mouseY):
    # Determine hover effect
    button_positions = [
        (app.width / 2 - 100, app.height / 3 - 20, app.width / 2 + 100, app.height / 3 + 20),
        (app.width / 2 - 100, app.height / 3 + 30, app.width / 2 + 100, app.height / 3 + 70),
        (app.width / 2 - 100, app.height / 3 + 80, app.width / 2 + 100, app.height / 3 + 120),
        (app.width / 2 - 100, app.height / 3 + 130, app.width / 2 + 100, app.height / 3 + 170),
        (app.width / 2 - 100, app.height / 3 + 180, app.width / 2 + 100, app.height / 3 + 220),
    ]
    fills = ["lightGray", "lightGray", "lightGray", "lightGray", "lightGray"]
    for i, (x1, y1, x2, y2) in enumerate(button_positions):
        if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
            fills[i] = "gray"

    # Update hover colors
    app.fillColour1, app.fillColour2, app.fillColour3, app.fillColour4, app.fillColour5 = fills

def main_onMousePress(app, mouseX, mouseY):
    # Button actions
    button_positions = [
        (app.width / 2 - 100, app.height / 3 - 20, app.width / 2 + 100, app.height / 3 + 20, "highScore"),
        (app.width / 2 - 100, app.height / 3 + 30, app.width / 2 + 100, app.height / 3 + 70, "freePlay"),
        (app.width / 2 - 100, app.height / 3 + 80, app.width / 2 + 100, app.height / 3 + 120, "challengeMode"),
        (app.width / 2 - 100, app.height / 3 + 130, app.width / 2 + 100, app.height / 3 + 170, "instructions"),
        (app.width / 2 - 100, app.height / 3 + 180, app.width / 2 + 100, app.height / 3 + 220, "quit"),
    ]
    for x1, y1, x2, y2, action in button_positions:
        if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
            if action == "highScore":
                print("High Score selected.")
            elif action == "freePlay":
                app.loading = True  # Activate the loading screen
                app.loadingStartTime = app.steps  # Track when the loading starts
                # setActiveScreen('game')  # Example
            elif action == "challengeMode":
                app.showChallengeOptions = True
                setActiveScreen("challengeModes")
                print("Challenge Mode selected.")
            elif action == "instructions":
                setActiveScreen("instructions")
                print("Instructions selected.")
            elif action == "quit":
                exit()

def main_onKeyPress(app, key):
    if key == "m":  # Return to main menu
        setActiveScreen("main")


def main_onStep(app):
    with open('./High Score.txt') as f:
        app.highScore = f.readline()

    app.steps += 1

    if app.loading:
        app.progress = min((app.steps - app.loadingStartTime) / 240, 1)  # 240 steps = 4 seconds
        if app.progress >= 1:  # Loading complete
                app.loading = False
                setActiveScreen('game')  # Start Freeplay mode


# Instructions Screen
def instructions_redrawAll(app):
    # Background
    drawRect(0, 0, app.width, app.height, fill="lightBlue")

    # Title
    drawLabel("Instructions", app.width / 2, app.height / 8, size=30, fill="darkBlue", bold=True)

    # Instructions Text
    instructions = [
        "1. Press UP to jump and double jump. and down to slide",
        "2. Press and hold UP to hover after a double jump.",
        "3. Avoid black circles (Quizzes), attackers and other obstacles.",
        "4. Collect power-ups for help.",
        "5. You can throw batarangs using the left arrow key.",
        "6. Slide to kill attackers",
        "7. Try to dodge the grey rectangles and the bullets."
    ]
    for i, line in enumerate(instructions):
        drawLabel(line, app.width / 2, app.height / 4 + i * 30, size=18, fill="black")

    # Back Button
    drawRect(app.width / 2, app.height - 100, 150, 40, fill="gray", border="black", align="center")
    drawLabel("Back to Menu", app.width / 2, app.height - 100, size=20, fill="black")


def instructions_onMousePress(app, mouseX, mouseY):
    # Check if the "Back to Menu" button is clicked
    if app.width / 2 - 75 <= mouseX <= app.width / 2 + 75 and app.height - 100 - 20 <= mouseY <= app.height - 100 + 20:
        setActiveScreen("main")



# Challenge Modes Screen
def challengeModes_redrawAll(app):
    # Background
    drawRect(0, 0, app.width, app.height, fill="lightGreen")

    # Title
    drawLabel("Challenge Modes", app.width / 2, app.height / 8, size=30, fill="darkGreen", bold=True)

    # Difficulty Buttons
    button_specs = [
        ("Easy", app.width / 2, app.height / 3, app.fillColour1),
        ("Medium", app.width / 2, app.height / 3 + 60, app.fillColour2),
        ("Hard", app.width / 2, app.height / 3 + 120, app.fillColour3)
    ]
    for text, x, y, fill in button_specs:
        drawRect(x, y, 200, 40, fill=fill, border="black", align="center")
        drawLabel(text, x, y, size=20, fill="black")

    # Back Button
    drawRect(app.width / 2, app.height - 100, 150, 40, fill="gray", border="black", align="center")
    drawLabel("Back to Menu", app.width / 2, app.height - 100, size=20, fill="black")

    if app.loading:
        drawRect(0, 0, app.width, app.height, fill="green")

        # Loading title
        drawLabel(f"Get Ready for {app.selectedDifficulty} Mode!", app.width / 2, app.height / 4, size=30, fill="white", bold=True)

        # Display the theme message based on the selected mode
        if app.selectedDifficulty == "Easy":
            theme_message = ["Avoid the incoming attackers and quizzes."]
        elif app.selectedDifficulty == "Medium":
            theme_message = ["Beware the gray boxes!", "They will decrease your health wherever you hit them."]
        elif app.selectedDifficulty == "Hard":
            theme_message = ["You will need Dean Trick's help to survive!"]
        else:
            theme_message = []

        for i, line in enumerate(theme_message):
            drawLabel(line, app.width / 2, app.height / 3 + i * 30, size=20, fill="lightGray")


        
        barWidth = app.progress * 300
        drawRect(app.width / 2, app.height / 2, 300, 20, fill="gray", border="white", align="center")
        drawRect(app.width / 2, app.height / 2, barWidth + 0.1, 20, fill="lightGreen", align="center")

        


def challengeModes_onMouseMove(app, mouseX, mouseY):
    # Highlight difficulty buttons on hover
    button_positions = [
        (app.width / 2 - 100, app.height / 3 - 20, app.width / 2 + 100, app.height / 3 + 20),
        (app.width / 2 - 100, app.height / 3 + 40, app.width / 2 + 100, app.height / 3 + 80),
        (app.width / 2 - 100, app.height / 3 + 100, app.width / 2 + 100, app.height / 3 + 140)
    ]
    fills = ["lightGray", "lightGray", "lightGray"]
    for i, (x1, y1, x2, y2) in enumerate(button_positions):
        if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
            fills[i] = "gray"

    # Update hover colors
    app.fillColour1, app.fillColour2, app.fillColour3 = fills


def challengeModes_onMousePress(app, mouseX, mouseY):
    # Button actions
    button_positions = [
        (app.width / 2 - 100, app.height / 3 - 20, app.width / 2 + 100, app.height / 3 + 20, "Easy"),
        (app.width / 2 - 100, app.height / 3 + 40, app.width / 2 + 100, app.height / 3 + 80, "Medium"),
        (app.width / 2 - 100, app.height / 3 + 100, app.width / 2 + 100, app.height / 3 + 140, "Hard")
    ]
    for x1, y1, x2, y2, difficulty in button_positions:
        if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
            app.loading = True
            app.loadingStartTime = app.steps
            app.selectedDifficulty = difficulty  # Store selected difficulty

            # app.difficulty = difficulty  # Set difficulty in the app
            # setActiveScreen('game')  # Start the game
            # print(f"Selected {difficulty} mode!")

    # Back to Menu
    if app.width / 2 - 75 <= mouseX <= app.width / 2 + 75 and app.height - 100 - 20 <= mouseY <= app.height - 100 + 20:
        setActiveScreen("main")

def challengeModes_onStep(app):
    app.steps += 1
    if app.loading:
        app.progress = min((app.steps - app.loadingStartTime) / 240, 1)  # 240 steps = 4 seconds
        if app.progress >= 1:  # Loading complete
                app.loading = False
                app.difficulty = app.selectedDifficulty  # Set the game's difficulty
                setActiveScreen('game')  # Start the game

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
    app.pauseButtonFill = "gray"
    app.scoreDoubled = False
    app.doubleTimeStarted = False
    app.paused = False
    app.pauseButtonPressed =  False # This is the physcical pause button check
    app.action = "Run"
    app.mainSpriteIndex = 0
    animate(app)
    app.mainChar = MainChar(app)
    app.attacker = Attacker()
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
    # if app.paused == False:
        # drawImage(BACKGROUND_IMAGE_URL, app.width/2, app.height/2, width=app.width, height=app.height, align ="center")
    app.frames.drawFrames(app)
    drawLine(0, app.mainChar.ground, app.width, app.mainChar.ground)
    if app.scoreDoubled:
        drawLabel(f"Score x2 : {app.score}", 50 + 10, 55, size=20)
    else:
        drawLabel(f"Score : {app.score}", 50, 55, size=20)
    app.mainChar.draw(app)
    app.poles.drawPole(app)
    app.quizzes.draw(app)
    app.collectibles.drawCollectible(app)
    app.batarangs.drawBatarangs(app)
    app.batarangs.drawBatarangCount(app)
    app.attacker.draw()
    if app.difficulty != "Easy":
        app.boulder.draw()
    if app.difficulty == "Hard":
        app.deanPower.draw(app)

    drawRect(app.width - 55, 30, 90, 40, fill=app.pauseButtonFill, border="black", align="center")
    drawLabel("Pause", app.width - 55, 30, size=18, fill="black")

    if app.paused:
        # Background with a translucent overlay
        drawRect(0, 0, app.width, app.height, fill="black", opacity=50)

        # Pause Menu Title
        drawLabel("Game Paused", app.width / 2, app.height / 3 - 60, size=30, fill="white", bold=True)

        # Buttons
        button_specs = [
            ("Resume", app.width / 2, app.height / 3, app.fillColour1),
            ("Main Menu", app.width / 2, app.height / 3 + 60, app.fillColour2),
            ("Quit", app.width / 2, app.height / 3 + 120, app.fillColour3),
        ]
        for label, x, y, fill in button_specs:
            drawRect(x, y, 240, 50, fill=fill, border="white", align="center")
            drawLabel(label, x, y, size=20, fill="black")

    elif app.gameOver:
        # Background overlay
        drawRect(0, 0, app.width, app.height, fill="black", opacity=70)

        # Game Over Title
        drawLabel("Game Over!", app.width / 2, app.height / 3 - 60, size=40, fill="red", bold=True)

        # Final Score
        drawLabel(f"Your Score: {app.score}", app.width / 2, app.height / 3, size=25, fill="white")

        # Buttons
        button_specs = [
            ("Retry", app.width / 2, app.height / 3 + 80, app.fillColour1),
            ("Main Menu", app.width / 2, app.height / 3 + 140, app.fillColour2),
        ]
        for label, x, y, fill in button_specs:
            drawRect(x, y, 200, 50, fill=fill, border="white", align="center")
            drawLabel(label, x, y, size=20, fill="black")


    

def game_onStep(app):
    # app.mainChar.jump(app)
    if app.paused == False:
        if not app.gameOver:
            app.steps += 1
            app.mainChar.onStep(app)
            app.poles.onStep(app)
            app.attacker.onStep(app)
            app.quizzes.onStep(app)
            app.collectibles.onStep(app)
            app.batarangs.onStep(app)
            if app.difficulty != "Easy":
                app.boulder.onStep(app)

            if app.difficulty == "Hard":
                app.deanPower.onStep(app)

        elif app.gameOver:
            with open('High Score.txt', 'r', encoding='utf-8') as file: 
                data = file.readlines() 
            print(data)
            if int(app.score) > int(data[0]):
                data[0] = str(app.score)
            with open('High Score.txt', 'w', encoding='utf-8') as file: 
                file.writelines(data) 

        if app.steps % 20 == 0:
            if app.scoreDoubled:
                app.score += 2
            else:
                app.score += 1

        if app.width != 800 or app.height != 425:
            app.width = 800
            app.height = 425
 
def game_onMouseMove(app, mouseX, mouseY):
    if app.width - 100 <= mouseX <= app.width - 10 and 10 <= mouseY <= 50:
        app.pauseButtonFill = "lightGray"
    else:
        app.pauseButtonFill = "gray"

    if app.paused:
         # Button positions for highlighting
        button_positions = [
            (app.width / 2 - 120, app.height / 3 - 25, app.width / 2 + 120, app.height / 3 + 25),  # Resume
            (app.width / 2 - 120, app.height / 3 + 35, app.width / 2 + 120, app.height / 3 + 85),  # Main Menu
            (app.width / 2 - 120, app.height / 3 + 95, app.width / 2 + 120, app.height / 3 + 145),  # Quit
        ]
        fills = ["lightGray", "lightGray", "lightGray"]

        # Highlight logic
        for i, (x1, y1, x2, y2) in enumerate(button_positions):
            if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
                fills[i] = "gray"

        # Update button colors
        app.fillColour1, app.fillColour2, app.fillColour3 = fills
    if app.gameOver:
        # Highlight buttons
        button_positions = [
            (app.width / 2 - 100, app.height / 3 + 55, app.width / 2 + 100, app.height / 3 + 105),  # Retry
            (app.width / 2 - 100, app.height / 3 + 115, app.width / 2 + 100, app.height / 3 + 165),  # Main Menu
        ]
        fills = ["lightGray", "lightGray"]

        for i, (x1, y1, x2, y2) in enumerate(button_positions):
            if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
                fills[i] = "gray"

        app.fillColour1, app.fillColour2 = fills


        # Need to do the third one both here and up in main as well

    

def game_onMousePress(app, mouseX, mouseY):
    if app.width - 100 <= mouseX <= app.width - 10 and 10 <= mouseY <= 50:
        app.paused = not app.paused

    if app.paused:
         # Button positions
        button_positions = [
            (app.width / 2 - 120, app.height / 3 - 25, app.width / 2 + 120, app.height / 3 + 25, "resume"),
            (app.width / 2 - 120, app.height / 3 + 35, app.width / 2 + 120, app.height / 3 + 85, "mainMenu"),
            (app.width / 2 - 120, app.height / 3 + 95, app.width / 2 + 120, app.height / 3 + 145, "quit"),
        ]

        # Button actions
        for x1, y1, x2, y2, action in button_positions:
            if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
                if action == "resume":
                    app.paused = False
                elif action == "mainMenu":
                    setActiveScreen("main")
                    reset(app)
                elif action == "quit":
                    exit()

    if app.gameOver:
        # Button positions
        button_positions = [
            (app.width / 2 - 100, app.height / 3 + 55, app.width / 2 + 100, app.height / 3 + 105, "retry"),
            (app.width / 2 - 100, app.height / 3 + 115, app.width / 2 + 100, app.height / 3 + 165, "mainMenu"),
        ]

        for x1, y1, x2, y2, action in button_positions:
            if x1 <= mouseX <= x2 and y1 <= mouseY <= y2:
                if action == "retry":
                    reset(app)  # Restart the game
                    app.gameOver = False
                elif action == "mainMenu":
                    setActiveScreen("main")
                    reset(app)



runAppWithScreens(width=800, height=425, initialScreen='main')