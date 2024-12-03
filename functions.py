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
    

    if app.mainSpriteIndex == 9:
        app.mainSpriteIndex = 0
    else:
        app.mainSpriteIndex += 1


