import board
import neopixel
import time


pixels = neopixel.NeoPixel(board.D18, 18)
pixel_pin = board.D18
num_pixels = 30
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER
)

def lightWifiGood():
    pixels.fill((0,0,0))
    for i in range(5):
        pixels[i] = (0,255,0)
    pixels.show()

def lightWifiBad():
    pixels.fill((0,0,0))
    for i in range(5):
        pixels[i] = (0,255,0)
    pixels.show()

def lightKill():
    pixels.fill((0,0,0))
    pixels.show()

def lightGreenFlash():
    pixels.fill((0,255,0))
    pixels.show()
    time.sleep(0.5)
    pixels.fill((0,0,0))
    pixels.show()



def lightPowerUp():
    for k in range(5):
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(0.0001)
    lightKill()





def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)





# while True:
#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((255, 0, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((255, 0, 0, 0))
#     pixels.show()
#     time.sleep(1)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 255, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 255, 0, 0))
#     pixels.show()
#     time.sleep(1)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 0, 255))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 0, 255, 0))
#     pixels.show()
#     time.sleep(1)

#     rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step
