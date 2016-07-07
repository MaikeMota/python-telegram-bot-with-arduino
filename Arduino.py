from serial import Serial

def start_communication():
    comport = Serial('COM3', 9600, timeout=5)

    return comport