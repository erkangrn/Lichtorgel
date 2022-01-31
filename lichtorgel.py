import pyaudio # Library für Audio I/O 
import numpy as np # Library für Vektoren, Matrizen, Arrays, FFT,...
from rpi_ws281x import * # Library für LED-Steuerung
import time # Library für Zeit
from sys import argv # Für Parameterübergabe

np.set_printoptions(suppress=True) 

# Steurung der LEDs je nach Frequenz
def steuerung(frequenz):
	rot, gruen, blau = 0, 0, 0
	if frequenz != 53 and frequenz != 150: # Werte bei Stille
		if frequenz > 55 and frequenz < 700:
			rot = 255
		elif frequenz > 700 and frequenz < 1000:
			gruen = 255
		elif frequenz > 1000 and frequenz < 10000:
			blau = 255
	for i in range (0, 30):
		strip.setPixelColorRGB(i, rot, gruen, blau)
	strip.show()
	return True

ZEIT = float(argv[1]) # Parameter aus der Kommandozeile

strip = Adafruit_NeoPixel(30, 18, 800000, 5, False, 255)
strip.begin()
p = pyaudio.PyAudio()
stream = p.open	(format=pyaudio.paInt16,
				channels=1,
				rate=44100,
				input=True,
       			frames_per_buffer=4096) 

while True:
	daten = np.fromstring(stream.read(4096, exception_on_overflow = False),dtype=np.int16) # Daten einlesen
	fourier = abs(np.fft.fft(daten).real) # Fast-Fourrier-Transformation
	frequenz = np.fft.fftfreq(4096,1.0/44100)  # gibt Frequenzen aus den Daten zurück
	frequenzHigh = frequenz[np.where(fourier == np.max(fourier))[0][0]] # höchste Frequenz auswählen
	frequenzHigh = int(abs(frequenzHigh)) # in Integer umwandeln und Betrag nehmen
	print("Frequenz: %d Hz"%frequenzHigh) # Frequenz ausgeben
	steuerung(frequenzHigh) # LEDs steuern
	time.sleep(ZEIT) # ggf. eine bestimmte Zeit lang warten

# Stream schließen, wird aber nie erreicht
stream.stop_stream()
stream.close()
p.terminate()
