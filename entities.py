import pygame.sprite
import random
from ball import Ball
import vector
import commons

from pin import Pin
from vector import Vector

@staticmethod
def update_balls():
    check_hit()
    #check_balls_collisions()
    Ball.all.update()

@staticmethod
def update_pins():
    Pin.all.update()
    pos_x = random.random() * (commons.screen_w - commons.gui_w)
    pos_y = random.random() * commons.screen_h
    if len(Pin.all) == 0:
        Pin.all.add(Pin(Vector(pos_x, pos_y), 40))

@staticmethod
def draw_all():
    for pin in Pin.all:
        pin.draw(commons.screen)
    # Pin.all.draw(commons.screen)
    Ball.all.draw(commons.screen)

@staticmethod
def check_balls_collisions():
    balls = list(Ball.all)
    num_balls = len(balls)

    for i in range(num_balls - 1, -1, -1):
        for j in range(i - 1, -1, -1):
            ball_i = balls[i]
            ball_j = balls[j]

            distance = vector.dist(ball_i.position, ball_j.position)
            if distance <= (ball_i.radius + ball_j.radius):
                relative_velocity = ball_j.velocity - ball_i.velocity
                normal = vector.normalize(ball_j.position - ball_i.position)

                impulse = 2 * vector.dot(relative_velocity, normal) / (1 / ball_i.radius + 1 / ball_j.radius)
                impulse *= commons.restitution

                ball_i.velocity += impulse * normal / (1 / ball_i.radius)
                ball_j.velocity -= impulse * normal / (1 / ball_j.radius)

                overlap = ball_i.radius + ball_j.radius - distance

                correction = commons.correction_factor * vector.length(relative_velocity) * commons.delta_time
                correction_vector = normal * (overlap + correction) / 2

                ball_i.position -= correction_vector
                ball_j.position += correction_vector

@staticmethod
def delete_balls():
    for ball in Ball.all:
        ball.kill()

@staticmethod
def delete_pins():
    for pin in Pin.all:
        pin.kill()


@staticmethod
def check_hit():
    for ball in Ball.all:
        for pin in Pin.all:
            closest_point_x = max(pin.position.x - pin.width / 2, min(ball.position.x, pin.position.x + pin.width / 2))
            closest_point_y = max(pin.position.y - pin.height / 2, min(ball.position.y, pin.position.y + pin.height / 2))

            distance = vector.dist(Vector(closest_point_x, closest_point_y), ball.position)

            if distance <= ball.radius:
                relative_velocity = -ball.velocity
                normal = vector.normalize(Vector(ball.position.x - closest_point_x, ball.position.y - closest_point_y))

                impulse = 2 * vector.dot(relative_velocity, normal) / (1 / ball.radius)
                impulse *= commons.restitution

                ball.velocity = vector.normalize(ball.velocity + impulse * normal / (1 / ball.radius)) * 1000

                overlap = ball.radius - distance
                correction = commons.correction_factor * vector.length(relative_velocity) * commons.delta_time
                correction_vector = normal * (overlap + correction)

                ball.position += correction_vector
                pin.health -= 1
                if pin.health == 0:
                    pin.alive = False
                break



@staticmethod
def add_pin():
    new_pin = Pin(vector.random_vector())
    Pin.all.add(new_pin)
