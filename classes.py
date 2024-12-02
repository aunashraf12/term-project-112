from cmu_graphics import *
from cmu_graphics.shape_logic import loadImageFromStringReference
from functions import *
import random
import math

COLLECTIBLES = {"health" : r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\RedCross.png","x2" : r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\x2 Score .png", "batarangs" : r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\112-term-project\Images\batarangs.png"}
ATTACKER_1 = r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\term-project-112\Images\attacker1\tile00"
ATTACKER1_IMAGES = [loadImageFromStringReference(f'{ATTACKER_1}{i}.png') for i in range(8)]
ATTACKER_2 = r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\term-project-112\Images\attacker2\Idle.png"
DEAD = r"D:\CMUQ\Fundamentals_of_Programming\Term_Project\term-project-112\Images\deadAttacker\tile00"
DEAD_ATTACKER_IMAGES = [loadImageFromStringReference(f'{DEAD}{i}.png') for i in range(4)]

# LEVEL_1_ATTRIBUTES = {"ddy" : 1.15, "obstacleFrequency"  : 120, ""}


class MainChar:
    def __init__(self, app) -> None:
        self.steps = 0
        self.timer = 0
        self.width = app.mainSpriteWidth/6
        self.height = app.mainSpriteHeight/6
        self.ground = 390
        self.x = 200
        self.y = self.ground - self.height/2
        self.dx = 0
        self.dy = 0
        self.ddy = 1.25
        self.pos = [200, self.ground - self.height/2]
        self.finalPosY = self.y - 50 # The y position after the jump is made
        self.blinking = False

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
        if not self.blinking or (self.blinkTimer // 5) % 2 == 0:  # Blink every 5 frames
            drawImage(app.mainSpriteImages[app.mainSpriteIndex], app.mainChar.pos[0], app.mainChar.pos[1], align='center', width=app.mainSpriteWidth/6, height=app.mainSpriteHeight/6)


    def jump(self, app):
        # app.mainCharPosY = self.finalPosY
        # if not app.poles.checkIllegalColliding(app) == (False, "bottom"):
        app.animation = "Jump"
        if app.jumpCount == 1:
            app.mainChar.dy = -17
        if app.jumpCount == 2:
            app.mainChar.dy = -20
        app.jumping = True


    def update(self, app, movement=(0, 0)):
        self.collisions = {"up" : False, "down" : False, "right" : False, 
                           "left": False}
        
        # The amount the character wil move in one frame
        # frameMovement = (movement[0] + self.velocity[0], movement[1] + 
        #                  self.velocity[1])

        # self.pos[0] += frameMovement[0]

        if self.hover == False:
            self.dy += self.ddy  # Gravity
            self.pos[1] += self.dy  # Vertical movement
        else:
            self.dy += 0.15 * self.ddy  # 1/4 th Gravity for hovering
            self.pos[1] += self.dy  # Vertical movement

        if self.pos[1] + self.height//2 >= self.ground:
            self.pos[1] = self.ground - self.width//2
            self.dy = 0

        app.frames.scrollRight()

       

        # Check for collision with poles
        if app.poles.checkForMainChar(app):
            self.grounded(app)  # Reset jump count if on a pole


        for pole in app.poles.poles:
            if app.mainChar.pos[0] + app.mainChar.width // 2  >= pole[0]:         # Checking for collision with poles downwards
                if app.mainChar.pos[0] - app.mainChar.width // 2 <= pole[0] + pole[2]: 
                    if app.mainChar.pos[1] + app.mainChar.height // 2 >= pole[1] and app.mainChar.pos[1] - app.mainChar.height // 2 <= pole[1] + app.poles.height:
                        self.collisions["down"] = True

    
        # # self.velocity[1] = 3 if self.hover == True else 8 #min(5, self.velocity[1] + 0.1) # Gravity

        if self.collisions['down']:
            self.dy = 0


    def grounded(self, app):
        bottomOfChar = self.y + self.height // 2
        if self.collisions['down'] or app.mainChar.pos[1] + app.mainChar.height / 2 >= app.mainChar.ground:
            app.jumpCount = 0
            return True
        return False

        
    def swing(self, app, x, y):
        # Line
        drawLine(x, y, self.x, self.y)
        
        if app.swingingPivot == True and abs(app.swingingPivotX - app.mainCharX ) <= 100: # Now check with the space bar in OnkeyHold
            # Circular motion
            # Harcode the arc length values
            pass


    def startBlinking(self):
            """Start the blinking effect."""
            self.blinking = True
            self.blinkTimer = 0


    def onStep(self, app):
        # self.gravity(app)
        if not app.swinging:
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

        self.width = app.mainSpriteWidth/6 # As the sprites switch between running, sliding etc.
        self.height = app.mainSpriteHeight/6

        if self.blinking:
            self.blinkTimer += 1
            if self.blinkTimer >= 30:  # Blink for 30 frames
                self.blinking = False
                self.blinkTimer = 0

        


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
            pole[0] -= app.obstacleSpeed

    def removePole(self, app):
        for pole in self.poles[:]:
            if pole[0] + pole[2] <= 0:
                self.poles.remove(pole)
        return True


    def onStep(self, app):
        app.poleTimer += 1
        if app.poleTimer % app.obstacleFrequency == 0:
            app.poles.addPole(app)

        app.poles.animatePole(app)
        app.poles.removePole(app)
        
        app.poles.checkForMainChar(app)

        if app.mainChar.health <= 0:
            app.gameOver = True


    def checkForMainChar(self, app):
        for pole in self.poles:
            # Pole boundaries
            poleLeft = pole[0]
            poleRight = pole[0] + pole[2]
            poleTop = pole[1]
            poleBottom = pole[1] + self.height

            # Player boundaries
            playerLeft = app.mainChar.pos[0] - app.mainChar.width // 2
            playerRight = app.mainChar.pos[0] + app.mainChar.width // 2
            playerTop = app.mainChar.pos[1] - app.mainChar.height // 2
            playerBottom = app.mainChar.pos[1] + app.mainChar.height // 2

            # Check vertical collision (landing on a pole)
            if playerBottom >= poleTop and playerTop <= poleTop:
                if playerRight > poleLeft and playerLeft < poleRight:
                    app.mainChar.dy = 0  # Stop downward movement
                    app.mainChar.pos[1] = poleTop - app.mainChar.height // 2  # Align player on top of the pole
                    app.mainChar.grounded(app)
                    return True

            # Check horizontal collision (sideways movement into a pole)
            if playerRight > poleLeft and playerLeft < poleRight:
                if playerBottom > poleTop and playerTop < poleBottom:
                    # Push player to the left or right of the pole
                    if playerLeft < poleLeft:  # Colliding from the left
                        app.mainChar.pos[0] = poleLeft - app.mainChar.width // 2
                    elif playerRight > poleRight:  # Colliding from the right
                        app.mainChar.pos[0] = poleRight + app.mainChar.width // 2
                    app.mainChar.dx = 0  # Stop horizontal movement
                    return True

        return False



class pivots:
    def __init__(self, app) -> None:
        self.x = app.width # random between 300 and 500
        self.y = app.height / 2
        self.r = 10
        self.steps = 0
        self.pivots = []

    def addPivot(self, app):
        if len(self.pivots) == 0:
            self.pivots.append([self.x, self.y, self.r])

    def drawPivot(self, app):
        for pivot in self.pivots:
            drawCircle(pivot[0], pivot[1], self.r, fill="red")

    def removePivot(self, app):
        for pivot in self.pivots[:]:
            if pivot[0] + pivot[2] < 0:
                self.pivots.remove(pivot)


    def onStep(self, app):
        for pivot in self.pivots:
            pivot[0] -= 10
        self.steps += 1
        if self.steps % 120 == 0:
            self.addPivot(app)

        self.removePivot(app)

        for pivot in self.pivots:
            if abs(app.mainChar.pos[0] - pivot[0]) < 100:
                    app.swingingPivots.stopSwinging()



class swingingPivot:
    def __init__(self, length=150, swingRange=(-math.pi/4, math.pi/4)):
        self.length = length
        self.swingRange = swingRange
        self.angle = 0
        self.angularVelocity = 0
        self.gravity = 0.0005
        app.swinging = False

    def startSwinging(self, x, y):
        self.pivotX = x
        self.pivotY = y
        app.swinging = True

    def stopSwinging(self):
        app.swinging = False

    def update(self, player):
        if app.swinging:
            # Apply physics
            angularAcceleration = -self.gravity * math.sin(self.angle)
            self.angularVelocity += angularAcceleration
            self.angle += self.angularVelocity

            # Release if angle exceeds maximum right swing
            if self.angle >= self.swingRange[1]:
                app.swinging = False
                tangentialSpeed = self.angularVelocity * self.length
                app.mainChar.dx = tangentialSpeed * math.cos(self.angle)
                app.mainChar.dy = tangentialSpeed * math.sin(self.angle)
                return

            # Update player position
            app.mainChar.pos[0] = self.pivotX + self.length * math.sin(self.angle)
            app.mainChar.pos[1] = self.pivotY + self.length * math.cos(self.angle)

    def draw(self):
        if app.swinging:
            # Draw the rope
            drawLine(self.pivotX, self.pivotY, app.mainChar.pos[0], app.mainChar.pos[1], fill="black", lineWidth=2)

        # Draw the pivot
        drawCircle(self.pivotX, self.pivotY, 5, fill="red")

    def onStep(self, app):
        if app.swinging:
            self.update(app)

class Attacker:
    def __init__(self) -> None:
        self.animated = True
        self.attacker1Index = 0
        self.attacker2 = loadImageFromStringReference(f'{ATTACKER_2}')
        self.attackers = []
        self.dead = False
        self.touching = False
        self.steps = 0

    def setWidthHeight(self):
        if self.animated:
            self.width, self.height = getImageSize(ATTACKER1_IMAGES[self.attacker1Index])
        else:
            self.width, self.height = getImageSize(self.attacker2)

    def draw(self):
        for attacker in self.attackers:
            if attacker[2] != True:
                if attacker[-1]:  # If animated
                    drawImage(ATTACKER1_IMAGES[self.attacker1Index], attacker[0], attacker[1], align='center')
                else:
                    drawImage(self.attacker2, attacker[0], attacker[1], align="center")
            else:
                for image in DEAD_ATTACKER_IMAGES:
                    drawImage(image, attacker[0], attacker[1], align='center')

    def addAttacker(self, app):
        # Ensure width and height are set before adding attackers
        self.setWidthHeight()

        choice = random.choice([1, 2])
        if choice == 1:
            # Add attacker on the ground
            self.attackers.append([app.width + 5, app.mainChar.ground - self.height / 2,False , True]) # [xPos, yPos, dead, animated]
        else:
            # Add attacker on the first pole if it exists
            if app.poles.poles:
                pole = app.poles.poles[0]
                self.attackers.append([pole[0] + pole[2] // 2, pole[1] - self.width / 2, False, False])

    def moveAttacker(self, app):
        for attacker in self.attackers:
            if attacker[1] == app.mainChar.ground - self.height / 2:  # If on ground
                attacker[0] -= app.attackerSpeed
            elif app.poles.poles:  # Ensure poles exist before accessing
                pole = app.poles.poles[0]
                attacker[0] = pole[0] + pole[2] // 2  # Stay on the middle of the pole

    def removeAttacker(self):
        # Use list comprehension to filter out attackers that are off-screen
        self.attackers = [attacker for attacker in self.attackers if attacker[0] + self.width // 2 > 0]

    def touchingMainChar(self, app):
        rightX = app.mainChar.pos[0] + app.mainChar.width//2
        leftX = app.mainChar.pos[0] - app.mainChar.width//2
        topY =  app.mainChar.pos[1] - app.mainChar.height//2
        bottomY = app.mainChar.pos[1] + app.mainChar.height//2

        for attacker in self.attackers[:]:
            right2X = attacker[0] + self.width // 2
            left2X = attacker[0] - self.width // 2
            top2Y = attacker[1] - self.height // 2
            bottom2Y = attacker[1] + self.height // 2
            if leftX <= right2X - self.width//2 and rightX >= left2X + self.width // 2 and bottomY >= top2Y + self.height // 2 and topY <= bottom2Y and app.action != "Slide" and not self.touching and attacker[2] != True:
                print("colliding")
                app.mainChar.health -= 25 if attacker[-1] == True else 20
                self.touching = True
                return True
            elif self.touching == True and leftX > right2X or rightX < left2X or bottomY < top2Y or topY > bottom2Y: # Reverse of the above condition
                
                self.touching = False
                return False
                
        return False
    
    def checkForDeath(self, app):
        # Case 1 main char
        rightX = app.mainChar.pos[0] + app.mainChar.width//2
        leftX = app.mainChar.pos[0] - app.mainChar.width//2
        topY =  app.mainChar.pos[1] - app.mainChar.height//2
        bottomY = app.mainChar.pos[1] + app.mainChar.height//2

        for attacker in self.attackers[:]:
            right2X = attacker[0] + self.width // 2
            left2X = attacker[0] - self.width // 2
            top2Y = attacker[1] - self.height // 2
            bottom2Y = attacker[1] + self.height // 2
            if leftX <= right2X - self.width//2 and rightX >= left2X + self.width // 2 and bottomY >= top2Y + self.height // 2 and topY <= bottom2Y and app.action == "Slide" and not self.touching:
                attacker[2] = True
                return
                
        # Case 2 Batarang 
        for batarang in app.batarangs.curBatarangs:
            for attacker in self.attackers[:]:
                rightX = batarang[0] + app.batarangs.width//2
                leftX = batarang[0] - app.batarangs.width//2
                topY =  batarang[1] - app.batarangs.height//2
                bottomY = batarang[1] + app.batarangs.height//2

                right2X = attacker[0] + self.width // 2
                left2X = attacker[0] - self.width // 2
                top2Y = attacker[1] - self.height // 2
                bottom2Y = attacker[1] + self.height // 2


                if leftX <= right2X - app.batarangs.width//2 and rightX >= left2X + app.batarangs.width//2 and bottomY >= top2Y + app.batarangs.height//2 and topY <= bottom2Y and not self.touching:
                    attacker[2] = True
                    return


    def onStep(self, app):
        if self.steps % app.attackerFrequency == 0:
            self.addAttacker(app)
        
        # Update attackers' movement and remove off-screen ones
        self.moveAttacker(app)
        self.removeAttacker()

        # Update animation frame index
        if len(ATTACKER1_IMAGES) > 0:  # Ensure there are images to cycle through
            if self.attacker1Index >= len(ATTACKER1_IMAGES) - 1:
                self.attacker1Index = 0
            else:
                self.attacker1Index += 1

        # Increment steps counter
        self.steps += 1
        self.touchingMainChar(app)
        self.checkForDeath(app)




# Only in level 2        
class Boulder:
    def __init__(self):
        self.boulders = []  # Each boulder is [x, y, width, height]
        self.steps = 0
        self.touching = False

    def addBoulder(self, app):
        # Randomize position: ground or 200 pixels above
        x = app.width + 5
        y = app.mainChar.ground - 25 if random.choice([1, 2]) == 1 else app.mainChar.ground - 95
        self.boulders.append([x, y, 100, 50]) if len(self.boulders) <= 1 else [] # [x, y, width, height]

    def draw(self):
        for boulder in self.boulders:
            drawRect(boulder[0], boulder[1], boulder[2], boulder[3], fill="grey", border="black", align="center")

    def remove(self):
        for boulder in self.boulders[:]:
            if boulder[0] + boulder[2] < 0:
                self.boulders.remove(boulder) 

    

    def checkCollision(self, app):
        """Check for collision with the main character."""
        for boulder in self.boulders:
            boulderWidth, boulderHeight = boulder[2], boulder[3]
            boulderLeft, boulderTop = boulder[0] - boulderWidth // 2, boulder[1] - boulderHeight // 2
            boulderRight, boulderBottom = boulder[0] + boulderWidth // 2, boulder[1] + boulderHeight // 2

            playerLeft = app.mainChar.pos[0] - app.mainChar.width // 2
            playerRight = app.mainChar.pos[0] + app.mainChar.width // 2
            playerTop = app.mainChar.pos[1] - app.mainChar.height // 2
            playerBottom = app.mainChar.pos[1] + app.mainChar.height // 2

            # Collision detection
            if (playerRight >= boulderLeft and playerLeft <= boulderRight and
                playerBottom >= boulderTop and playerTop <= boulderBottom and 
                self.touching == False):
                print((playerRight, boulderLeft), (playerLeft, boulderRight), (playerBottom, boulderTop), (playerTop, boulderBottom))
                self.touching = True
                app.mainChar.health -= 15
                print("colliding with box")
                app.mainChar.startBlinking()  # Trigger blinking
                # self.boulders.remove(boulder)  # Remove the boulder after collision
            elif (playerRight < boulderLeft or playerLeft >= boulderRight or
                playerBottom <= boulderTop or playerTop >= boulderBottom):
                self.touching = False
            

    def onStep(self, app):
        self.checkCollision(app)
        self.steps += 1
        if self.steps % app.obstacleFrequency == 0:
            self.addBoulder(app)

        # Move boulders to the left
        for boulder in self.boulders:
            boulder[0] -= app.obstacleSpeed

        # Remove off-screen boulders
        self.boulders = [boulder for boulder in self.boulders if boulder[0] + boulder[2] > 0]

    



        
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
                if abs(quiz[0] - rightX) <= self.r - 2:
                    # print("collison")
                    app.mainChar.health -= 10
                    self.quizzes.remove(quiz)
                    return True
                
        return False
    
    def onStep(self, app):
        self.steps += 1
        if self.steps % app.obstacleFrequency == 0:
            self.add(app)
        for quiz in self.quizzes:
            quiz[0] -= app.obstacleSpeed + 3

        self.removeQuiz(app)
        self.touchingMainChar(app)




class collectibles:
    def __init__(self) -> None:
        self.collectibles = [] # 2-D array with the x and y position as well as the width and height of the images
        self.steps = 0
        self.timeFrequency = random.randint(10, 20)

    def addCollectible(self, app):
        if len(self.collectibles) == 0:
            myList = list(COLLECTIBLES.keys())
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
                if collectible[0] == "health":
                    app.mainChar.health = 100
                elif collectible[0] == "x2":
                    app.scoreDoubled = True # Remove this after some time passes by
                else:
                    app.mainChar.powerUps["batarangs"] += 3
                    # app.batarangs.initialiseBatrangsArray(app)
                
                self.collectibles.remove(collectible)


    def onStep(self, app):
        self.steps += 1
        if self.steps % (app.collectibleFrequency) == 0:
            self.addCollectible(app)

        
        self.animateCollectible(app)
        self.removeCollectible(app)
        self.detectCollectible(app)



class Batarang:
    def __init__(self, app) -> None:
        self.x = app.mainChar.pos[0]
        self.y = app.mainChar.pos[1]
        width, height = getImageSize(COLLECTIBLES["batarangs"])
        self.width, self.height = width / 8, height / 8
        self.batarangs = []
        self.curBatarangs = [] # if multiple thrown at once
        


    def initialiseBatrangsArray(self, app):
        # for _ in range(app.mainChar.powerUps["batarangs"]):
        self.batarangs = []
        while len(self.batarangs) < app.mainChar.powerUps["batarangs"]:
            self.batarangs.append([app.mainChar.pos[0], app.mainChar.pos[1]])


    def throwBatarang(self, app):
        
        if self.batarangs != []: #  app.mainChar.powerUps["batarangs"] > 0 and 
            app.batarangAngle = 0
            self.curBatarangs.append(self.batarangs.pop()) # + [app.batarangAngle])
            app.mainChar.powerUps["batarangs"] -= 1
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
        self.initialiseBatrangsArray(app)
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