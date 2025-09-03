#!/bin/bash
python main.py tests/test2.txt test.s
avr-gcc -mmcu=atmega328p -o test.elf test.s
avr-objcopy -O ihex -R .eeprom test.elf test.hex
avrdude -c arduino -p m328p -P /dev/tty.usbmodem11301 -b 115200 -U flash:w:test.hex