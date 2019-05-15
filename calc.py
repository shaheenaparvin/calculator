import tkinter as Tk
import math

class Calculator:
    """Main class that constructs the calculator and handles user input and calculations"""

    def __init__(self, parent):
        # Global variables needed throughout a single calculation
        self.operations = {'+': False,
                           '-': False,
                           '*': False,
                           '/': False}
        self.first_number_selected = 0
        self.second_number_selected = 0

        # Expands a button to fill all the open grid-space around it.
        expand_button = Tk.N + Tk.E + Tk.S + Tk.W

        # Display label setup
        self.display_label = Tk.Label(parent, text='0', font='Verdana 16 bold',
                                      bg='black', fg='white', height=2, width=4)
        self.display_label.grid(row=0, column=0, columnspan=4, sticky=expand_button)
        # Button Layout
        # Number buttons
        Tk.Button(parent, text='0', command=self._number_callback(0)).grid(row=4, columnspan=2, sticky=expand_button)
        for number in range(1,10):
            callback = self._number_callback(number)
            row = math.ceil(number/3)
            col = (number-1) % 3
            Tk.Button(parent, text=str(number), height=2, width=6, command=callback).grid(row=row, column=col)
        # Operation buttons
        for position, operator in enumerate(self.operations.keys()):
            Tk.Button(parent, text=operator, height=2, width=6,command=self._operation_callback(operator)).grid(row=position + 1, column=3)
        Tk.Button(parent, text='C', height=2, width=6, command=self.reset).grid(row=4, column=2)
        Tk.Button(parent, text='=', height=2, command=self.calculate_result).grid(row=5, columnspan=4, sticky=expand_button)

    def number_pressed(self, button_number):
        """This function is called when buttons 0 - 9 are pushed"""

        if not any(self.operations.values()):
            if self.first_number_selected == 0:
                self.first_number_selected = button_number
                self.display_label['text'] = str(button_number)
            else:
                self.display_label['text'] += str(button_number)
                self.first_number_selected = int(self.display_label['text'])
        elif self.second_number_selected == 0:
            self.second_number_selected = button_number
            self.display_label['text'] = str(button_number)
        else:
            self.display_label['text'] += str(button_number)
            self.second_number_selected = int(self.display_label['text'])

    def _number_callback(self, number):
        """Helper method that is creates a callback function
        for each of the buttons that indicate numbers."""
        return lambda: self.number_pressed(number)

    def operation_selected(self, operation):
        """This function is triggered when +,-,*, or / is pushed.
        First check if the first and second numbers are already selected.
        If so, it calculates the result of the operation and displays it,
            then it sets the operation to the last one pushed.
        This allows for multiply calculations before the '=' button is pushed."""
        if self.second_number_selected and self.first_number_selected:
            self.first_number_selected = self.calculate_result()
            self.display_label['text'] = str(self.first_number_selected)

        self._reset_operations()
        self.operations[operation] = True

    def _operation_callback(self, sign):
        """Helper method that is creates a callback function
        for each of the buttons that indicate operations."""
        return lambda: self.operation_selected(sign)

    def _reset_operations(self):
        """Reset the press-status of all the operations"""
        for operator in self.operations.keys():
            self.operations[operator] = False

    def calculate_result(self):
        """Performs calculation then sets up variables for future operations with the resulting number"""
        result = self.first_number_selected

        # The code can probably be rewritten in such a way that the operation that is to be performed
        # is directly accessible from the `operations` dictionary. This way if you add more operations
        # in the future, you wouldn't have to rewrite these methods in order to have them function
        # properly.
        if self.operations['+']:
            result = self.first_number_selected + self.second_number_selected
        elif self.operations['-']:
            result = self.first_number_selected - self.second_number_selected
        elif self.operations['*']:
            result = self.first_number_selected * self.second_number_selected
        elif self.operations['/']:
            result = round(self.first_number_selected / self.second_number_selected, 3)
            result = int(result) if result.is_integer() else result

        self.first_number_selected = result
        self.second_number_selected = 0  # Resets for next calculation if the clear button is not pressed
        self._reset_operations()
        self.display_label['text'] = str(result)
        return result

    def reset(self):
        """Reset all the variables to their default states"""
        self.first_number_selected = 0
        self.second_number_selected = 0
        self._reset_operations()
        self.display_label['text'] = '0'

    @staticmethod
    def run():
        frame = Tk.Tk()
        frame.wm_title('Calculator')
        frame.resizable(width=False, height=False)
        Calculator(frame)
        frame.mainloop()


def main():
    Calculator.run()

if __name__ == '__main__':
    main()
