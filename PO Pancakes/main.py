"""
Name: Georgia Moutafis-Tymcio
Date: June 13th 2024
Description: A cooking simulator game. You are a chef in a kitchen and you must get as many points
as you can by completing as many orders as possible. If you get 3 orders wrong, you lose the game."""

# I - Import and Initialize
import pygame
import mySprites
pygame.init()
pygame.mixer.init()


def main():
    '''This is my mainline logic'''
    # D - Display configuration
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("PO Pancakes")

    # E - Entities (just background for now)
    background = pygame.Surface(screen.get_size())
    background = pygame.image.load("myKitchen.png")
    background.convert()
    screen.blit(background, (0, 0))

    player = mySprites.Player(screen)
    stove = mySprites.Stove()
    servery = mySprites.Servery(screen)
    garbage = mySprites.Garbage()
    toppingStation = mySprites.ToppingStation()

    upBoundary = mySprites.Boundary((0, 0), (640, 100))
    leftBoundary = mySprites.Boundary((0, 0), (50, 480))
    boundaryServery = mySprites.Boundary((255, 395), (485, 480))
    boundaryGarbage = mySprites.Boundary((540, 400), (600, 490))
    rightEdge = mySprites.Boundary((639, 0), (640, 479))
    bottomEdge = mySprites.Boundary((0, 475), (639, 479))
    boundaries = pygame.sprite.OrderedUpdates(leftBoundary, upBoundary, boundaryServery, boundaryGarbage, rightEdge, bottomEdge)

    pancakeGroup = pygame.sprite.OrderedUpdates()

    butter = mySprites.Toppings("butterSlice.png", 181, 104)
    chocolateSauce = mySprites.Toppings("chocolateSauce.png", 116, 108)
    blueberries = mySprites.Toppings("blueberries.png", 454, 106)
    whippedCream = mySprites.Toppings("whippedCream.png", 506, 108)

    toppingGroup = pygame.sprite.OrderedUpdates(butter, chocolateSauce, blueberries, whippedCream)

    order = mySprites.Orders(50, 15)
    myOrders = pygame.sprite.OrderedUpdates(order)

    score = mySprites.ScoreKeeper()
    lives = mySprites.LifeKeeper()
    allSprites = pygame.sprite.OrderedUpdates(stove, servery, garbage, toppingStation, boundaries, pancakeGroup,\
    toppingGroup, myOrders, score, lives, player)

    gameover = pygame.image.load("gameover.png")
    gameover = gameover.convert()

    pygame.mixer.music.load("Papa's Background.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

    pop = pygame.mixer.Sound("pop.wav")
    pop.set_volume(0.6)

    bell = pygame.mixer.Sound("bell.wav")
    bell.set_volume(0.4)
    alarm = pygame.mixer.Sound("alarm.wav")
    alarm.set_volume(0.8)
    error = pygame.mixer.Sound("error.wav")
    error.set_volume(1)
    correct = pygame.mixer.Sound("correct.wav")
    correct.set_volume(0.7)
    # A - Action (broken into ALTER steps)

        # A - Assign values to key variables
    clock = pygame.time.Clock()
    keepGoing = True
    burnerPositions = [(6, 410), (6, 327), (6, 244)]
    burnersOccupied = [False, False, False]

        # L - Loop
    while keepGoing:

        # T - Timer to set frame rate
        clock.tick(30)

        #variable constantly updating to get the current tick time
        currentTime = pygame.time.get_ticks()

        # E - Event handling

        #checks if the player collides with a boundary
        if pygame.sprite.spritecollide(player, boundaries, False):
            player.restrictMovement()
        else:
            player.allowMovement()

        #iterates through each pancake in the pancake group
        for pancake in pancakeGroup:

            #checks if a pancake collides with the topping station and if it's empty/if itself is already there
            if pancake.rect.colliderect(toppingStation.rect) and ((pancake.atToppings and toppingStation.occupied)\
            or (not pancake.atToppings and not toppingStation.occupied)):
                pancake.setPancake()
                toppingStation.setOccupied()
                burnersOccupied[pancake.burnerNum] = False
            #changes the atToppings variable to False and makes the toppingStation no longer occupied if the pancake gets moved off the topping station
            elif pancake.atToppings and not pancake.rect.colliderect(toppingStation.rect):
                pancake.resetAtToppings()
                toppingStation.resetOccupied()

            #checks if a pancake collides with another pancake at the topping station to stack pancakes
            for pancake2 in pancakeGroup:
                if pancake.rect.colliderect(pancake2.rect) and pancake != pancake2 and pancake.atToppings and not pancake.isStacked\
                and not pancake2.isStacked:
                    pancake2.kill()
                    pop.play()
                    pancake.isStacked = True
                    burnersOccupied[pancake2.burnerNum] = False
                    burnersOccupied[pancake.burnerNum] = False
                    break

            #checks if a pancake collides with the garbage can
            if pancake.rect.colliderect(garbage.rect):
                pancake.kill()
                burnersOccupied[pancake.burnerNum] = False

            #checks if a pancake collides with the servery
            if pancake.rect.colliderect(servery.rect):
                for orders in myOrders:
                    #checks if the pancake matches with the order
                    if pancake.toppingsList == orders.toppings:
                        score.addPoint()
                        correct.play()
                        orders.kill()
                        #creates new order
                        newOrder = mySprites.Orders(50, 15)
                        myOrders.add(newOrder)
                        allSprites.add(newOrder)
                    else:
                        lives.removeLife()
                        error.play()

                #resets the toppings
                for topping in toppingGroup:
                    topping.resetClick()
                burnersOccupied[pancake.burnerNum] = False
                pancake.kill()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.goRight()
                if event.key == pygame.K_LEFT:
                    player.goLeft()
                if event.key == pygame.K_UP:
                    player.goUp()
                if event.key == pygame.K_DOWN:
                    player.goDown()

                #creates a pancake and places it on an unoccupied stove burner
                if event.key == pygame.K_a and player.rect.left <= stove.rect.right + 25:
                    for i in range(3):
                        if burnersOccupied[i] == False:
                            newPancake = mySprites.Pancake(burnerPositions[i], i)
                            pop.play()
                            pancakeGroup.add(newPancake)
                            allSprites = pygame.sprite.OrderedUpdates(stove, servery, garbage, toppingStation, boundaries, pancakeGroup,\
    toppingGroup, myOrders, score, lives, player)
                            allSprites.add(newPancake)
                            newPancake.setCooking()
                            burnersOccupied[i] = True
                            break

                #flips the pancake
                if event.key == pygame.K_f:
                    for pancake in pancakeGroup:
                        pancake.flipPancake()

                #adds a topping
                if event.key == pygame.K_a and player.rect.top <= toppingStation.rect.bottom + 40 and toppingStation.occupied:
                    for pancake in pancakeGroup:
                        for topping in toppingGroup:
                            if pancake.atToppings and topping.clicked:
                                pancake.addTopping(topping.imageName)

            #stops player movement
            if event.type == pygame.KEYUP:
                player.stopMoving()

            if event.type == pygame.MOUSEBUTTONDOWN:

                #drags pancake
                for pancake in pancakeGroup:
                    pancake.setDrag()

                #opens/closes the orders if clicked
                for orders in myOrders:
                    orders.openOrder()
                    orders.closeOrder()

            #checks if the player clicks a pancake within the range of the stove
            if event.type == pygame.MOUSEBUTTONDOWN and player.rect.left <= stove.rect.right + 25:
                for pancake in pancakeGroup:
                    pancake.setClick()

            #checks if the player clicks a topping
            if event.type == pygame.MOUSEBUTTONDOWN and player.rect.top <= toppingStation.rect.bottom + 25:
                for topping in toppingGroup:
                    topping.setClick()
            if event.type == pygame.MOUSEBUTTONUP:

                #iterates through each pancake in the pancake group
                for pancake in pancakeGroup:
                    #stops the pancake from being moved while the mouse button is not held down
                    pancake.resetDrag()

                    #resets the pancake to its previous position if it's dragged somewhere and does not collide with anything
                    if not pancake.atToppings and not pancake.isCookedRotated:
                        pancake.resetToStove(burnerPositions[pancake.burnerNum])
                    elif not pancake.atToppings and (pancake.isCookedRotated or pancake.isStacked):
                        pancake.setPancake()

        for pancake in pancakeGroup:
            #cooks each pancake that is on the stove
            pancake.cookPancakes(currentTime, bell, alarm)

        #stops the game when the player loses all their lives
        if lives.lives == 0:
            keepGoing = False

        # R - Refresh display
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        pygame.display.flip()

    #displays the game over screen
    screen.blit(gameover, (0, 0))
    pygame.display.flip()
    pygame.mixer.music.fadeout(3000)

    # Close the game window
    pygame.time.delay(3000)
    pygame.quit()

main()
