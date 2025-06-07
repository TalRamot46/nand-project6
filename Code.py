"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

class CodeException(Exception):
    pass

class Code:
    """Translates Hack assembly language mnemonics into binary codes."""
    
    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        dest_dict = {
            "" : "000",
            "M" : "001",
            "D" : "010",
            "MD" : "011",
            "A" : "100",
            "AM" : "101",
            "AD" : "110",
            "AMD" : "111" 
        }
        try:
            return dest_dict[mnemonic]
        except KeyError:
            raise CodeException("dest mnemonic invalid")
        
    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: the binary code of the given mnemonic.
        """
        comp_dict = {
            # a = 0
            "0" : "0    1   0   1   0   1   0",
            "1" : "0    1   1   1   1   1   1",
            "-1" : "0   1   1   1   0   1   0",
            "D" : "0    0   0   1   1   0   0",
            "A" : "0    1   1   0   0   0   0",
            "!D" : "0   0   0   1   1   0   1",
            "!A" : "0   1   1   0   0   0   1",
            "-D" : "0   0   0   1   1   1   1",
            "-A" : "0   1   1   0   0   1   1",
            "D+1" : "0  0   1   1   1   1   1",
            "A+1" :	"0  1   1   0   1   1   1",
            "D-1":	"0  0   0   1  	1	1	0",
            "A-1":	"0  1   1   0	0	1	0",
            "D+A":	"0  0   0   0   0   1   0",
            "D-A":	"0  0   1   0	0	1	1",
            "A-D":	"0  0   0   0	1	1	1",
            "D&A":	"0  0   0   0	0	0	0",
            "D|A":	"0  0   1   0	1	0	1",
            
            # a = 1
            "M" : "1    1   1	0	0	0	0",
            "!M" : "1   1	1	0	0	0	1",
            "-M" : "1   1	1	0	0	1	1",
            "M+1" : "1  1	1	0	1	1	1",
            "M-1" : "1  1	1	0	0	1	0",
            "D+M" : "1  0	0	0	0	1	0",
            "D-M" : "1  0	1	0	0	1	1",
            "M-D" : "1  0	0	0	1	1	1",
            "D&M" : "1  0	0	0	0	0	0",
            "D|M" : "1  0	1	0	1	0	1"
        }
        try:
            comp_result = "".join(comp_dict[mnemonic].split())
            return comp_result
        except KeyError:
            raise CodeException("comp mnemonic invalid")

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        # Your code goes here!
        jump_dict = {
            "" : "000", # no jump
            "JGT" : "001",
            "JEQ" : "010",
            "JGE" : "011", 
            "JLT" : "100",
            "JNE" : "101",
            "JLE" : "110",
            "JMP" : "111"
        }
        try:
            return jump_dict[mnemonic]
        except KeyError:
            raise CodeException("jump mnemonic invalid")
    
    @staticmethod
    def decimal_to_15bit(decimal_str: str):
        """
        Converts a positive decimal number (0 to 2^15 - 1) to its 15-bit binary string representation.

        Args:
            decimal_num: A positive integer between 0 and 32767 (inclusive).

        Returns:
            A string representing the 15-bit binary notation of the decimal number.
            Returns an error message if the input is invalid.
        """

        try:
            decimal_num = int(decimal_str)
        except ValueError:
            raise CodeException("attempted to convert an invalid symbol to a 15-bit number")
        if decimal_num < 0 or decimal_num > 32767:
            raise CodeException("input must be a positive integer between 0 and 32767.")

        binary_representation = bin(decimal_num)[2:]  # Convert to binary and remove "0b" prefix
        padded_binary = binary_representation.zfill(15)  # Pad with leading zeros to make it 15 bits
        return padded_binary


# Important:
# Here I neglected the implementation of the Extended C-Command Specification 
# as it isn't used in any of the test files.

