import turtle
import math
import random

#Set up initial screen
wn = turtle.Screen()
wn.setup(width=600, height=600)
wn.title("Space Shooter Game")
wn.bgcolor('black')
turtle.color('white')
turtle.write("< SPACE SHOOTER GAME > \nPress R to start \nLeft Key - Turn Left \nRight Key - Turn Right \nSpace Bar - Shoot",False,align = "center", font = ("Courier", 24, "normal"))
turtle.hideturtle()
# Stop screen updates
wn.tracer(0)

# Create Shooter shape
shooter_vertices = ((0,15),(-15,0),(-18,5),(-18,-5),(0,0),(18,-5),(18, 5),(15, 0))
wn.register_shape("player",shooter_vertices)

#Create asteroid shape
asteroid_vertices = ((0, 10), (5, 7), (3,3), (10,0), (7, 4), (8, -6), (0, -10), (-5, -5), (-7, -7), (-10, 0), (-5, 4), (-1, 8))
wn.register_shape("asteroid",asteroid_vertices)


#Create class 'Sprite'
class Sprite(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        #Set attributes to sprites
        self.speed(0)
        self.penup()

#Create Function to determine direction 
def get_direction(s1, s2):
    x1 = s1.xcor()
    y1 = s1.ycor()
    
    x2 = s2.xcor()
    y2 = s2.ycor()
    
    direction = math.atan2(y1 - y2, x1 - x2)
    direction = direction * 180.0 / math.pi
    
    return direction

#Create variable for shooter and scoreboard
player = Sprite()
player.color("lightslateblue")
player.shape("player")
pen = Sprite()
pen.color("white")

# Set missile
missiles = []
for i in range(3):
    missile = Sprite()
    missile.color("lawngreen")
    missile.shape("square")
    missile.shapesize(stretch_wid = 0.3,stretch_len=0.7)
    missile.speed = 1
    missile.state = "ready"
    missile.hideturtle()
    missiles.append(missile)

#Create function for resetting of scoreboard
def set_scoreboard(pen):
    pen.goto(0, 250)
    pen.write("Score: 0", False, align = "center", font = ("Courier", 24, "normal"))
    pen.hideturtle()

#Create function for resetting of asteroid
def set_asteroids(asteroids):
    for i in range(7):   
        asteroid = Sprite()
        asteroid.color("Darkkhaki")
        asteroid.shape("asteroid")
        asteroid.speed = random.randint(3,6)/100
        asteroid.goto(0, 0)
        heading = random.randint(0, 360)
        distance = random.randint(300, 400)
        asteroid.setheading(heading)
        asteroid.forward(distance)
        asteroid.setheading(get_direction(player, asteroid))
        asteroids.append(asteroid)
        asteroid.speed += 0.001


# Create functions for different commands    
def rotate_left():
    player.left(15)
    
def rotate_right():
    player.right(15)
    
def fire_missile():
    for missile in missiles:
        if missile.state == "ready":
            missile.goto(0, 0)
            missile.showturtle()
            missile.setheading(player.heading())
            missile.state = "fire"
            break

#Main Game function
def start_game():
    #Reset Game
    turtle.hideturtle()
    turtle.clear()
    asteroids = []
    pen.clear()
    wn.bgcolor('black')
    wn.tracer(0)
    player.score = 0
    player.goto(0, 0)
    player.showturtle()
    set_scoreboard(pen)
    set_asteroids(asteroids)
    Game_Over = False
    count = 0
    #Main game loop
    while Game_Over == False:
        # Do screen update
        wn.update()
        # Set keys for respective commands
        wn.listen()
        wn.onkey(rotate_left, "Left")
        wn.onkey(rotate_right, "Right")
        wn.onkey(fire_missile, "space")
    
        # Move the missile
        for missile in missiles:
            if missile.state == "fire":
                missile.forward(missile.speed)
        
            # Check for borders
            if missile.xcor() > 300 or missile.xcor() < -300 or missile.ycor() > 300 or missile.ycor() < -300:
                missile.hideturtle()
                missile.state = "ready"
                

        # Iterate through asteroids
        for asteroid in asteroids:    
            # Move the asteroid
            asteroid.forward(asteroid.speed)

        
        # Check for collisions
            # Asteroid and Player
            if asteroid.distance(player) < 20:
                # Reset Asteroid
                heading = random.randint(0, 360)
                distance = random.randint(400, 600)
                asteroid.setheading(heading)
                asteroid.forward(distance)
                asteroid.setheading(get_direction(player, asteroid))
                Game_Over = True
                pen.clear()
                pen.write("Score: {}".format(player.score), False, align = "center", font = ("Courier", 24, "normal"))
                
            # Asteroid and Missile
            for missile in missiles:
                if asteroid.distance(missile) < 20:
                    # Reset Asteroid
                    heading = random.randint(0, 360)
                    distance = random.randint(300, 400)
                    asteroid.setheading(heading)
                    asteroid.forward(distance)
                    asteroid.setheading(get_direction(player, asteroid))
                    
                    
                    # Reset Missile
                    missile.goto(600, 600)
                    missile.hideturtle()
                    missile.state = 'ready'
                    
                    # Increase score
                    player.score += 10
                    count +=1
                    pen.clear()
                    pen.write("Score: {}".format(player.score), False, align = "center", font = ("Courier", 24, "normal"))


        #Set Game Over screen    
        if Game_Over == True:
            player.hideturtle()
            missile.hideturtle()
            for a in asteroids:
                a.hideturtle()
            pen.clear()
            #wn.clear()
            wn.bgcolor('black')
            pen.write("Press R to restart",False,align = "center", font = ("Courier", 24, "normal"))
            turtle.color('firebrick1')
            turtle.write('GAME OVER!',False,align = "center", font = ("Courier", 50, "bold"))
            break
            
            
#Set command to restart Game            
wn.listen()
wn.onkey(start_game,'r')

wn.mainloop()