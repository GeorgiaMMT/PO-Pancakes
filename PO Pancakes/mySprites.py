"""
Name: Georgia Moutafis-Tymcio
Date: June 13th 2024
Description: Module for my sprite classes"""

import pygame
import random
pygame.init()

class Player(pygame.sprite.Sprite):
  '''Sprite subclass for user-controlled Chef sprite.'''

  def __init__(self, screen):
    '''Initializer to set the image and position for the Chef Sprite. Takes the screen as a parameter.
    Sets direction instance variables, and a boolean instance variable determining if the sprite is in a valid area of the screen'''
    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    self.upImage = pygame.image.load("chefUp.png")
    self.downImage = pygame.image.load("chefDown.png")
    self.leftImage = pygame.image.load("chefLeft.png")
    self.rightImage = pygame.image.load("chefRight.png")

    self.dirX = 0
    self.dirY = 0

    self.image = self.downImage
    self.rect = self.image.get_rect()
    self.rect.centerx = screen.get_width() // 2
    self.rect.centery = screen.get_height() //2
    self.x = self.rect.left
    self.y = self.rect.top
    self.valid = True

  def goRight(self):
    '''Make the player move RIGHT, and change to chefRight'''
    self.image = self.rightImage
    self.dirY = 0
    self.dirX = 5

  def goLeft(self):
    '''Make the player move LEFT, and change to chefLeft'''
    self.image = self.leftImage
    self.dirY = 0
    self.dirX = -5

  def goUp(self):
    '''Make the player move UP, and change to chefUp'''
    self.image = self.upImage
    self.dirY = -5
    self.dirX = 0

  def goDown(self):
    '''Make the player move DOWN, and change to chefDown'''
    self.image = self.downImage
    self.dirY = 5
    self.dirX = 0

  def stopMoving(self):
    '''Make the player stop moving'''
    self.dirY = 0
    self.dirX = 0

  def restrictMovement(self):
    '''Makes the player no longer in a valid area to move'''
    self.valid = False

  def allowMovement(self):
    '''Makes the player in a valid area to move'''
    self.valid = True

  def update(self):
    '''Updates the location of the player'''
    if self.valid == True:
      self.x = self.rect.left
      self.y = self.rect.top

      self.rect.left += self.dirX
      self.rect.top += self.dirY
    else:
      #makes the user go back to the previous position. This is used if it collides with a boundary
      self.rect.left = self.x
      self.rect.top = self.y

class Stove(pygame.sprite.Sprite):
  '''Sprite subclass for stove sprite'''

  def __init__(self):
    '''Initializer to set the image and location for the Stove Sprite.'''
    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load("stove.png")
    self.rect = self.image.get_rect()
    self.rect.left = 0
    self.rect.top = 222

class Servery(pygame.sprite.Sprite):
  '''Sprite subclass for servery sprite'''

  def __init__(self, screen):
    '''Initializer to set the image and location for the Servery Sprite. Takes the screen as a parameter'''
    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load("servery.png")
    self.rect = self.image.get_rect()
    self.rect.left = 235
    self.rect.top = screen.get_height() - 85

class Garbage(pygame.sprite.Sprite):
  '''Sprite subclass for garbage sprite'''

  def __init__(self):
    '''Initializer to set the image and location for the Garbage Sprite. Takes the screen as a parameter'''
    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    self.image = pygame.image.load("garbage.png")
    self.rect = self.image.get_rect()
    self.rect.left = 513
    self.rect.top = 390


class ToppingStation(pygame.sprite.Sprite):
  '''Sprite subclass for the topping station sprite'''

  def __init__(self):
    '''Initializer to set the image for the topping station Sprite.  Sets a boolean instance variable to determine
    if the topping station is occupied by a pancake'''
    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    self.occupied = False

    self.image = pygame.image.load("toppingStation.png")
    self.rect = self.image.get_rect()
    self.rect.left = 235
    self.rect.top = 72

  def setOccupied(self):
    '''Makes the topping station become occupied'''
    self.occupied = True

  def resetOccupied(self):
    '''Makes the topping station no longer occupied'''
    self.occupied = False

