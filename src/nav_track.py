from hub import light_matrix, port, motion_sensor
import runloop
import motor_pair, motor
import time
import color_sensor
import color
from app import linegraph


wheel_circumference = 27.6 # in centimeters
velocity = 100 # in degrees/sec
rear_arm_port = port.C

right_sensor = port.E
right_motor = port.F
left_sensor = port.B
left_motor = port.A

def dist_cm_to_degrees(dist):
    return round(360*dist/wheel_circumference)

def yaw_degrees():
    return abs(motion_sensor.tilt_angles()[0]/10) # Note that tilt_angles yaw is in tenths of degrees

async def turn(direction): # expecting direction = 1 for right and -1 for left
    motion_sensor.reset_yaw(0)
    while yaw_degrees() != 0: # This is needed since reset_yaw might still not be complete when yaw_degrees is called
        runloop.sleep_ms(10)
    while yaw_degrees() < 90:
        motor_pair.move(motor_pair.PAIR_1, 100*direction)
    motor_pair.stop(motor_pair.PAIR_1, stop=motor.HOLD)

async def turn_right():
    await turn(1)

async def turn_left():
    await turn(-1)

async def turn_slant(degrees=45,right=False):
    motion_sensor.reset_yaw(0)
    while yaw_degrees() != 0:
        runloop.sleep_ms(10)
    while yaw_degrees() < degrees:
        steering = 100 if right else -100
        motor_pair.move(motor_pair.PAIR_1, steering)
    motor_pair.stop(motor_pair.PAIR_1, stop=motor.HOLD)
    error = yaw_degrees() - degrees
    if error > 15:
        await turn_slant(degrees=round(error), right=not right)

async def gyro_move_straight(dist_cm):
    motion_sensor.reset_yaw(0)
    motor.reset_relative_position(port.A, 0)
    while yaw_degrees() != 0:
        runloop.sleep_ms(10)
    linegraph.clear(color.BLUE)
    while abs(motor.relative_position(port.A)) < dist_cm_to_degrees(dist_cm):
        motor_pair.move_tank(motor_pair.PAIR_1, velocity, velocity)
        error = round(yaw_degrees())
        left = motion_sensor.tilt_angles()[0] > 0
        linegraph.plot(color.BLUE,time.ticks_ms(),error)
        if error > 15:
            motor_pair.stop(motor_pair.PAIR_1)
            await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -25, velocity, velocity)
            await turn_slant(degrees=error, right=left)
            motion_sensor.reset_yaw(0)
            while yaw_degrees() != 0:
                runloop.sleep_ms(10)            
            error = round(yaw_degrees())
            linegraph.plot(color.BLUE,time.ticks_ms(),error)
    motor_pair.stop(motor_pair.PAIR_1, stop=motor.HOLD)

# Aligned east facing from SW corner with yellow-horizontal blue-vertical black frames jig
async def ship_mission():
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, dist_cm_to_degrees(39), velocity, velocity, stop=motor.HOLD)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, -dist_cm_to_degrees(10), velocity, velocity, stop=motor.HOLD)
    await turn_slant()
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, dist_cm_to_degrees(13), velocity, velocity, stop=motor.HOLD)
    await turn_slant(right=True)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, dist_cm_to_degrees(13), velocity, velocity, stop=motor.HOLD)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, dist_cm_to_degrees(-55), velocity, velocity, stop=motor.HOLD)
    
async def brush_mission():
    await gyro_move_straight(60)
    await turn_right()

    await motor.run_for_degrees(rear_arm_port, -150, 300)
    await motor.run_for_degrees(rear_arm_port, 240, 300)
    
    await turn_left()

async def reveal_mission():
    await gyro_move_straight(15)
    await turn_slant()
    await motor.run_for_degrees(rear_arm_port, -150, 300)
    await turn_slant(degrees=60, right=True)
    await turn_right()

