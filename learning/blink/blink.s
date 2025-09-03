        .section .text
        .global main

.equ DDRB,  0x04
.equ PORTB, 0x05
.equ PB5,   5          ; LED do UNO (pino 13)

main:
        sbi DDRB, PB5

loop:
        sbi PORTB, PB5     ; ON
        rcall delay_big
        cbi PORTB, PB5     ; OFF
        rcall delay_big
        rjmp loop

; delay ~ bem maior
delay_big:
        ldi r20, 0x10
db1:    ldi r21, 0xFF
db2:    ldi r22, 0xFF
db3:    dec r22
        brne db3
        dec r21
        brne db2
        dec r20
        brne db1
        ret
