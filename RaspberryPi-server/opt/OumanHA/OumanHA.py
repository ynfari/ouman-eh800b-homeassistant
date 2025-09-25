from flask import Flask, jsonify
import serial
import time
import re
import threading

app = Flask(__name__)

measurement_names = [
    "1", "2", "3", "4", "5",
    "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15",
    "16", "17", "18", "19", "20",
    "21", "22", "23", "24", "25",
    "26", "27"
]

cached_measurements = {}

def strip_units(value):
    """Strips non-numeric characters from the measurement value."""
    numeric_value = re.findall(r"[-+]?\d*\.?\d+", value)
    if numeric_value:
        return numeric_value[0]  # Return the first match as the numeric value
    return "0"  # Return 0 if no numeric value is found

def read_measurements():
    # Open the serial port
    try:
        ser = serial.Serial(
            port='/dev/ttyACM0', 
            baudrate=9600,        
            bytesize=serial.EIGHTBITS,  
            stopbits=serial.STOPBITS_ONE,  
            parity=serial.PARITY_NONE,    
            timeout=1  
        )
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

    time.sleep(2) 

    # Flush serial port
    ser.flushInput()
    ser.flushOutput()

    command = "MEASUREMENTS\n"
    ser.write(command.encode('utf-8'))
    time.sleep(2)
    ser.flushInput()
    ser.flushOutput()
    ser.write(command.encode('utf-8')) # Send again!

    meas = []
    while len(meas) < 27:
        try:
            # Read a line from the serial port
            line = ser.readline().decode('utf-8').strip()
            if line:  # If there is data received
                numeric_value = strip_units(line)  # Strip non-numeric characters
                meas.append(numeric_value)  # Store the numeric value
        except serial.SerialException as e:
            print(f"Error reading from serial port: {e}")
            break

    ser.close()
    return meas

def update_measurements():
    global cached_measurements
    while True:
        data = read_measurements()
        if data:
            cached_measurements = {name: value for name, value in zip(measurement_names, data)}
        else:
            print("Failed to read data!")
        
        time.sleep(60)

@app.route('/measurements', methods=['GET'])

def get_measurements():
    if cached_measurements:
        return jsonify({'measurements': cached_measurements}), 200
    else:
        return jsonify({'error': 'No measurements available'}), 500

if __name__ == '__main__':
    from waitress import serve
    threading.Thread(target=update_measurements, daemon=True).start()
    serve(app,host='0.0.0.0', port=5001)
