import paho.mqtt.publish as publish
import json
import digitalio
import board
import busio
import adafruit_rfm9x

RADIO_FREQ_MHZ = 858.0
CS = digitalio.DigitalInOut(board.CE1)
RESET = digitalio.DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
# Initialze RFM radio with a more conservative baudrate
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=10000) #baudrate ændret fra 1000000 til 10000 pga lav mængde data

while True:
    data = rfm9x.receive()
    if data != None:
        decoded_data = data.decode()
        # publish decoded data til markdata¨
        publish.single("markdata/", decoded_data, hostname="20.93.112.153")

        