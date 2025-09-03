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

        ; inicia valores
        ldi r16, 0x04 ;  num 1 (multiplicando)
        ldi r17, 0x02 ;  num 2 (multiplicador)
        ldi r19, 0x00 ;  resultado
        ldi r21, 0x00 ;  contador

loop:
        add r19, r16 ; resultado = resultado + num1
        inc r21     ; contador++
        cp r21, r17 ;
        brlo loop    ; se contador < num2, repete
        
        mov r16, r19 ; move resultado para r16 para transmissão
        
        ; Converte para ASCII e envia dígito por dígito
        ; Para números até 255, precisamos de até 3 dígitos
        
        ; Calcula centenas
        ldi r22, 0  ; contador de centenas
        cpi r16, 100
        brlo tens   ; se < 100, pula centenas
        
hundreds_loop:
        subi r16, 100
        inc r22
        cpi r16, 100
        brsh hundreds_loop
        
        ; Envia centena (se > 0)
        cpi r22, 0
        breq tens
        ldi r20, '0'
        add r20, r22
        rcall send_char

tens:
        ; Calcula dezenas
        ldi r22, 0  ; contador de dezenas
        cpi r16, 10
        brlo units  ; se < 10, pula dezenas
        
tens_loop:
        subi r16, 10
        inc r22
        cpi r16, 10
        brsh tens_loop
        
        ; Envia dezena
        ldi r20, '0'
        add r20, r22
        rcall send_char

units:
        ; Envia unidade
        ldi r20, '0'
        add r20, r16
        rcall send_char
        rjmp fim

send_char:
        lds r23, UCSR0A
        sbrs r23, UDRE0_BIT
        rjmp send_char
        sts UDR0, r20
        ret

fim:
        rjmp fim

