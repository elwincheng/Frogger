import pygame, sys, random
# Made by Elwin Cheng
pygame.init() # initialize pygame, is required.
width, height = 750, 700 # make variables for height and width of display

display = pygame.display.set_mode((width, height)) # Creates the display
pygame.display.set_caption("Frogger") # this will show up on the top left of the display screen

froggyImage = pygame.image.load('transparentBabyFrog.png')
logImage = pygame.image.load('bigLog.png')
beachImage = pygame.image.load('beach.png')
oceanImage = pygame.image.load('ocean.jpg')

clock = pygame.time.Clock() # Will use this later to limit FPS

velocities = [] # generate velocity for each log row
for i in range(7):
    num = random.random()
    speed = random.random() * 2 + 1
    if num < 0.5:
        velocities.append(speed*-1)
    else:
        velocities.append(speed)


logList = [] # generate logs
for y in range(7):
    logs = []
    x = 0
    while x < 650:
        length = int(random.random() * 150 + 50) # create random length of rectangle between 50 and 200
        dist = int(random.random() * 80 + 50) # create random distance between rectangles between 50 and 130
        logs.append(pygame.Rect(x+dist, y*70+110, length, 50)) # add a rectangle object, which represents a log, to the row of logs
        x += length + dist # increase x so that next rectangle is farther apart than the last
    logList.append(logs) # add the row of logs to logList

rotatedFroggyImage = froggyImage

beach = pygame.Rect(0, 0, width, 80)
island = pygame.Rect(0, height-80, width, 80)
white = (255,255,255)
black = (0,0,0)
froggy = pygame.Rect(int(width/2),height-80,40,40)
green = (0,255,0)
dir = 1
jumpCount = 11
frogSpeed = 0
pygame.time.delay(6000)

run = True
while run: # main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # check if exit button is pressed
            run = False
        if event.type == pygame.KEYDOWN: # check if a key is pressed
            if event.key == pygame.K_UP:
                rotatedFroggyImage = froggyImage
                jumpY = True # to know if jumping in y or x plane
                jumpCount = 0
                dir = 1 # direction of jump
            if event.key == pygame.K_DOWN:
                rotatedFroggyImage = pygame.transform.rotate(froggyImage, 180)
                jumpY = True
                jumpCount = 0
                dir = -1
            if event.key == pygame.K_LEFT:
                rotatedFroggyImage = pygame.transform.rotate(froggyImage, 90)
                jumpY = False
                jumpCount = 0
                dir = 1
            if event.key == pygame.K_RIGHT:
                rotatedFroggyImage = pygame.transform.rotate(froggyImage, 270)
                jumpY = False
                jumpCount = 0
                dir = -1
        if jumpCount < 10: # check if a button has been pressed
            d = (-(jumpCount-3)**2 + 10) * dir * 10 # jump distance is calculated
            if jumpY: # jump in x plane
                froggy.y -= d # change froggy's y coordinate
            else: # jump in y plane
                froggy.x -= d # change froggy's x coordinate
            jumpCount += 1



    #pygame.draw.rect(display, white, island) # tell pygame to draw the island rectangle with white color onto the display
    #pygame.draw.rect(display, white, beach)  # tell pygame to draw the beach rectangle with white color onto the display

    display.blit(oceanImage, (0, 0))
    scaledBeachImage = pygame.transform.scale(beachImage, beach.size)
    display.blit(scaledBeachImage, beach)
    display.blit(scaledBeachImage, island)

    landed = False
    for row in range(7): # loop through logs, update their position, check if they collide with froggy, reloop them, and draw them
        for log in logList[row]:
            if log.colliderect(froggy):
                frogSpeed = velocities[row]
                landed = True
            # pygame.draw.rect(display, white, log)  # # tell pygame to draw every log rectangle with white color onto the display
            scaledlogImage = pygame.transform.scale(logImage, log.size)
            display.blit(scaledlogImage, log)


            if velocities[row] < 0:
                if log.right <= 0:
                    log.left = width
            else:
                if log.left >= width:
                    log.right = 0
            log.x += int(velocities[row])

    if not landed:
        frogSpeed = 0
        if froggy.bottom < height-80 and froggy.top > 80: # game over
            run = False
    if froggy.left >= width or froggy.right <= 0: # game over
        run = False

    froggy.x += int(frogSpeed)
    #pygame.draw.rect(display,green, froggy) # draw froggy
    display.blit(rotatedFroggyImage,froggy)
    pygame.display.flip() # display everthing onto the screen



    clock.tick(60) # set 60 FPS

sys.exit()
pygame.quit() # quit pygame
