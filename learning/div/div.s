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

        ; Inicializa valores
        ldi r16, 0xAA ; numerador = 170
        ldi r17, 0x07 ; denominador = 7
        ldi r19, 0x00 ; parte inteira = 0
        mov r18, r16  ; backup numerador
        mov r26, r17  ; r26 = denominador original

sub:
        cp r16, r17   ; compara numerador com denominador
        brlo resto_pronto ; se numerador < denominador, para
        sub r16, r17  ; numerador = numerador - denominador
        inc r19       ; parte_inteira++
        rjmp sub      ; repete

resto_pronto:
        mov r21, r16 ; r21 = resto
        rjmp envia_inteiro
envia_inteiro:
        ; Transmite parte inteira (sempre dois dígitos)
        mov r22, r19      ; r22 = parte inteira
        ldi r23, 10
        mov r24, r22
        ldi r25, 0
        ; Calcula dezena
        dec_int_loop:
            cpi r24, 10
            brlt dec_int_done
            subi r24, 10
            inc r25
            rjmp dec_int_loop
        dec_int_done:
            ldi r20, '0'
            add r20, r25
            rcall envia_uart
            ldi r20, '0'
            add r20, r24
            rcall envia_uart
        ldi r20, ',' ; separador decimal
        rcall envia_uart
        mov r16, r21 ; r16 = resto
        
        ; Primeira casa decimal
        ldi r23, 0x0A 
        mul r16, r23  ; r0 = resto * 10
        mov r16, r0   ; r16 = resto * 10
        clr r0
        clr r1
        
        ldi r24, 0x00 ; contador primeira casa
primeira_casa:
        cp r16, r26   ; compara com denominador
        brlt transmite_primeira
        sub r16, r26  ; subtrai denominador
        inc r24       ; incrementa contador
        rjmp primeira_casa
        
transmite_primeira:
        ldi r20, '0'
        add r20, r24
        rcall envia_uart
        
        ; Segunda casa decimal
        ldi r23, 0x0A 
        mul r16, r23  ; r0 = resto * 10
        mov r16, r0   ; r16 = resto * 10
        clr r0
        clr r1
        
        ldi r24, 0x00 ; contador segunda casa
segunda_casa:
        cp r16, r26   ; compara com denominador
        brlt transmite_segunda
        sub r16, r26  ; subtrai denominador
        inc r24       ; incrementa contador
        rjmp segunda_casa
        
transmite_segunda:
        ldi r20, '0'
        add r20, r24
        rcall envia_uart
        rjmp fim
fim:
        rjmp fim

; Rotina para enviar caractere UART
envia_uart:
        lds r22, UCSR0A
        sbrs r22, UDRE0_BIT
        rjmp envia_uart
        sts UDR0, r20
        ret

        lsl r16
        rjmp wait

wait:
        ldi r20, '0' ; '0' = 0x30
        add r20, r16 ; counter + '0'
        lds r22, UCSR0A
        sbrs r22, UDRE0_BIT
        rjmp wait

        sts UDR0, r20

