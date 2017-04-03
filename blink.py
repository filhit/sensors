#!/usr/bin/python
import dbus.service
import dbus.glib
import gobject
import dbus

from gpiozero import LED, PWMLED, Button
import random

gobject.threads_init()

red = PWMLED(19)
yellow = PWMLED(21)
leds = [
  PWMLED(23),
  PWMLED(24),
  PWMLED(25),
  PWMLED(12),
  PWMLED(4),
  PWMLED(17),
  PWMLED(22),
  PWMLED(27),
  yellow
]

button = Button(18)
is_on = False

def turn_on():
  for led in leds:
    global is_on
    is_on = True
    led.pulse(random.uniform(0.1, 2))
  red.on();

def turn_off():
  global is_on
  is_on = False
  for led in leds:
    led.off()
  red.off();

def toggle():
  global is_on
  if is_on:
    turn_off()
  else:
    turn_on()

button.when_pressed = toggle

class DbusReceiver(dbus.service.Object):

    loop = None

    def __init__(self, bus_name, object_path, loop):
        dbus.service.Object.__init__(self, bus_name, object_path)
        self.loop = loop


    @dbus.service.method('filhit.Blink')
    def turn_on(self):
        turn_on()

    @dbus.service.method('filhit.Blink')
    def turn_off(self):
        turn_off()

    @dbus.service.method('filhit.Blink')
    def state(self):
        global is_on
        if not is_on:
            raise Exception('Lights are off')

loop = gobject.MainLoop()

bus = dbus.SystemBus()
bus_name = dbus.service.BusName('filhit.blink', bus=bus)

obj = DbusReceiver(bus_name, '/filhit/Blink', loop)

loop.run()
