import board
import neopixel
import time
import screen
import socket

# Try some screen stuff for service run script


hostName = socket.gethostname()
ip_address = socket.gethostbyname(hostName)
hostAddress = socket.gethostbyname(hostName + ".local")

print(f"Hostname: {hostName}")
print(f"Host Address: {hostAddress, }")

screen.welcomeScreen(hostName, hostAddress)
print("Screen done")
time.sleep(30)

pixels = neopixel.NeoPixel(board.D18, 18)

pixels[0] = (0, 0, 0)
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 30

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

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


def rainbow_cycle(wait):
    for i in range(10):
        for j in range(255):
            for i in range(num_pixels):
                pixel_index = (i * 256 // num_pixels) + j
                pixels[i] = wheel(pixel_index & 255)
            pixels.show()
            time.sleep(wait)





# Comment this line out if you have RGBW/GRBW NeoPixels
# pixels.fill((255, 0, 0))
# # Uncomment this line if you have RGBW/GRBW NeoPixels
# # pixels.fill((255, 0, 0, 0))
# pixels.show()
# time.sleep(2)

# Comment this line out if you have RGBW/GRBW NeoPixels
# pixels.fill((0, 255, 0))
# # Uncomment this line if you have RGBW/GRBW NeoPixels
# # pixels.fill((0, 255, 0, 0))
# pixels.show()
# time.sleep(2)

# Comment this line out if you have RGBW/GRBW NeoPixels
# pixels.fill((0, 0, 255))
# # Uncomment this line if you have RGBW/GRBW NeoPixels
# # pixels.fill((0, 0, 255, 0))
# pixels.show()
# time.sleep(2)

rainbow_cycle(0.0015) # rainbow cycle with 1ms delay per step

# Comment this line out if you have RGBW/GRBW NeoPixels
pixels.fill((0, 255, 0))
# Uncomment this line if you have RGBW/GRBW NeoPixels
# pixels.fill((0, 255, 0, 0))
pixels.show()
time.sleep(8)


pixels.fill((0, 0, 0))
pixels.show()
time.sleep(9999999)


# while True:
#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((255, 0, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((255, 0, 0, 0))
#     pixels.show()
#     time.sleep(2)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 255, 0))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 255, 0, 0))
#     pixels.show()
#     time.sleep(2)

#     # Comment this line out if you have RGBW/GRBW NeoPixels
#     pixels.fill((0, 0, 255))
#     # Uncomment this line if you have RGBW/GRBW NeoPixels
#     # pixels.fill((0, 0, 255, 0))
#     pixels.show()
#     time.sleep(2)

#     rainbow_cycle(0.001) # rainbow cycle with 1ms delay per step
