# from hub import light_matrix
# import runloop

# async def main():
#     # write your code here
#     await light_matrix.write("Hi!")

# runloop.run(main())

from hub import port
import motor_pair
import runloop
import sys
import math 
import motor
import color_sensor
import color

def degrees_from_distance_cm(dist_cm):
    wheel_diameter_cm = 8.78
    wheel_circumference = math.pi * wheel_diameter_cm
    return int((dist_cm / wheel_circumference) * 360)

async def move_for_time():
    motor_pair.move_tank(motor_pair.PAIR_1, 100, 100)
    await runloop.sleep_ms(1000)
    motor_pair.stop(motor_pair.PAIR_1)

async def move_for_rotations():
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 221, 0) # 90 degrees is how far in centimeters if the wheel is 27.6cm in circumference?

async def move_for_rotations_left():
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, -80)

async def move_for_rotations_right():
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, 80)

async def move_for_distance(dist_cm):
    # how do you write a function to move the robot by distance in centimeters instead of degrees rotation?
    distance =  degrees_from_distance_cm(dist_cm)   
    print("moving {}".format(degrees_from_distance_cm(distance)))
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, distance, 100, 100)
    pass

async def move_in_a_square():
    await move_for_rotations()
    await move_for_rotations_right()
    await move_for_rotations()
    await move_for_rotations_right()
    await move_for_rotations()
    await move_for_rotations_right()
    await move_for_rotations()
    # This is kind of repetitive. We can do better and make it more maintainable and easy to work with.

async def move_in_a_square_loop():
    await move_for_rotations()
    for i in range(3):
        await move_for_rotations_right()
        await move_for_rotations()

async def navigate_to_mine_cart():
    # assumption: starting from lower left hand corner facing opposite home area 
    await move_for_distance(24)
    await move_for_rotations_left()
    await move_for_distance(90)
    await move_for_rotations_right()


async def square_on_line():
    print("square_on_line")
    motor_pair.move_tank(motor_pair.PAIR_1, 100, 100)
    # port.F is left color sensor, port.D is right
    await runloop.until(lambda: color_sensor.color(port.F) is color.BLACK)
    print("squared left")
    motor_pair.stop(motor_pair.PAIR_1)
    motor.run(port.E, -100)
    await runloop.until(lambda: color_sensor.color(port.D) is color.BLACK)
    motor.stop(port.E)
    motor_pair.move_tank(motor_pair.PAIR_1, -100, -100)
    await runloop.until(lambda: color_sensor.color(port.D) is color.WHITE)
    motor_pair.stop(motor_pair.PAIR_1)

async def mine_cart_square():
    await navigate_to_mine_cart()
    await square_on_line()

async def main(): 
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)# How can you tell what port each motor is connected to?
    #await move_for_time()
    #await move_for_rotations()
    #await move_for_rotations_left()
    #await move_for_rotations_right()
    #await move_in_a_square()
    #await move_in_a_square_loop()
    await mine_cart_square()



runloop.run(main())
sys.exit(0)