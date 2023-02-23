# from screen import updateScreen
# import light
# import helpers
# import screen

import time

# Webapp
import threading
from flask import Flask, render_template, request




######## WAKE UP ########
#light.lightPowerUp()

# Check internet connection
#helpers.checkInternet()

# Set welcome screen
#screen.welcomeScreen()
# Check abiotic sensor


######## AWAKE ########

def runAwake():
    i = 0
    while True:
        print("Still running main worker: ", i)
        i += 1
        time.sleep(5)


#     updateScreen(t, cpu)

#     time.sleep(1800)




######## GET READY FOR BED ########
# Back up images to drive
# Back up data to drive
# Turn of light



######## GO TO SLEEP ########
#light.lightKill()
# Take an image an hour - just for fun? With flash



######## WEBAPP ########



app = Flask(__name__)

def runApp():
    app.run(debug=True, use_reloader=False, port=5000, host='0.0.0.0')


@app.route('/')
def hello():
    return """
    <h1>TECOLOGY<h1>
    <h2>Insect Dashboard<h2>
    """




### RUN PROGRAM ###
if __name__ == '__main__':
    try:
        #logger.info(f'start first thread')
        t1 = threading.Thread(target=runApp).start()
        #logger.info(f'start second thread')
        t2 = threading.Thread(target=runAwake).start()
    except Exception as e:
        print("error")
        #logger.error("Unexpected error:" + str(e))


