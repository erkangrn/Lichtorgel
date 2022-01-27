from rpi_ws281x import *

strip = Adafruit_NeoPixel(30, 18, 800000, 5, False, 255)
strip.begin()
for i in range (0, 30):
			strip.setPixelColorRGB(i, 0, 0, 0)
strip.show()