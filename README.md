# pirok
Control and monitor a Rocket Espresso machine (or else) with your Raspberry Pi

Highly inspired by James Ward's great work: http://int03.co.uk/blog/project-coffee-espiresso-machine/ but written mostly in python language and using a little different hardware 

Hardware requirements: 
- Espresso machine
- Raspberry B+
- various sensors (temperature, ultrasound, flowmeter, humidity etc)
- SSR for temperature control
- i am using a "Mimo 720s" which is 800x480 color touchscreen, but it is quite old now, you probably have cheaper alternatives

Software requirements:
- Raspbian (Linux raspberrypi 3.18.2+ #1 PREEMPT Sun Feb 8 01:19:24 CET 2015 armv6l GNU/Linux)
- Pygame library for graphics
- RPi.GPIO library (version 0.5?) for dealing with advanced GPIOs
- and lot of other things i probably forgot...

Warning, code not clean (and some parts need to be called with Super User priviledges, this is also not clean) but it works!

Basically, 
- main.py = main program, initializes all and handles user interface (keep display updated each 0,5s, react to touchscreen)
- multithreadXXX.py = tasks that are launched to poll a specific hardware
- readXXX.py = low level code that reads a specific hardware
- myXXX.py = user interface module for gauges and plots
- SSRControl.ppy = drives the SSR

To start program, type "python main.py"



