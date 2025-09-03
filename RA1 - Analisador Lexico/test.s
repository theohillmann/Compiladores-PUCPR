        .section .text
        .global main

main:
        clr r1
        ldi r16,0
        sts 0x00C5,r16
        ldi r16,0x67
        sts 0x00C4,r16
        ldi r16,0x08
        sts 0x00C1,r16
        ldi r16,0x06
        sts 0x00C2,r16

        ldi r16,10
        ldi r17,8
        add r16,r17
        sts tmp_1,r16
        lds r16,tmp_1
        sts res_1,r16
        rcall print_num_signed
        rcall newline

        ldi r16,35
        ldi r17,13
        sub r16,r17
        sts tmp_2,r16
        lds r16,tmp_2
        sts res_2,r16
        rcall print_num_signed
        rcall newline

        ldi r16,5
        ldi r17,6
        rcall mul_loop
        sts tmp_3,r16
        lds r16,tmp_3
        sts res_3,r16
        rcall print_num_signed
        rcall newline

        ldi r16,27
        ldi r17,9
        sts tmp_4_div,r17
        rcall div_loop
        sts tmp_4_rem,r17
        sts tmp_4,r16
        lds r16,tmp_4
        sts res_4,r16
        lds r16,tmp_4
        lds r17,tmp_4_rem
        lds r18,tmp_4_div
        rcall print_div_dec
        rcall newline

        ldi r16,17
        ldi r17,6
        rcall div_loop
        mov r16,r17
        sts tmp_5,r16
        lds r16,tmp_5
        sts res_5,r16
        rcall print_num_signed
        rcall newline

        ldi r16,4
        ldi r17,3
        rcall pow_loop
        sts tmp_6,r16
        lds r16,tmp_6
        sts res_6,r16
        rcall print_num_signed
        rcall newline

        lds r16,res_3
        ldi r17,2
        rcall mul_loop
        sts tmp_7,r16
        lds r16,tmp_7
        sts res_7,r16
        rcall print_num_signed
        rcall newline

        ldi r16,80
        lds r17,res_4
        add r16,r17
        sts tmp_8,r16
        lds r16,tmp_8
        sts res_8,r16
        rcall print_num_signed
        rcall newline

        ldi r16,55
        sts var_x,r16

        lds r16,var_x
        ldi r17,7
        sub r16,r17
        sts tmp_9,r16
        lds r16,tmp_9
        sts res_9,r16
        rcall print_num_signed
        rcall newline

        ldi r16,12
        sts var_mem,r16

        lds r16,var_mem
        ldi r17,3
        sts tmp_10_div,r17
        rcall div_loop
        sts tmp_10_rem,r17
        sts tmp_10,r16
        lds r16,tmp_10
        sts res_10,r16
        lds r16,tmp_10
        lds r17,tmp_10_rem
        lds r18,tmp_10_div
        rcall print_div_dec
        rcall newline

        ldi r16,21
        ldi r17,3
        rcall mul_loop
        sts tmp_11,r16
        lds r16,tmp_11
        sts res_11,r16
        rcall print_num_signed
        rcall newline

        ldi r16,36
        ldi r17,12
        sts tmp_12_div,r17
        rcall div_loop
        sts tmp_12_rem,r17
        sts tmp_12,r16
        lds r16,tmp_12
        sts res_12,r16
        lds r16,tmp_12
        lds r17,tmp_12_rem
        lds r18,tmp_12_div
        rcall print_div_dec
        rcall newline

end:
        rjmp end

send:
        push r17
wait:
        lds r17,0x00C0
        sbrs r17,5
        rjmp wait
        sts 0x00C6,r16
        pop r17
        ret

newline:
        push r16
        ldi r16,13
        rcall send
        ldi r16,10
        rcall send
        pop r16
        ret

print_num:
        push r17
        push r18
        push r19
        push r20
        mov r18,r16
        clr r19
        clr r20
