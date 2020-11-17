// i = 0
// sum = 0
// int1 = 4
// int2 = 2
// if int1 OR int 2 = 0 then sum = 0 
// else
// sum = 4 + 4
// for (let i = 0; i < int2; i++) {
//    sum = int1+ sum 
// }

    @i
    M=0
    @sum
    M=0
    @R0
    D=M
    @MULTIPLICATION_BY_ZERO
    D;JEQ
    @R1
    D=M
    @MULTIPLICATION_BY_ZERO
    D;JEQ


(LOOP)
    @i 
    D=M
    @R1
    D=D-M
    @FINALIZE
    D;JEQ

    @sum
    D=M
    @R0
    D=D+M
    @sum
    M=D
    @i
    M=M+1
    @LOOP
    0;JMP

(MULTIPLICATION_BY_ZERO)
    @sum
    M=0
    @FINALIZE
    0;JMP

(FINALIZE)
    @sum
    D=M
    @R2
    M=D

(END)
    @END
    0;JMP