class Boundary(pygame.sprite.Sprite):
  '''Sprite subclass for boundary sprites'''

  def __init__(self, coords1, coords2):
    '''Initializer to set the image and location for the boundary Sprite. Takes a tuple with the coordinates for where
    the boundary starts, and a tuple with the coordinates for where the boundary ends as its parameters.'''

    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    #creates a transparent rectangle based off the coordinates for the boundary
    self.image = pygame.Surface((coords2[0] - coords1[0], coords2[1] - coords1[1]))
    self.image.convert()
    self.image.set_colorkey((0, 0, 0))

    self.rect = self.image.get_rect()
    self.rect.left = coords1[0]
    self.rect.top = coords1[1]

class Pancake(pygame.sprite.Sprite):
  '''Sprite subclass for the Pancake Sprite'''

  def __init__ (self, xy, burnerNum):
    '''Initializer to set the image for the Pancake Sprite. Takes a tuple of the pancake’s x and y coordinates
    and an integer that represents which stove burner the pancake is on as its parameters. Sets boolean instance variables determining
    the status of the pancake (how cooked it is). Sets a boolean instance variable determining if the pancake is currently cooking and
    an instance variable that saves the time the pancake starts cooking. Sets boolean instance variables for if the pancake is getting
    dragged/clicked. Sets an instance variable determining which stove burner the pancake is on and the starting coords of the pancake.
    Sets boolean instance variables determining which toppings are on the pancake and a list containing these toppings.
    Sets a boolean instance variable determining if the pancake is at the topping station.'''


    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    self.uncooked = pygame.image.load("uncooked.png")
    self.cooked = pygame.image.load("cooked.png")
    self.burnt = pygame.image.load("burnt.png")
    self.stacked = pygame.image.load("stacked.png")
    self.cookedRotate = pygame.image.load("cookedRotated.png")

    self.isUncooked = True
    self.isHalfCooked = False
    self.isCooked = False
    self.isCookedRotated = False
    self.isBurnt = False
    self.isFlipped = False
    self.isStacked = False

    self.burnerNum = burnerNum
    self.isCooking = False
    self.startTime = 0

    self.isDrag = False
    self.isClick = False

    self.chocolateSauce = False
    self.butter = False
    self.blueberries = False
    self.whippedCream = False
    self.toppingsList = []

    self.atToppings = False

    self.image = self.uncooked
    self.rect = self.image.get_rect()
    self.startingCoords = xy
    self.rect.left,  self.rect.top = xy

  def startDrag(self):
    '''Allows the pancake sprite to start to be dragged'''

    if self.rect.collidepoint(pygame.mouse.get_pos()):
      if self.isCooked or self.isBurnt:
        self.isDrag = True

  def setDrag(self):
    '''Stops the pancake sprite from being dragged'''
    self.isDrag = False

  def setClick(self):
    '''Validate that the pancake sprite was clicked'''

    if self.rect.collidepoint(pygame.mouse.get_pos()) and self.isHalfCooked == True:
      self.isClick = True

  def setCooking(self):
    '''Sets the boolean instance variable determining whether the pancake is currently cooking
    to True and assigns the current time to the startTime instance variable'''

    self.isCooking = True
    self.startTime = pygame.time.get_ticks()

  def cookPancakes(self, currentTime, bell, alarm):
    '''Changes boolean instance variables associated with the status of the pancake (how cooked it is). Takes the currentTime,
    the bell sound effect, and the alarm sound effect as parameters.'''

    #verifies if the pancake is on the second side
    if self.isCooking and self.isFlipped:
        #verifies if the pancake has been cooking for over 15 seconds
        if currentTime - self.startTime >= 15000:
          self.isBurnt = True
          alarm.play()
        #verifies if the pancake has been cooking for over 5 seconds
        elif currentTime - self.startTime >= 5000:
          self.isCooked = True
          bell.play()

    #verifies if the pancake is on the first side
    elif self.isCooking and self.isFlipped == False:
        #verifies if the pancake has been cooking for over 15 seconds
        if currentTime - self.startTime >= 15000:
            self.isBurnt = True
            alarm.play()
        #verifies if the pancake has been cooking for over 5 seconds
        elif currentTime - self.startTime >= 5000:
            self.isHalfCooked = True
            bell.play()

  def flipPancake(self):
    '''Sets the isFlipped boolean variable to True and resets the start time on the flipped side if the sprite is clicked'''
    if self.isClick:
      self.startTime = pygame.time.get_ticks()
      self.isFlipped = True
      self.isClick = False

  def setPancake(self):
    '''Sets the pancake location, sets the topping station instance variable as True, and sets the isCooking instance variable as False'''

    self.atToppings = True
    self.rect.left = 290
    self.rect.top = 85
    self.isCooking = False
    self.isCookedRotated = True

  def resetToStove(self, xy):
      '''resets the pancake's location to the stove. Takes a tuple of xy coordinates as a parameter'''

      self.rect.left, self.rect.top = xy

  def addTopping(self, topping):
    '''Adds a topping to the pancake. Takes the image name of a topping as a parameter and changes the associated boolean instance variable'''

    if topping == "chocolateSauce.png":
      self.chocolateSauce = True
    if topping == "butterSlice.png":
      self.butter = True
    if topping == "blueberries.png":
      self.blueberries = True
    if topping == "whippedCream.png":
      self.whippedCream = True


  def resetAtToppings(self):
    '''sets the boolean instance variable atToppings as False'''
    self.atToppings = False

  def update(self):
    '''Updates the sprite's image and location, as well as the toppings on the pancake'''

    #if the isDrag variable is True, the pancakes center follows the mouse
    if self.isDrag:
      self.rect.center = pygame.mouse.get_pos()

    #changes the image
    if self.isStacked:
      self.image = self.stacked
    elif self.isCookedRotated:
         self.image = self.cookedRotate
    elif self.isBurnt:
      self.image = self.burnt
    elif self.isCooked:
       self.image = self.cooked
    elif self.isHalfCooked and self.isFlipped == False:
       self.image = self.cooked
    elif self.isUncooked:
      self.image = self.uncooked

    #updates the topping list
    self.toppingsList = [self.isStacked, self.chocolateSauce, self.butter, self.blueberries, self.whippedCream]

    #blits the toppings onto the pancakes
    if self.chocolateSauce:
        self.image.blit(pygame.image.load("chocolateSauce.png"), (15, 11))
    if self.butter:
        self.image.blit(pygame.image.load("butterSlice.png"), (15, 11))
    if self.blueberries:
        self.image.blit(pygame.image.load("blueberries.png"), (15, 11))
    if self.whippedCream:
        self.image.blit(pygame.image.load("whippedCream.png"), (15, 11))


