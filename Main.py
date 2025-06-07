"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser, A_COMMAND, C_COMMAND, L_COMMAND
from Code import Code

class AssemblerException(Exception):
    pass

def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    parser = Parser(input_file)
    symbol_table = SymbolTable()
    first_pass(parser, symbol_table)
    second_pass(parser, symbol_table)
    translate_file(parser, output_file)

def first_pass(parser: Parser, symbol_table: SymbolTable) -> None:
    while parser.has_more_commands():
        while parser.command_type() == L_COMMAND:
            symbol_table.add_entry(parser.symbol(), parser.current_command_index)
            parser.remove_current_command()
        parser.advance()
    # last instruction can't be an L_COMMAND
    parser.restart()

def second_pass(parser: Parser, symbol_table: SymbolTable) -> None:
    n = 16
    parser.restart()
    while parser.has_more_commands():
        if parser.command_type() == A_COMMAND and not parser.symbol().isdigit(): # handling variables
            if symbol_table.contains(parser.symbol()):
                address = symbol_table.get_address(parser.symbol())
                parser.change_current_command(f"@{address}")
            else:
                symbol_table.add_entry(parser.symbol(), n)
                parser.change_current_command(f"@{n}")
                n += 1
        elif parser.command_type == C_COMMAND:
            pass
        elif parser.command_type == L_COMMAND:
            raise AssemblerException("translating the L_COMMAND was unsuccessful")
        parser.advance()
    parser.restart()

def translate_instruction(parser: Parser) -> str:
    if parser.command_type() == C_COMMAND:
        c = parser.comp()
        d = parser.dest()
        j = parser.jump()

        pref = Code.prefix(c)
        cc = Code.comp(c)
        dd = Code.dest(d)
        jj = Code.jump(j)

        instruction = pref + cc + dd + jj

    elif parser.command_type() == A_COMMAND:
        decimal_symbol = parser.symbol()
        bin_symbol = Code.decimal_to_15bit(decimal_symbol)

        instruction = "0" + bin_symbol

    else:
        pass

    return instruction

def translate_file(parser: Parser, output_file: typing.TextIO) -> None:
    output_lines = []
    while parser.has_more_commands():
        instruction = translate_instruction(parser)
        output_lines.append(instruction + '\n')
        parser.advance()
    # one more iteration for the last instruction
    instruction = translate_instruction(parser)
    output_lines.append(instruction)
    output_file.writelines(output_lines)



if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
