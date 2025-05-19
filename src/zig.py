from hub import light_matrix, port, motion_sensor
import motor_pair
import motor
import runloop
import sys

async def move_forward_cycle_arm_loop():
    raise_degrees = 90
    arm_speed = 50
    for i in range(3):
        await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, 300, 100, 100)
        print(f"run {i}")
        await motor.run_for_degrees(port.D, raise_degrees, arm_speed)
        runloop.sleep_ms(1000)
        await motor.run_for_degrees(port.D, -raise_degrees, arm_speed)

async def zigzag():
    base_speed = 80
    left_speed_offset = 100
    right_speed_offset = 0
    turn_rotation_degrees = 100
    straight_line_degrees = 300
    for i in range(4):
        await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1,
                                               turn_rotation_degrees,
                                               base_speed+left_speed_offset,
                                               base_speed+right_speed_offset)
        await motor_pair.move_thank_for_degrees(motor_pair.PAIR_1,
                                                straight_line_degrees,
                                                base_speed,
                                                base_speed)
        tmp = left_speed_offset
        left_speed_offset = right_speed_offset
        right_speed_offset = tmp

def turn_for_yaw():
    runloop.sleep_ms(5000)
    base_speed = 100
    motor.reset_relative_position(port.A, 0)
    motion_sensor.reset_yaw(0)
    while abs(motor.relative_position(port.A)) < 500:
        motor_pair.move_tank(motor_pair.PAIR_1, base_speed, base_speed)
        yaw_angle, pitch_angle, roll_angle = motion_sensor.title_angles()
        print(f"yaw: {yaw_angle}, position: {motor.relative_position(port.A)}")
        while abs(yaw_angle) > 20:
            # left is negative yaw
            # right is positive yaw
            yaw_angle, pitch_angle, roll_angle = motion_sensor.title_angles()
            if yaw_angle < 0:
                motor_pair.move_tank(motor_pair.PAIR_1, -100, 100)
            else:
                motor_pair.move_tank(motor_pair.PAIR_1, 100, -100)
            runloop.sleep_ms(500)

async def main():
    await light_matrix_write("Hi!")
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
    await move_forward_cycle_arm_loop()
    sys.exit(0)

runloop.run(main())