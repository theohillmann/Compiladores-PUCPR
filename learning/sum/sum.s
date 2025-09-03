        .section .text
        .global main

; ===== Constantes estáticas =====
; Baud = 9600 @ 16 MHz -> UBRR = 103 (0x0067)
.equ UBRR_HI,   0x00
.equ UBRR_LO,   0x67

; Endereços (data space) dos registradores da USART0
.equ UCSR0A,    0x00C0
.equ UCSR0B,    0x00C1
.equ UCSR0C,    0x00C2
.equ UBRR0L,    0x00C4
.equ UBRR0H,    0x00C5
.equ UDR0,      0x00C6

; Bits (pré-calculados, sem usar <<)
.equ UDRE0_BIT, 5       ; bit em UCSR0A
.equ TXEN0_MASK, 0x08   ; (1<<3) = 8
.equ UCSZ_8BIT,  0x06   ; (1<<2)|(1<<1) = 6  -> 8N1

; ===== Código =====
main:
        ; Baud rate
        ldi r16, UBRR_HI
        sts UBRR0H, r16
        ldi r16, UBRR_LO
        sts UBRR0L, r16

        ; Habilita transmissor
        ldi r16, TXEN0_MASK
        sts UCSR0B, r16

        ; Formato 8N1 (8 bits)
        ldi r16, UCSZ_8BIT
        sts UCSR0C, r16

loop:
        ldi r16, 0x01
        ldi r18, 0x02
        add r16, r18

        ldi r20, '0' ; '0' = 0x30
        add r16, r20 ; 3+48 = 51 = '3'


wait:
        lds r17, UCSR0A
        sbrs r17, UDRE0_BIT
        rjmp wait

        sts UDR0, r16

