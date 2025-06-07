"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
A_COMMAND = "A_COMMAND"
C_COMMAND = "C_COMMAND"
L_COMMAND = "L_COMMAND"


class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        input_lines = input_file.read().splitlines()

        self.clean_input_lines = []
        for line in input_lines:
            line = line.strip()  # Remove leading/trailing whitespace
            if not line or line.startswith('//'):  # Skip empty lines and comments
                continue

            # Remove inline comments (if any)
            comment_index = line.find('//')
            if comment_index != -1:
                line = "".join(line[:comment_index].split())
            else:
                line = "".join(line.split())

            if line:  # Add non-empty instruction/label to the list
                self.clean_input_lines.append(line)

            if self.clean_input_lines:
                self.current_command_index: int = 0
                self.current_command: str = self.clean_input_lines[self.current_command_index]
        

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.current_command_index < len(self.clean_input_lines) - 1

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            self.current_command_index += 1
            self.current_command = self.clean_input_lines[self.current_command_index]
        else:
            raise Exception("reached end of file")

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        current_command = self.current_command
        if '@' in current_command:
            return A_COMMAND
        if ";" in current_command or "=" in current_command \
            or '<<' in current_command or '>>' in current_command:    
            return C_COMMAND
        if '(' in current_command:
            return L_COMMAND
        

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """        
        if self.command_type() == A_COMMAND:
            return self.current_command[1:]
        elif self.command_type() == L_COMMAND:
            return self.current_command[1:-1]
        raise Exception("symbol() is only for A_COMMANDS or L_COMMANDS")


    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == C_COMMAND:
            if "=" not in self.current_command:
                return "" # value not stored anyway
            equal_sign_index = self.current_command.find("=")
            return self.current_command[:equal_sign_index]
        return Exception("dest() is only for C_COMMANDS")

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == C_COMMAND:
            if ';' not in self.current_command:
                equal_sign_index = self.current_command.find("=")
                return self.current_command[equal_sign_index+1:]
            if "=" not in self.current_command:
                semicolon_index = self.current_command.find(";")
                return self.current_command[:semicolon_index]
            else: # There is a comp and a jump
                equal_sign_index = self.current_command.find("=")
                semicolon_index = self.current_command.find(";")
                return self.current_command[equal_sign_index+1:semicolon_index]
        raise Exception("comp() is only for C_COMMANDS")


    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == C_COMMAND:
            if ";" not in self.current_command:
                return "" # no jump
            semicolon_index = self.current_command.find(';')
            return self.current_command[semicolon_index+1:]
        raise Exception("jump() is only for C_COMMANDS")
        
    def change_current_command(self, command: str) -> None:
        self.current_command = command
        self.clean_input_lines[self.current_command_index] = self.current_command

    def remove_current_command(self) -> None:
        del self.clean_input_lines[self.current_command_index]
        self.current_command = self.clean_input_lines[self.current_command_index]
    
    def restart(self) -> None:
        self.current_command_index = 0
        self.current_command = self.clean_input_lines[self.current_command_index]




