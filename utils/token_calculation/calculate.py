import math
import tiktoken  # Make sure you have the tiktoken package installed

class Cal:
    def __init__(self, model='gpt-4o'):  # Specify the model to use for token encoding
        self.model = model

    def calc_token(self, in_text, out_text):
        enc = tiktoken.encoding_for_model(self.model)
        return len(enc.encode(str(out_text) + str(in_text)))

    def calc_money(self, in_text, out_text):
        return (self.calc_token(in_text, out_text) * 0.005 + self.calc_token(out_text, in_text) * 0.015) / 1000


def read_context_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # Read the file and filter out empty lines
        lines = [line.strip() for line in file if line.strip()]
    return " ".join(lines)  # Join all lines into a single string


# Read input and output context from files
input_context = read_context_from_file('./input.txt')
output_context = read_context_from_file('./output.txt')

# Create a calculator object
calculator = Cal()

# Calculate the cost
money = calculator.calc_money(input_context, output_context)

# Print the result
print(f"The total cost is: {money}")