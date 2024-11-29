# from cmu_graphics import *

# class Frames:
#     def __init__(self):
#         self.currentFrame = 0  # Start with the first frame index
#         self.frameWidth = 800  # Width of each frame
#         self.frames = [self.drawFrame1, self.drawFrame2]  # List of frame drawing functions
#         self.xOffset = 0  # Horizontal offset for scrolling

#     def scrollRight(self):
#         # Move frames to the left by increasing xOffset
#         self.xOffset -= 5  # Adjust speed as needed

#         # Reset xOffset to loop frames infinitely
#         if self.xOffset <= -self.frameWidth:
#             self.xOffset = 0
#             # Swap frame order to simulate continuous scrolling
#             self.frames.append(self.frames.pop(0))

#     def drawFrames(self, app):
#         # Draw current and next frame for seamless transition
#         for i in range(2):  # Draw two frames at a time for smooth transition
#             with translate(i * self.frameWidth + self.xOffset, 0):
#                 self.frames[i]()

#     def drawFrame1(self):
#         # Draw sky for frame 1
#         drawRect(0, 0, app.width, app.height, fill='skyBlue')
        
#         # Define buildings for frame 1
#         building_specs = [
#             {'color': 'lightGray', 'width': 100, 'height': 300, 'x_start': 50},
#             {'color': 'darkGray', 'width': 120, 'height': 350, 'x_start': 210},
#             {'color': 'dimGray', 'width': 80, 'height': 250, 'x_start': 380},
#             {'color': 'slateGray', 'width': 90, 'height': 400, 'x_start': 510}
#         ]
        
#         self.drawBuildings(building_specs)

#     def drawFrame2(self):
#         # Draw sky for frame 2
#         drawRect(0, 0, app.width, app.height, fill='lightSkyBlue')
        
#         # Define buildings for frame 2
#         building_specs = [
#             {'color': 'darkSlateGray', 'width': 110, 'height': 320, 'x_start': 70},
#             {'color': 'gray', 'width': 130, 'height': 300, 'x_start': 240},
#             {'color': 'lightSlateGray', 'width': 90, 'height': 280, 'x_start': 410},
#             {'color': 'darkGray', 'width': 100, 'height': 360, 'x_start': 580}
#         ]
        
#         self.drawBuildings(building_specs)

#     def drawBuildings(self, building_specs):
#         for spec in building_specs:
#             building_color = spec['color']
#             building_width = spec['width']
#             building_height = spec['height']
#             x_start = spec['x_start']

#             # Draw the building
#             drawRect(x_start, app.height - building_height,
#                      building_width, building_height,
#                      fill=building_color)

#             # Define window properties
#             window_x_spacing = 25
#             window_y_spacing = 50
#             window_width = 20
#             window_height = 30

#             y_start = app.height - building_height

#             # Draw windows with uniform spacing
#             for y in range(y_start + window_y_spacing // 2,
#                            app.height - window_height - window_y_spacing // 2,
#                            window_y_spacing):
#                 for x in range(x_start + window_x_spacing // 2,
#                                x_start + building_width - window_width - window_x_spacing // 2,
#                                window_x_spacing):
#                     drawRect(x, y, window_width, window_height, fill='yellow')

# # Initialize the Frames object
# frames = Frames()

# def redrawAll(app):
#     frames.drawFrames(app)

# def onKeyHold(keys):
#     if "right" in keys:
#         frames.scrollRight()

# # Run the application with key hold event to scroll frames continuously
# runApp()

from cmu_graphics import *

class Frames:
    def __init__(self):
        self.currentFrame = 0  # Start with the first frame index
        self.frameWidth = 800  # Width of each frame
        self.xOffset = 0  # Horizontal offset for scrolling
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
app.frames = Frames()

def redrawAll(app):
    app.frames.drawFrames(app)

def onKeyHold(app, keys):
    if "right" in keys:
        app.frames.scrollRight()

runApp(800, 425)