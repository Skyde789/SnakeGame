from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import random
import threading
import time
import math

#Making Position it's own class so it's clean
class Position:
    def __init__(self,posX,posY):
        self.x = posX
        self.y = posY
#Same here
class Player:
    def __init__(self):
        self.positionList = [Position(3,3)]
        self.length = 1
#and here
class Food:
    def __init__(self):
        self.position = Position(0,0)

#0 = left
#1 = up
#2 = right
#3 = down
direction = 2

player = Player()
food = Food()
sense = SenseHat()
sense.clear()

def MovePlayer(minAmount = 0, maxAmount = 7):
    global player
    global direction

    #Basic stuff mostly, move towards the direction, then add the new position to the list and remove the oldest one from the list for the snake effect
    if direction == 0:
        player.positionList.append(Position(player.positionList[-1].x - 1, player.positionList[-1].y))
        player.positionList.remove(player.positionList[0])
    if direction == 1:
        player.positionList.append(Position(player.positionList[-1].x, player.positionList[-1].y - 1))
        player.positionList.remove(player.positionList[0])
    if direction == 2:
        player.positionList.append(Position(player.positionList[-1].x + 1, player.positionList[-1].y))
        player.positionList.remove(player.positionList[0])
    if direction == 3:
        player.positionList.append(Position(player.positionList[-1].x, player.positionList[-1].y + 1))
        player.positionList.remove(player.positionList[0])
    
    #if we are out of bounds, we die
    if player.positionList[-1].x < minAmount or player.positionList[-1].x > maxAmount:
        Die()
        
    if player.positionList[-1].y < minAmount or player.positionList[-1].y > maxAmount:
        Die()
        
    CheckHit()
    UpdateLights()
    #Time between the moves
    time.sleep(max(0.15, 1 - (math.floor(player.length / 5) * 0.115)))
    
def UpdateLights():
    global player
    global food
    sense.clear()
    #for each position we have stored, set pixels to glow white in correct positions
    for pos in player.positionList:
        sense.set_pixel(pos.x, pos.y, 255,255,255)
    #same for the foodposition    
    sense.set_pixel(food.position.x, food.position.y, 0,255,0)

def SpawnFood():
    global food
    global player
    #Randomly generate a position for the food, if it overlaps with a player position, this loops until it doesn't overlap
    food.position.x = random.randint(0,7)
    food.position.y = random.randint(0,7)
    for pos in player.positionList:
        if food.position.x == pos.x and food.position.y == pos.y:
            SpawnFood()
            
def EatFood():
    global player
    #Add one to our score and add the current position to the positionList
    player.length = player.length + 1
    player.positionList.append(Position(player.positionList[-1].x, player.positionList[-1].y))
    #Also spawn the new food so the game continues lol
    SpawnFood()

def CheckHit():
    global player
    global food
    #Loops through every playerposition (except the latest one) and checks if we overlapped and should die
    i = 0
    if len(player.positionList) > 1:
        while i < len(player.positionList) - 1:
            if player.positionList[-1].x == player.positionList[i].x and player.positionList[-1].y == player.positionList[i].y:
                Die()
            i += 1
    #If we hit a food then eat it
    if player.positionList[-1].x == food.position.x and player.positionList[-1].y == food.position.y:
        EatFood()
    
def Die():
    global player
    sense.show_message("GG", text_colour=[255,0,0])
    sense.clear()
    i = 0
    while i < 3:
        time.sleep(1)
        if player.length < 10:
            sense.show_letter(str(player.length))
        else:
            sense.show_message(str(player.length))
        time.sleep(1)
        sense.clear()
        i += 1
    quit()
    
def PushLeft(event):
    global direction
    if event.action != ACTION_RELEASED or event.action != ACTION_HELD:
        direction = 0
def PushUp(event):
    global direction
    if event.action != ACTION_RELEASED or event.action != ACTION_HELD:
        direction = 1
def PushRight(event):
    global direction
    if event.action != ACTION_RELEASED or event.action != ACTION_HELD:
        direction = 2
def PushDown(event):
    global direction
    if event.action != ACTION_RELEASED or event.action != ACTION_HELD:
        direction = 3
        
SpawnFood()
UpdateLights()

while True:
    threading.Timer(1.0, MovePlayer())
    sense.stick.direction_left = PushLeft
    sense.stick.direction_up = PushUp
    sense.stick.direction_right = PushRight
    sense.stick.direction_down = PushDown
    
        