// Create infinite loop 
// Access keyboard register 
// If value of keyboard register != 0 set screen to all black
// else if value of keyboard register = 0 set screen to all white 
// set i (index) to 8191
// screen memory map ranges from 0 to 8191 
// use i to access each register in screen memory 
// for (let i = 8191; i == 0; i--) { change each register to -1 }


(LOOP)
    @8191
    D=A
    @i
    M=D
    @KBD
    D=M
    @SET_SCREEN_TO_BLACK
    D;JGT
    @SET_SCREEN_TO_WHITE
    D;JLE
    
(SET_SCREEN_TO_BLACK)
    @i
    D=M
    @LOOP
    D;JLT
    @SCREEN
    A=A+D
    M=-1
    @i
    M=M-1
    @SET_SCREEN_TO_BLACK
    D;JMP

(SET_SCREEN_TO_WHITE)
    @i
    D=M
    @LOOP
    D;JLT
    @SCREEN
    A=A+D
    M=0
    @i
    M=M-1
    @SET_SCREEN_TO_WHITE
    D;JMP