hunds:
        cpi r18,100
        brlo tens
        subi r18,100
        inc r19
        rjmp hunds
tens:
        cpi r18,10
        brlo ones
        subi r18,10
        inc r20
        rjmp tens
ones:
        tst r19
        breq maybe_tens
        mov r16,r19
        ldi r17,48
        add r16,r17
        rcall send
maybe_tens:
        tst r19
        brne print_tens
        tst r20
        breq print_units
print_tens:
        mov r16,r20
        ldi r17,48
        add r16,r17
        rcall send
print_units:
        mov r16,r18
        ldi r17,48
        add r16,r17
        rcall send
        pop r20
        pop r19
        pop r18
        pop r17
        ret

print_num_signed:
        sbrs r16,7
        rjmp ppos
        push r16
        ldi r16,45
        rcall send
        pop r16
        com r16
        inc r16
ppos:
        rcall print_num
        ret

div_loop:
        push r18
        push r19
        mov r18,r16
        mov r19,r17
        clr r16
        tst r19
        brne dgo
        mov r17,r18
        pop r19
        pop r18
        ret
dgo:
        cp r18,r19
        brlo dstore
        sub r18,r19
        inc r16
        rjmp dgo
dstore:
        mov r17,r18
        pop r19
        pop r18
        ret

mul_loop:
        push r18
        push r19
        mov r18,r16
        mov r19,r17
        clr r16
mgo:
        tst r19
        breq mend
        add r16,r18
        dec r19
        rjmp mgo
mend:
        pop r19
        pop r18
        ret

pow_loop:
        push r18
        push r19
        sts pow_base,r16
        ldi r16,1
pow_go:
        tst r17
        breq pow_end
        lds r19,pow_base
        push r17
        mov r17,r19
        rcall mul_loop
        pop r17
        dec r17
        rjmp pow_go
pow_end:
        pop r19
        pop r18
        ret

print_div_dec:
        push r17
        push r18
        push r19
        push r20
        push r21
        push r22
        rcall print_num
        ldi r16,46
        rcall send
        mov r19,r17
        clr r20
        clr r21
        ldi r22,100
sum100:
        tst r22
        breq div16
        add r20,r19
        adc r21,r1
        dec r22
        rjmp sum100
div16:
        clr r17
divrun:
        tst r21
        brne dsub
        cp r20,r18
        brlo done2
dsub:
        sub r20,r18
        sbc r21,r1
        inc r17
        rjmp divrun
done2:
        mov r16,r17
        cpi r16,10
        brsh two
        ldi r16,48
        rcall send
        mov r16,r17
two:
        rcall print_num
        pop r22
        pop r21
        pop r20
        pop r19
        pop r18
        pop r17
        ret

        .section .bss
zero:
        .skip 1
pow_base:
        .skip 1
var_x:
        .skip 1
var_mem:
        .skip 1
tmp_1:
        .skip 1
tmp_2:
        .skip 1
tmp_3:
        .skip 1
tmp_4:
        .skip 1
tmp_4_div:
        .skip 1
tmp_4_rem:
        .skip 1
tmp_5:
        .skip 1
tmp_6:
        .skip 1
tmp_7:
        .skip 1
tmp_8:
        .skip 1
tmp_9:
        .skip 1
tmp_10:
        .skip 1
tmp_10_div:
        .skip 1
tmp_10_rem:
        .skip 1
tmp_11:
        .skip 1
tmp_12:
        .skip 1
tmp_12_div:
        .skip 1
tmp_12_rem:
        .skip 1
res_1:
        .skip 1
res_2:
        .skip 1
res_3:
        .skip 1
res_4:
        .skip 1
res_5:
        .skip 1
res_6:
        .skip 1
res_7:
        .skip 1
res_8:
        .skip 1
res_9:
        .skip 1
res_10:
        .skip 1
res_11:
        .skip 1
res_12:
        .skip 1
