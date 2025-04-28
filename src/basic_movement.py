from hub import light_matrix, port
import motor_pair
import runloop

WheelCircumferenceCm = 27.6

def degreesFromDistanceCentimeters(distanceCm):
    return int(distanceCm*360/WheelCircumferenceCm)

async def main():
    await light_matrix.write("Hi!")
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
    velocity = 100
    # Move forward for given distance
    degrees = degreesFromDistanceCentimeters(40)
    print(degrees)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, degrees, velocity, velocity)
    for i in range(4):
        await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, degreesFromDistanceCentimeters(6), velocity, -velocity)
        degrees = degreesFromDistanceCentimeters(10)
        await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, degrees, velocity, velocity)
runloop.run(main())