class Toppings(pygame.sprite.Sprite):
  '''Sprite subclass for toppings'''

  def __init__(self, imageName, x, y):
    '''Initializer to set the image for the toppings Sprite.
    Takes the name of the image as a string, the x coordinate for the topping location as an integer,
    and the y coordinate for the topping location as an interger as its parameters. Sets a boolean instance
    variable for if the topping is clicked and an instance variable for the topping's image name'''

    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    self.imageName = imageName
    self.image = pygame.image.load(imageName)

    self.rect = self.image.get_rect()
    self.rect.left = x
    self.rect.top = y

    self.clicked = False

  def setClicked(self):
    '''validates if the topping has been clicked.'''

    if self.rect.collidepoint(pygame.mouse.get_pos()):
      self.clicked = True

  def resetClick(self):
      '''makes the topping no longer be clicked'''
      self.clicked = False

class Orders(pygame.sprite.Sprite):
  '''Sprite subclass for orders'''

  def __init__(self, x, y):
    '''Initializer to set the image and location for the Orders Sprite.
    Takes the x and y coordinates as parameters. Creates instance variables for
    the different images of toppings, a random number, a list of toppings, and a boolean
    instance variable for if the order has been clicked. Randomly sets the toppings as True or False.'''
    # Call the parent __init__() method
    pygame.sprite.Sprite.__init__(self)

    self.orderImage = pygame.image.load("order.png")
    self.orderDetails = pygame.image.load("orderDetails.png")

    self.image = self.orderImage
    self.image.convert()
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    self.rect.top = y
    self.rect.left = x

    #sets the image for the different toppings and scales the image to be larger
    self.chocolateSyrupImage = pygame.transform.scale(pygame.image.load("chocolateSauce.png"), (80, 30))
    self.butterImage = pygame.transform.scale(pygame.image.load("butterSlice.png"), (55, 55))
    self.blueberriesImage = pygame.transform.scale(pygame.image.load("blueberries.png"), (55, 55))
    self.whippedCreamImage = pygame.transform.scale(pygame.image.load("whippedCream.png"), (55, 55))
    self.pancakeImage = pygame.transform.scale(pygame.image.load("cooked.png"), (100, 60))
    self.stackedPancakeImage = pygame.transform.scale(pygame.image.load("stacked.png"), (100, 60))

    self.random = 0
    self.toppings = []

    self.clicked = False

    #randomly sets the toppings as True or False
    for item in range(5):
      self.random = random.randint(0, 1)
      self.toppings.append(bool(self.random))
    self.stacked, self.chocolateSyrup, self.butter, self.blueberries, self.whippedCream = self.toppings

  def openOrder(self):
    '''Verifies if the sprite has been clicked and updates it's image and location'''

    if self.rect.collidepoint(pygame.mouse.get_pos()):
      self.clicked = True
      self.image = self.orderDetails
      self.rect.left = 440
      self.rect.top = 70

  def closeOrder(self):
    '''Verifies if the sprite has been clicked again and updates it's image and location'''
    if self.clicked == True and self.rect.collidepoint(pygame.mouse.get_pos()):
        self.clicked = False
        self.image = self.orderImage
        self.rect.left = self.x
        self.rect.top = self.y

  def update(self):
    '''Updates the sprite's image and location'''

    #if the order is clicked for a first time, the images of the toppings that are True for the order are blitted onto the order sprite
    if self.clicked:
      if self.chocolateSyrup:
        self.image.blit(self.chocolateSyrupImage, (20, 45))
      if self.butter:
        self.image.blit(self.butterImage, (125, 30))
      if self.blueberries:
        self.image.blit(self.blueberriesImage, (20, 130))
      if self.whippedCream:
        self.image.blit(self.whippedCreamImage, (125, 130))
      if self.stacked:
        self.image.blit(self.stackedPancakeImage, (55, 210))
      else:
        self.image.blit(self.pancakeImage, (55, 210))

