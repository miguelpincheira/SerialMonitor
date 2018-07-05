import serial
import logging
import signal


class SerialMonitor:

    def __init__(self, _the_device='/dev/ttyUSB0', _the_baud=9600, debug=False):
        # Initialize the Logger Format
        log_formatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
        self.log = logging.getLogger()
        file_handler = logging.FileHandler("logs/SerialMonitor.log")
        file_handler.setFormatter(log_formatter)
        self.log.addHandler(file_handler)
        # Set the logger for screen
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_formatter)
        self.log.addHandler(console_handler)
        if debug:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
        # Initialize the configuration
        self.the_device = _the_device
        self.the_baud = _the_baud
        self.the_port = ''
        self.port_is_open = False
        self.buffer = ''
        # Values to Monitor
        self.temp = ''
        self.humd = ''
        # Enable the Signal Catch
        signal.signal(signal.SIGINT, self.signal_handler)

    def signal_handler(self, signal, frame):
        self.log.debug("CTR+C Catched - Will stop after next reading")
        self.port_is_open = False

    def open(self):
        self.log.info("Opening Port on device {} at {}".format(self.the_device, self.the_baud))
        self.the_port = serial.Serial(self.the_device, self.the_baud)
        self.port_is_open = True

    def process_reading(self,message):
        message = message.rstrip('\r\n')
        self.log.debug("MSG({}) - SIZE({})".format(message,len(message)))
        vals = message.split(":")
        if vals[0] == 'H':
            self.humd = vals[1]

        if vals[0] == 'T':
            self.temp = vals[1]
            self.log.info("Temp:{}° - Humd:{}% ".format(self.temp, self.humd))

    def start(self):
        self.log.info("Port monitoring started")
        self.open()
        while self.port_is_open:
            reading = self.the_port.readline().decode()
            self.process_reading(reading)
        self.log.info("Port monitoring stoped")


if __name__ == '__main__':
    # Try to loading config
    my_monitor = SerialMonitor('/dev/ttyACM0', 9600)
    my_monitor.start()

