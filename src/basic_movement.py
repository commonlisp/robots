from hub import light_matrix, port
import motor_pair
import runloop

WheelCircumferenceCm = 27.6

def degreesFromDistanceCentimeters(distanceCm):
    return int(distanceCm*WheelCircumferenceCm/360)

async def main():
    await light_matrix.write("Hi!")
    await motor_pair.pair(motor_pair.PAIR_1, port.A, port.B)
	velocity = 100
	# Move forward for given distance
    await motor_pair.move_tank_for_degrees(motor_pair.PAIR_1, degreesFromDistanceCentimeters(40), velocity, velocity)
