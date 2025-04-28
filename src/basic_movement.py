from hub import light_matrix, port
import motor_pair
import runloop

WheelCircumferenceCm = 27.6

def degreesFromDistanceCentimeters(distanceCm):
    return int(round(distanceCm*360/WheelCircumferenceCm))

async def main():
    await light_matrix.write("Hi!")
    motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
    velocity = 100
    # Move forward for given distance
    degrees = degreesFromDistanceCentimeters(40)
    print(degrees)
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, degrees, velocity, velocity)

runloop.run(main())