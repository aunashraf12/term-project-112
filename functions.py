from cmu_graphics import *
from PIL import Image as PILImage
import pathlib, os
# from cmu_graphics.shape_logic import loadImageFromStringReference


BASE_SPRITE_URL = ("./templerun/") 
COLLECTIBLES = {"health" : "./Images/RedCross.png", "batarangs" : "./Images/Batarang.png","x2" : "./Images/x2 Score .png"}

def openImage(fileName):
    return PILImage.open(os.path.join(pathlib.Path(__file__).parent,fileName))

def animate(app):
    if app.action == "Hover":
        app.acton = "Slide"
    app.mainSpriteImages = [CMUImage(openImage(f'{BASE_SPRITE_URL}{app.action}__00{i}.png')) for i in range(10)]
    app.mainSpriteWidth, app.mainSpriteHeight = getImageSize(app.mainSpriteImages[app.mainSpriteIndex])
    

    # if app.sliding == False and app.jumping == False:
    #     drawImage(app.mainSpriteImages[app.mainSpriteIndex], app.mainChar.pos[0], app.mainChar.pos[1], align='center', width=app.mainSpriteWidth/4, height=app.mainSpriteHeight/4)
    # elif app.sliding == True:
    
    # elif app.jumping ==  True:
    #     drawImage(app.mainSpriteImages[app.mainSpriteIndex], app.mainChar.pos[0], app.mainChar.pos[1], align='center', width=app.mainSpriteWidth/4, height=app.mainSpriteHeight/4)

    if app.mainSpriteIndex == 9:
        app.mainSpriteIndex = 0
    else:
        app.mainSpriteIndex += 1




# from cmu_graphics import *
# from pillow import Image as PILImage


# BASE_SPRITE_URL = (r"D:/CMUQ/Fundamentals_of_Programming/Term_Project/112-term-project/templerun//") 
# COLLECTIBLES = {"health" : r"D:/CMUQ/Fundamentals_of_Programming/Term_Project/112-term-project/Images/RedCross.png", "batarangs" : r"D:/CMUQ/Fundamentals_of_Programming/Term_Project/112-term-project/Images/Batarang.png","x2" : r"D:/CMUQ/Fundamentals_of_Programming/Term_Project/112-term-project/Images/x2 Score .png"}


# def animate(app):
#     if app.action == "Hover":
#         app.acton = "Slide"
#     app.mainSpriteImages = [loadImageFromStringReference(f'{BASE_SPRITE_URL}{app.action}__00{i}.png') for i in range(10)]
#     app.mainSpriteWidth, app.mainSpriteHeight = getImageSize(app.mainSpriteImages[app.mainSpriteIndex])
    

#     # if app.sliding == False and app.jumping == False:
#     #     drawImage(app.mainSpriteImages[app.mainSpriteIndex], app.mainChar.pos[0], app.mainChar.pos[1], align='center', width=app.mainSpriteWidth/4, height=app.mainSpriteHeight/4)
#     # elif app.sliding == True:
    
#     # elif app.jumping ==  True:
#     #     drawImage(app.mainSpriteImages[app.mainSpriteIndex], app.mainChar.pos[0], app.mainChar.pos[1], align='center', width=app.mainSpriteWidth/4, height=app.mainSpriteHeight/4)

#     if app.mainSpriteIndex == 9:
#         app.mainSpriteIndex = 0
#     else:
#         app.mainSpriteIndex += 1