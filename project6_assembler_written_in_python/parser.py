class Parser:
    def __init__(self, filename, source):
        self._filename = filename
        self._source = source
        self._file = open(self._source, "rt")
        self._variable_counter = 16
        self._all_symbols = {
            "SP": "0",
            "LCL": "1",
            "ARG": "2",
            "THIS": "3",
            "THAT": "4",
            "R0": "0",
            "R1": "1",
            "R2": "2",
            "R3": "3",
            "R4": "4",
            "R5": "5",
            "R6": "6",
            "R7": "7",
            "R8": "8",
            "R9": "9",
            "R10": "10",
            "R11": "11",
            "R12": "12",
            "R13": "13",
            "R14": "14",
            "R15": "15",
            "SCREEN": "16384",
            "KBD": "24576",
        }

    def parse(self) -> None:
        """
        Parse the input file and translate into machine language.
        As a side effect creates new file {filename}.hack containing binary
        instructions translated from the {filename}.asm program

        Input: None
        Return None
        """
        line_counter = 0
        for line in self._file:
            if line == "\n" or line[:2] == "//":
                continue
            else:
                line = self.clean_line(line)
                command_type = self.command_type(line)
                if command_type == "L_COMMAND":
                    self.update_symbol_table_pseudocommand(command_type, line, line_counter)
                else:
                    line_counter += 1

        self._file.seek(0, 0)

        with open(f"{self._filename}.hack", "wt") as hack_file:
            for line in self._file:
                if line == "\n" or line[:2] == "//":
                    continue
                else:
                    command_type = self.command_type(line)
                    line_counter += 1
                    line = self.clean_line(line)
                    if command_type in ["A_COMMAND"]:
                        symbol_mnemonic = self.symbol(line, command_type)
                        binary_a = self.translate_a_command(symbol_mnemonic)
                        hack_file.write(f"{binary_a}\n")
                    elif command_type == "C_COMMAND":
                        dest_mnemonic = self.dest(line)
                        comp_mnemonic = self.comp(line)
                        jump_mnemonic = self.jump(line)

                        translated_dest = self.translate_dest(dest_mnemonic)
                        translated_comp = self.translate_comp(comp_mnemonic)
                        translated_jump = self.translate_jump(jump_mnemonic)

                        binary_c = "111" + translated_comp + translated_dest + translated_jump
                        hack_file.write(f"{binary_c}\n")
                        

        self._file.close()

    def clean_line(self, line) -> str:
        """ 
        Remove inline comments from the line
        """
        if "/" in line:
            cleaned_line = line.split("/")[0].strip()
            return cleaned_line
        return line.strip()

    def command_type(self, line) -> str:
        """
        Return whether it's A or C or L command
        
        Input: line of text (str)
        Return: command type (str)
        """
        stripped_line = line.strip()
        
        if stripped_line[0] == "@":
            return "A_COMMAND"
        elif stripped_line[0] == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self, line, command_type):
        """
        Return mnemonic symbol from A or L command

        Input: A or L Command as line of text (str)
        Return: Mnemonic symbol (str)
        """
        stripped_line = line.strip()
        if command_type == "A_COMMAND":
            get_symbol = stripped_line.split("@")[1]
        elif command_type == "L_COMMAND":
            get_symbol = stripped_line.split(")")[0][1:]

        return get_symbol    

    
    def dest(self, line) -> str:
        """
        Return destination part of C instruction

        Input: line of text (str)
        Return: Destination part extraction from the line of text (str)
        """
        if "=" not in line:
            dest = "null"
        else:
            dest = line.split("=")[0]

        return dest

    def comp(self, line) -> str:
        """
        Return computation part of C instruction

        Input: line of text (str)
        Return: Computation part extraction from the line of text (str)
        """
        if "=" in line:
            comp = line.split("=")[1]
        elif "=" not in line and ";" in line:
            comp = line.split(";")[0]

        return comp

    def jump(self, line) -> str:
        """
        Return jump part of C instruction

        Input: line of text (str)
        Return: Jump part extracted from the line of text (str)
        """
        if ";" not in line:
            jump = "null"
        elif ";" in line:
            jump = line.split(";")[-1] 
    
        return jump
            

    def translate_dest(self, mnemonic) -> str:
        """
        Return translated destination part of c instruction

        input: mnemonic symbol
        return: value of the mnemonic symbol
        """
        symbol_table = {
            "null": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111"
        }

        return symbol_table[mnemonic]

    def translate_comp(self, mnemonic) -> str:
        """
        Return translated destination part of c instruction

        Input: mnemonic symbol
        Return: value of the mnemonic symbol
        """
        symbol_table = {
            "0": "0101010",
            "1": "0111111",
            "-1": "0111010",
            "D": "0001100",
            "A": "0110000",
            "!D": "0001101",
            "!A": "0110001",
            "-D": "0001111",
            "-A": "0110011",
            "D+1": "0011111",
            "A+1": "0110111",
            "D-1": "0001110",
            "A-1": "0110010",
            "D+A": "0000010",
            "D-A": "0010011",
            "A-D": "0000111",
            "D&A": "0000000",
            "D|A": "0010101",
            "M": "1110000",
            "!M": "1110001",
            "-M": "1110011",
            "M+1": "1110111",
            "M-1": "1110010",
            "D+M": "1000010",
            "D-M": "1010011",
            "M-D": "1000111",
            "D&M": "1000000",
            "D|M": "1010101"
        }

        return symbol_table[mnemonic]
        
    def translate_jump(self, mnemonic) -> str:
        """
        Translate C command jump mnemonic into 3-bit value

        Input:  jump mnemonic representation (str)
        Return: 3-bit value of the input symbol (str)
        """
        symbol_table = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }

        return symbol_table[mnemonic]

    def translate_a_command(self, value) -> str:
        """
        Translate A command into 16-bit sequence

        Input:  value of A command (str)
        Return: 16-bit value of the input A command (str)
        """
        try:
            return "{0:016b}".format(int(value))
        except ValueError:
            if value in self._all_symbols:
                value = self._all_symbols[value]
            else:
                self._all_symbols[value] = self._variable_counter
                self._variable_counter += 1
                value = self._all_symbols[value]

            return "{0:016b}".format(int(value))

    def update_symbol_table_pseudocommand(self, command_type, line,
                                          line_counter) -> None:
        """
        Update main symbol table with pseudocommands found in the assembly
        program

        Input: command_type (str), line (str), line_counter (int)
        Return: None
        """
        symbol_mnemonic = self.symbol(line, command_type)
    
        if symbol_mnemonic not in self._all_symbols:
            self._all_symbols[symbol_mnemonic] = line_counter
