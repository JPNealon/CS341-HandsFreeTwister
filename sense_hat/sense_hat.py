'''
Authors:     Brandon, Carson, Jack
Instructor:  Dr. Zhang
Course:      CPSC 341-01 IoT
Institution: Gonzaga University, Spokane, WA 99258
Date:        30 January 2023
Description: A file for practice with the basic functionality of Sense Hat with
             Raspberry Pi.
'''

from sense_hat import SenseHat
import time

if __name__ == '__main__':

    sns = SenseHat()

    g = (0, 255, 0) #Green
    b = (1, 1, 1) #Black
    w = (255, 255, 255) #White

    # Image 1: Frog
    img_1 = [
        w, g, g, g, w, g, g, g,
        w, g, b, g, w, g, b, g,
        g, g, g, g, g, g, g, g,
        g, b, b, b, b, b, b, b,
        g, g, g, g, g, g, g, g,
        g, g, g, g, g, g, g, g,
        g, g, g, g, g, g, g, g,
        g, g, w, g, g, g, w, g,
    ]

    r = (255, 0, 0) #Red
    bl = (0, 0, 255) #Blue
    t = (241, 194, 125) #Tan
    c = (116, 55, 71) #Crimson
    gy = (128, 128, 128) #Grey
    o = (255, 165, 0) #Orange
    k = (0,0,0) #Clear/Off

    #Image 2: Superman
    img_2 = [
        k, k, k, k, b, t, k, k,
        k, k, k, k, t, t, k, k,
        k, k, r, bl, r, o, r, k,
        r, r, bl, bl, bl, r, bl, k,
        c, c, t, c, bl, bl, b, t,
        k, c, c, c, r, c, k, k,
        k, k, k, b, gy, b, gy, k,
        k, k, k, r, k, k, r, k,
    ]
    
    # TODO: Display messages when actions. You should define the contents of the message, the color of the text, the color of the background, and the scroll speed. 

    red = (255,0,0)
    blue = (0,0,255)
    text = (255,255,255)
        
    while True:
        for event in sns.stick.get_events():
            if event.direction == "down":
                # Display images. Define two or more images to display (see above). 
                sns.set_pixels(img_1) #Display Image 1
                time.sleep(2) #Let the image display for 2 seconds
                sns.set_pixels(img_2) #Display Image 2
                time.sleep(2) #Let the Image display for 2 seconds
            elif event.direction == "left":
                # display temp with tree for hot/cold with diff colors and speeds etc
                temp = round(sns.get_temperature())
                if temp >= 24: # higher than 24C show red background and display 
                    message = 'Temp: %dC'%(temp)
                    sns.show_message(message,.1,text,red)
                elif temp < 24: # lower than 24C show blue background asnd display
                    message = 'Temp: %dC'%(temp)
                    sns.show_message(message,.1,text,blue)
            elif event.direction == "up":
                # display humidity with tree etc
                humidity = round(sns.get_humidity())
                if humidity >= 50: # higher than 50% show red background and display 
                    message = 'Humidity: %d'%(humidity)
                    sns.show_message(message,.1,text,red)
                elif humidity < 50: # lower than 50% show blue background asnd display
                    message = 'Humidity: %d'%(humidity)
                    sns.show_message(message,.1,text,blue)
            elif event.direction == "right":
                # display presure with tree etc
                pressure = round(sns.get_pressure())
                if pressure >= 1013: # lower than 1013 mbars show blue background asnd display
                    message = 'Pressure: %dmbars'%(pressure)
                    sns.show_message(message,.1,text,red)
                elif pressure < 1013: # higher than 1013 mbars show red background and display 
                    message = 'Pressure: %dmbars'%(pressure)
                    sns.show_message(message,.1,text,blue)
            else:
                raise ValueError("ValueError")