import sys
# import gl, GL, time
import numpy as np
from numpy.random import randint
from turtle import *
from time import sleep

scale_factor = 10


class Prey:

    def __init__(self, radius=float(scale_factor)/3, color=["red", "red"]):

        self.color = color
        self.radius = radius
        self.prey = Turtle()
        self.prey.hideturtle()
        self.prey.color(color[0], color[1])
        self.prey.penup()
        self.prey.speed("fastest")
        # self.prey.pensize(float(scale_factor)/2)
        self.pos = None


    def __del__(self):

        self.prey.clear()


    def set_pos(self, position):

        self.prey.clear()
        self.pos = position
        # self.prey.setposition(self.pos)
        self.prey.goto((self.pos[0] - float(scale_factor)/8, self.pos[1] - float(scale_factor)/8))
        self.prey.pendown()
        # self.prey.dot()
        # self.prey.begin_fill()
        # self.prey.circle(self.radius)
        # self.prey.end_fill()
        self.prey.begin_fill()
        for _ in range(4):
            self.prey.forward(float(scale_factor)/4)
            self.prey.left(90)
        self.prey.end_fill()
        self.prey.penup()


class Snake:


    def __init__(self, width=100*scale_factor, height=100*scale_factor, max_score=100):

        self.max_score = 100
        self.height = height
        self.width = width
        self.snake = Turtle()
        self.snake.color("green", "green")
        self.snake.hideturtle()
        self.snake.pensize(scale_factor)
        self.snake.speed(1)
        self.pos = [(scale_factor, scale_factor)]
        self.direction = "right"
        self.score = 0
        self.prey = None
        self.create_prey()

        self.snake_bg = Turtle()
        self.snake_bg.color("white", "white")
        self.snake_bg.hideturtle()
        self.snake_bg.pensize(scale_factor)
        self.snake_bg.speed("fastest")
        self.snake_bg_curr_pos = self.pos[0]


    def set_pos(self):

        self.snake.clear()
        self.snake.setposition(self.pos[-1])
        self.snake_bg.setposition(self.pos[0])
        self.snake_bg_curr_pos = self.pos[0]


    def create_prey(self):

        pos = (randint(1, self.width/scale_factor)*scale_factor, randint(1, self.height/scale_factor)*scale_factor)
        while pos in self.pos:
            pos = (randint(1, self.width/scale_factor)*scale_factor, randint(1, self.height/scale_factor)*scale_factor)

        if self.prey is None:
            self.prey = Prey()

        self.prey.set_pos(pos)

    def move(self):

        self.snake.forward(1)
        self.pos.append(self.snake.pos())


    def change_dir(self, new_direction):

        self.direction = new_direction

    def catch_prey(self):

        if self.prey.pos[0] - float(scale_factor)/8 <= self.pos[-1][0] <= self.prey.pos[0] + float(scale_factor)/8 and \
            self.prey.pos[1] - float(scale_factor)/8 <= self.pos[-1][1] <= self.prey.pos[1] + float(scale_factor)/8:
            return True

        return False

    def hit_walls(self):

        if self.pos[-1][0] < 0 or self.pos[-1][0] >= self.height or \
            self.pos[-1][1] < 0 or self.pos[-1][1] >= self.width:
            return True

        return False

    def hit_self(self):

        if self.pos[-1] in self.pos[:-1]:
            return True

        return False

    def remove_tail(self):
        # self.snake_bg.clear()
        # self.snake_bg.setposition(self.snake_bg_curr_pos)
        self.snake_bg.setposition(self.pos[0])
        self.snake_bg_curr_pos = self.pos[0]
        del self.pos[0]


    def up(self):
        if self.direction == "left":
            self.snake.right(90)
        elif self.direction == "right":
            self.snake.left(90)

        if self.direction != "down":
            self.direction = "up"

    def down(self):
        if self.direction == "left":
            self.snake.left(90)
        elif self.direction == "right":
            self.snake.right(90)

        if self.direction != "up":
            self.direction = "down"

    def left(self):
        if self.direction == "up":
            self.snake.left(90)
        elif self.direction == "down":
            self.snake.right(90)

        if self.direction != "right":
            self.direction = "left"

    def right(self):
        if self.direction == "up":
            self.snake.right(90)
        elif self.direction == "down":
            self.snake.left(90)

        if self.direction != "left":
            self.direction = "right"

    def hold(self):
        return


    def play(self):

        # while self.direction is None:
        #     sleep(2)

        while True:
            self.move()
            if self.hit_walls() or self.hit_self():
                print("GAME OVER")
                return self.score

            if self.catch_prey():
                self.create_prey()
                self.score += 1
            else:
                self.remove_tail()

            if self.score == self.max_score:
                print("GAME WON")
                return self.score



def main(args):

    max_score = 100
    screen_width = 100
    screen_height = 100

    screen = Screen()
    screen.screensize(screen_width, screen_height)
    screen.setworldcoordinates(0, 0, screen_width, screen_height)

    game = Snake(screen_width, screen_height, max_score=max_score)

    screen.onkey(game.up, "Up")
    screen.onkey(game.down, "Down")
    screen.onkey(game.left, "Left")
    screen.onkey(game.right, "Right")
    screen.onkey(game.hold, "space")

    screen.listen()

    score = game.play()

    print("SCORE: %d"%(score))

    if score == max_score:
        print("Hurray")

    return 0


if __name__ == "__main__":
    exit(main(sys.argv))