async def mine_cart_mission():
    await gyro_move_straight(30)
    await turn_left()
    await motor.run_for_degrees(rear_arm_port, 240, 300)
    await turn_right()
    await turn_slant()

async def restore_statue_mission():
    await gyro_move_straight(2)
    await turn_slant(right=True)
    await gyro_move_straight(2)
    await turn_slant(right=False)
    await gyro_move_straight(9)
    await turn_slant(right=True)
    await gyro_move_straight(30)
    await turn_right()
    await motor.run_for_degrees(rear_arm_port, -150, 300)
    await turn_left()

async def scale_mission():
    await gyro_move_straight(20)
    await turn_right()
    await motor.run_for_degrees(rear_arm_port, 240, 300)

    await turn_left()

async def market_mission():
    await gyro_move_straight(40)
    await turn_left()
    await motor.run_for_degrees(rear_arm_port, -150, 300)

    await turn_right()
    await gyro_move_straight(30)
    await motor.run_for_degrees(rear_arm_port, 240, 300)
    await turn_right()
    await gyro_move_straight(80)

def all_done_squaring():
    return ((motor.velocity(left_motor) is 0) and (motor.velocity(right_motor) is 0))

async def move_until_black(motor_port, color_port, direction):
    motor.run(motor_port, velocity * direction)
    while color_sensor.reflection(color_port) > 50:
        await runloop.sleep_ms(50)
    motor.stop(motor_port)

async def square_on_black_white_line():
    #motor_pair.move_tank(motor_pair.PAIR_1, velocity, velocity)
    # port.F is left color sensor, port.D is right
    a = move_until_black(left_motor, left_sensor, -1)
    b = move_until_black(right_motor, right_sensor, 1)
    runloop.run(*[a,b])
    await runloop.until(all_done_squaring)

async def mid_board():
    #await gyro_move_straight(79) # aligns on black-white line
    await gyro_move_straight(76)
    #await turn_left()
    #await gyro_move_straight(12)

# pre: lined up on SW corner with two blue frames + yellow, aligned to north
async def square_on_mine_shaft():
    await gyro_move_straight(95)
    await gyro_move_straight(-3)
    await turn_right()
    await square_on_black_white_line()


async def main():
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.F)

    motion_sensor.set_yaw_face(motion_sensor.FRONT)
    motion_sensor.reset_yaw(0)
    await motor.run_for_degrees(rear_arm_port, 180, 100) # resets rear arm counterclockwise so it always starts from same spot
    await ship_mission()

    return

    #await square_on_mine_shaft()
    #await mid_board()
    #await gyro_move_straight(20)
    #return

    # await motor.run_for_degrees(port.E, 120, 300) # This is enough to lift mine cart
    # await motor.run_for_degrees(port.E, -120, 300)
    # return 
    #linegraph.clear(color.BLUE)
    # while True:-
    #     #print("tilt angles yaw {} {}".format(motion_sensor.tilt_angles()[0], time.ticks_ms()))
    #     angles = motion_sensor.tilt_angles()
    #     #print("tilt angles {} {} {}".format(angles[0], angles[1], angles[2]))
    #     linegraph.plot(color.BLUE,time.ticks_ms(),motion_sensor.tilt_angles()[0])
    #     runloop.sleep_ms(1000)

    # while abs(motion_sensor.tilt_angles()[0]/10) < 90:
    #     motor_pair.move(motor_pair.PAIR_1, 100)
    #     #runloop.sleep_ms(100)
    #     linegraph.plot(color.BLUE,time.ticks_ms(),motion_sensor.tilt_angles()[0]/10)
    # motor_pair.stop(motor_pair.PAIR_1, stop=motor.HOLD)
    # linegraph.plot(color.BLUE,time.ticks_ms(),motion_sensor.tilt_angles()[0]/10)
    # linegraph.show(False)

    await brush_mission()
    await reveal_mission()
    await mine_cart_mission()
    await restore_statue_mission()
    await scale_mission()
    await market_mission()

runloop.run(main())