class LifeKeeper(pygame.sprite.Sprite):
  '''Sprite subclass lifeKepper to display the current lives'''

  def __init__(self):
      '''Initializer to set the font and score for our Sprite. Sets an instance variable
      for the amount of lives'''

      # Call the parent __init__() method
      pygame.sprite.Sprite.__init__(self)
      self.font = pygame.font.Font("CHERL.TTF", 30)
      self.lives = 3

  def removeLife(self):
      '''removes a life from the counter'''
      self.lives -= 1

  def update(self):
      '''Render and center the scorekeeper text on each Refresh. Displays the amount of lives'''
      self.image = self.font.render("Lives: " + str(self.lives), 1, (0, 0, 0))
      self.rect = self.image.get_rect()
      self.rect.centerx = 560
      self.rect.centery = 50

class ScoreKeeper(pygame.sprite.Sprite):
  '''Sprite subclass ScoreKeeper to display the current points'''

  def __init__(self):
      '''Initializer to set the font and score for our Sprite. Sets an instance variable for
      the amount of points'''

      # Call the parent __init__() method
      pygame.sprite.Sprite.__init__(self)
      self.font = pygame.font.Font("CHERL.TTF", 30)
      self.points = 0

  def addPoint(self):
      '''Add a point to the score to be displayed.'''
      self.points += 5

  def update(self):
      '''Render and center the scorekeeper text on each Refresh. Displays the amount of points'''
      self.image = self.font.render("Score: " + str(self.points), 1, (0, 0, 0))
      self.rect = self.image.get_rect()
      self.rect.centerx = 560
      self.rect.centery = 15

