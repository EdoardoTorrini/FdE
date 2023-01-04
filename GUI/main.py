import serial
import serial.tools.list_ports
'''

    Gestione Multitreading delle Porte COM, riconoscimento delle Porte Attive in Comunicazione Seriale   

    ports = serial.tools.list_ports.comports()
    
    for port, desc, hwind in sorted(ports):
        print(port, ":", desc, "[", hwind, "]")    
    
'''


serialPort = serial.Serial(
    "COM3", baudrate=115200, timeout=1, bytesize=8, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE
)

serialString = ""

try:
    while 1:

        try:
            data = serialPort.read(255).decode("latin1")

            nVal = data.find('\0')
            data = data[:nVal]
            if data != "":
                print(data)

        except Exception as sVal:
            sErr = sVal

except KeyboardInterrupt as sVal:
    print("Esecuzione Interrotta")