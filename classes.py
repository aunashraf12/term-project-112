from cmu_graphics import *
from functions import *
import random

COLLECTIBLES = {"health" : r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\RedCross.png","x2" : r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\x2 Score .png", "batarangs" : r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\batarangs.png"}



class MainChar:
    def __init__(self, app) -> None:
        self.steps = 0
        self.timer = 0
        self.width = 50 # Width of app is 764
        self.height = 50 # height of app is around 400
        self.width = app.mainSpriteWidth/6
        self.height = app.mainSpriteHeight/6
        self.ground = 390
        self.velocity = [0, 0]
        self.x = 200
        self.y = self.ground - self.height/2
        self.pos = [200, self.ground - self.height/2]
        self.finalPosY = self.y - 50 # The y position after the jump is made
        # self.collisions = 
        self.powerUps = {"x2": 0, "batarangs":0}
        self.slide = False
        self.healthBoosts = [] # Now append to these boosts as they are collected and then pop from them
        self.health = 100
        app.poleBelow = False
        # app.below = False

    def draw(self, app):
        # drawRect(self.pos[0], self.pos[1], self.width, self.height, fill="blue", align="center")
        drawLabel("Health Bar", 10, 8, align="top-left")
        drawRect(10, 20, 100, 5, fill=None, border="black")
        drawRect(10, 20, self.health, 5, fill="red") if self.health > 0 else drawRect(10, 20, 100, 5, fill="red", opacity=0)


    def jump(self, app):
        # app.mainCharPosY = self.finalPosY
        # if not app.poles.checkIllegalColliding(app) == (False, "bottom"):
        app.animation = "Jump"
        if app.jumpCount == 1:
            app.mainChar.pos[1] -= 100
        if app.jumpCount == 2:
            app.mainChar.pos[1] -= 180
        app.jumping = True

        # if len(app.poles.poles) > 0:
        #     if self.pos[1] - app.poles.poles[0][1] + app.poles.height <= self.height / 2:
        #         self.pos[1] = app.poles.poles[0][1] + app.poles.height + self.height / 2  # Work on this afterwards
        #     else:
        #         self.pos[1] = app.poles.poles[0][1] - self.height / 2


    def update(self, app, movement=(0, 0)):
        self.collisions = {"up" : False, "down" : False, "right" : False, 
                           "left": False}
        
        # The amount the character wil move in one frame
        frameMovement = (movement[0] + self.velocity[0], movement[1] + 
                         self.velocity[1])

        self.pos[0] += frameMovement[0]
        self.pos[1] += frameMovement[1]
        # app.scrollX += frameMovement[0]
        # app.scrollY += frameMovement[1]
        app.frames.scrollRight()


        for pole in app.poles.poles:
            if app.mainChar.pos[0] + app.mainChar.width // 2  >= pole[0]:         # Checking for collision with poles downwards
                if app.mainChar.pos[0] - app.mainChar.width // 2 <= pole[0] + pole[2]: 
                    if app.mainChar.pos[1] + app.mainChar.height // 2 >= pole[1] and app.mainChar.pos[1] - app.mainChar.height // 2 <= pole[1] + app.poles.height:
                        self.collisions["down"] = True

    
        self.velocity[1] = 3 if self.hover == True else 8 #min(5, self.velocity[1] + 0.1) # Gravity
        if self.collisions['down'] or app.mainChar.pos[1] + app.mainChar.height / 2 >= app.mainChar.ground:
            self.velocity[1] = 0

        if self.collisions["left"]:
            self.velocity[0] = 0


    def grounded(self, app):
        bottomOfChar = self.y + self.height // 2
        if self.collisions['down'] or app.mainChar.pos[1] + app.mainChar.height / 2 >= app.mainChar.ground:
            app.jumpCount = 0
            return True
        # elif app.poleBelow and bottomOfChar + 5 >= app.curPolY:
        #     app.jumpCount = 0
        #     return True
        else:
            return False

    def swing(self, app, x, y):
        # Line
        drawLine(x, y, self.x, self.y)
        
        if app.swingingPivot == True and abs(app.swingingPivotX - app.mainCharX ) <= 100: # Now check with the space bar in OnkeyHold
            # Circular motion
            # Harcode the arc length values
            pass


    def throw(self, app):
        # if mainChar.batarangs >= 0: # Check this in on key press
        # Batarang(app)
        drawLine(app.mainCharX, app.mainCharHeight / 4, app.mainCharX, 3 * app.mainCharHeight / 4) # Rotate this as well


    def collecting(app):
        pass
        # if app.mainChar touching any powerups:
        #     app.mainChar.addPowerUp() # Class method

    def onStep(self, app):
        # self.gravity(app)
        self.update(app)
        self.grounded(app) # Checks if the object is grounded and sets the jump count to zero
        self.steps += 1
        if self.steps % 30 == 0:
            self.timer += 1
        animate(app)
        
        # if after making the jump the character is in the middle of a pole
        if self.collisions["down"] == True:
            if app.poles.poles[0][1] - (self.pos[1] - self.height // 2) <= self.height:
                self.pos[1] = app.poles.poles[0][1] - self.height // 2
            elif self.pos[1] + self.height // 2 - (app.poles.poles[0][1] + app.poles.height) <= self.height:
                self.pos[1] = app.poles.poles[0][1] + app.poles.height + self.height // 2 + 1


class Poles:
    def __init__(self) -> None:
        self.width = 400 # random between 300 and 500
        self.height = 10
        self.poles = []

    def addPole(self, app):
        poleX = app.width
        self.width = random.randint(300, 500)
        poleY = random.randint(100, 300)

        if len(self.poles) == 0:
            self.poles.append([poleX, poleY, self.width])

    def drawPole(self, app):
        for pole in self.poles:
            drawRect(pole[0], pole[1], pole[2], self.height)

    def animatePole(self, app):
        for pole in self.poles:
            pole[0] -= 8

    def removePole(self, app):
        for pole in self.poles[:]:
            if pole[0] + pole[2] <= 0:
                self.poles.remove(pole)
        return True


    def onStep(self, app):
        app.poleTimer += 1
        # print(self.poles)
        if app.poleTimer % 120 == 0:
            # print("generated", app.poleTimer)    
            app.poles.addPole(app)

        app.poles.animatePole(app)
        app.poles.removePole(app)
        
        app.poles.checkForMainChar(app)

        if app.mainChar.health <= 0:
            app.gameOver = True


        


    def checkForMainChar(self, app):
        for pole in self.poles:
            if app.mainChar.pos[0] + app.mainChar.width//2 >= pole[0] and app.mainChar.pos[0] - app.mainChar.width // 2 <= pole[0] + pole[2] and app.mainChar.y + app.mainChar.height // 2 <= pole[1]:
                app.poleBelow = True
                app.curPolY = pole[1]
            else:
                app.poleBelow = False


class swingingPivots:
    def __init__(self, app) -> None:
        self.x = app.width # random between 300 and 500
        self.y = 50
        self.r = 10
        self.blips = 0
        self.pivots = []

    def addPivot(self, app):
        self.pivots.append([self.x, self.y, self.r])

    def checkForMainChar(self, app):
        # ang1 = angleTo(app.mainChar, 200, 300, 200)
        # x, y = getPointInDir(200, 200, 45, 50)
        # Line(200, 200, x, y)

        for pivot in self.pivots:
            if pivot[0] - app.mainChar.pos[0] <= 80:
                app.mainChar.swing(app, pivot[0], pivot[1])

    def removePivot(self, app):
        for pivot in self.pivots[:]:
            if pivot[0] + pivot[2] < 0:
                self.pivots.remove(pivot)


    def onStep(self, app):
        self.x -= 10
        self.blips += 1
        if self.blips % 120 == 0:
            self.addPivot(app)

        self.removePivot(app)


class Quizzes:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.r = 10
        self.steps = 0
        self.quizzes = []

    def add(self, app):
        self.x = app.width
        self.y =  random.randint(200, 400)# random.randint(app.width//2 ,app.width)
        self.quizzes.append([self.x, self.y, self.r])
        

    def draw(self, app):
        for quiz in self.quizzes:
            drawCircle(quiz[0], quiz[1], quiz[2], fill="black")

    def removeQuiz(self, app):
        for quiz in self.quizzes[:]:
            if quiz[0] + quiz[2] <= 0:
                self.quizzes.remove(quiz)


    def touchingMainChar(self, app):
        rightX = app.mainChar.pos[0] + app.mainChar.width//2
        topY =  app.mainChar.pos[1] - app.mainChar.height//2
        bottomY = app.mainChar.pos[1] + app.mainChar.height//2
        for quiz in self.quizzes:
            if quiz[1] - self.r > bottomY or quiz[1] + self.r < topY:
                return False
            else:
                if abs(quiz[0] - rightX) <= self.r:
                    # print("collison")
                    app.mainChar.health -= 10
                    self.quizzes.remove(quiz)
                    return True
                
        return False
    
    def onStep(self, app):
        self.steps += 1
        if self.steps % 120 == 0:
            self.add(app)
        for quiz in self.quizzes:
            quiz[0] -= 15

        self.removeQuiz(app)
        self.touchingMainChar(app)


class Enemy:
    def __init__(self) -> None:
        self.width, self.height = 0 , 0
        self.x = app.width
        self.y = app.mainChar.ground - self.height / 2


class collectibles:
    def __init__(self) -> None:
        self.collectibles = [] # 2-D array with the x and y position as well as the width and height of the images
        self.steps = 0
        self.timeFrequency = random.randint(10, 20)

    def addCollectible(self, app):
        if len(self.collectibles) == 0:
            myList = list(COLLECTIBLES.keys())
            print(myList)
            thisCollectible = random.choice(myList) # Random
            self.timeFrequency = random.randint(1, 5)
            if thisCollectible == "health":
                width, height = getImageSize(COLLECTIBLES["health"])
                self.collectibles.append(["health", app.width, app.mainChar.ground - app.mainChar.height // 2, width, height])
            elif thisCollectible == "x2":
                width, height = getImageSize(COLLECTIBLES["x2"])
                self.collectibles.append(["x2", app.width, app.mainChar.ground - app.mainChar.height // 2, width, height])
            elif thisCollectible == "batarangs":
                width, height = getImageSize(COLLECTIBLES["batarangs"])
                self.collectibles.append(["batarangs", app.width, app.mainChar.ground - app.mainChar.height // 2, width, height])


    def drawCollectible(self, app):
        for collectible in self.collectibles:
            drawImage(COLLECTIBLES[collectible[0]], collectible[1], collectible[2], width=50, height=50, align="center")

    def animateCollectible(self, app):
        for collectible in self.collectibles:
            collectible[1] -= 10


    def removeCollectible(self, app):
        for collectible in self.collectibles[:]:
            if collectible[1] + collectible[3] // 2 <= 0:
                self.collectibles.remove(collectible)

    def detectCollectible(self, app):
        for collectible in self.collectibles[:]:
            left1, right1 = app.mainChar.pos[0] - app.mainChar.width//2, app.mainChar.pos[0] + app.mainChar.width//2
            top1, bottom1 = app.mainChar.pos[1] - app.mainChar.height//2, app.mainChar.pos[1] + app.mainChar.height//2
            left2, right2 = collectible[1] - 50 // 2, collectible[1] + 5 // 2
            top2, bottom2 = collectible[2] - 50 // 2, collectible[2] + 5 // 2

            if left1 <= right2 and right1 >= left2 and top1 <= bottom2 and bottom1 >= top2:
                print("colliding")
                if collectible[0] == "health":
                    app.mainChar.health = 100
                elif collectible[0] == "x2":
                    app.scoreDoubled = True # Remove this after some time passes by
                else:
                    app.mainChar.powerUps["batarangs"] += 3
                    app.batarangs.initialiseBatrangsArray(app)
                
                self.collectibles.remove(collectible)


    def onStep(self, app):
        print(self.collectibles)
        self.steps += 1
        if self.steps % (self.timeFrequency * 30) == 0:
            self.addCollectible(app)

        
        self.animateCollectible(app)
        self.removeCollectible(app)
        self.detectCollectible(app)


class Batarang:
    def __init__(self) -> None:
        self.x = app.mainChar.pos[0]
        self.y = app.mainChar.pos[1]
        width, height = getImageSize(COLLECTIBLES["batarangs"])
        self.width, self.height = width / 8, height / 8
        self.batarangs = []
        self.curBatarangs = [] # if multiple thrown at once
        


    def initialiseBatrangsArray(self, app):
        for _ in range(app.mainChar.powerUps["batarangs"]):
            self.batarangs.append([self.x, self.y])


    def throwBatarang(self, app):
        
        if len(self.curBatarangs) > 0:
            app.batarangAngle = 0
            self.curBatarangs.append(self.batarangs.pop()) # + [app.batarangAngle])
            app.throwBatarang = True

    def removeBatarang(self, app):
        for batarang in self.curBatarangs[:]:
            if batarang[0] - self.width / 2 >= app.width:
                self.curBatarangs.remove(batarang)

    def drawBatarangs(self, app):
        for batarang in self.curBatarangs[:]:
            drawImage(COLLECTIBLES["batarangs"], batarang[0], batarang[1], align='center', width=self.width, height=self.height, rotateAngle = app.batarangAngle)

    def drawBatarangCount(self, app):
        drawLabel(f"Batarangs : {len(self.batarangs)}", 70, 80, size=20)

    
    def onStep(self, app):
        print(app.mainChar.powerUps)
        # self.initialiseBatrangsArray(app)
        self.removeBatarang(app)
        app.batarangAngle += 10
        for batarang in self.curBatarangs[:]: # if len(self.curBatarangs) >= 0
            batarang[0] += 20




class Frames:
    def __init__(self):
        self.currentFrame = 0  # Start with the first frame index
        self.frameWidth = 800  # Width of each frame
        self.xOffset = app.scrollX  # Horizontal offset for scrolling
        self.frames = [self.drawFrame1, self.drawFrame2]  # List of frame drawing functions

    def scrollRight(self):
        # Move frames to the left by increasing xOffset
        self.xOffset -= 10  # Adjust speed as needed

        # Reset xOffset to loop frames infinitely
        if self.xOffset <= -self.frameWidth:
            self.xOffset = 0
            # Swap frame order to simulate continuous scrolling
            self.frames.append(self.frames.pop(0))

    def drawFrames(self, app):
        # Draw current and next frame for seamless transition
        for i in range(2):  # Draw two frames at a time for smooth transition
            xPosition = i * self.frameWidth + self.xOffset
            if xPosition < app.width:
                self.frames[i](app, xPosition)

    def drawFrame1(self, app, xOffset):
        # Draw sky for frame 1
        drawRect(xOffset, 0, app.width, app.height, fill='skyBlue')
        
        # Define buildings for frame 1
        buildingSpecs = [
            {'color': 'lightGray', 'width': 100, 'height': 300, 'xStart': xOffset + 50},
            {'color': 'darkGray', 'width': 120, 'height': 350, 'xStart': xOffset + 210},
            {'color': 'dimGray', 'width': 80, 'height': 250, 'xStart': xOffset + 380},
            {'color': 'slateGray', 'width': 90, 'height': 400, 'xStart': xOffset + 510}
        ]
        
        self.drawBuildings(app, buildingSpecs)

    def drawFrame2(self, app, xOffset):
        # Draw sky for frame 2
        drawRect(xOffset, 0, app.width, app.height, fill='lightSkyBlue')
        
        # Define buildings for frame 2
        buildingSpecs = [
            {'color': 'darkSlateGray', 'width': 110, 'height': 320, 'xStart': xOffset + 70},
            {'color': 'gray', 'width': 130, 'height': 300, 'xStart': xOffset + 240},
            {'color': 'lightSlateGray', 'width': 90, 'height': 280, 'xStart': xOffset + 410},
            {'color': 'darkGray', 'width': 100, 'height': 360, 'xStart': xOffset + 580}
        ]
        
        self.drawBuildings(app, buildingSpecs)

    def drawBuildings(self, app, buildingSpecs):
        for spec in buildingSpecs:
            buildingColor = spec['color']
            buildingWidth = spec['width']
            buildingHeight = spec['height']
            xStart = spec['xStart']

            # Draw the building
            drawRect(xStart, app.height - buildingHeight,
                     buildingWidth, buildingHeight,
                     fill=buildingColor)

            # Define window properties
            windowXSpacing = 25
            windowYSpacing = 50
            windowWidth = 20
            windowHeight = 30

            yStart = app.height - buildingHeight

            # Draw windows with uniform spacing
            for y in range(yStart + windowYSpacing // 2,
                           app.height - windowHeight - windowYSpacing // 2,
                           windowYSpacing):
                for x in range(xStart + windowXSpacing // 2,
                               xStart + buildingWidth - windowWidth - windowXSpacing // 2,
                               windowXSpacing):
                    drawRect(x, y, windowWidth, windowHeight, fill='yellow')

# Initialize the Frames object



        
            

            




# MAIN MENU
# Collision Game Over Pause MENU
