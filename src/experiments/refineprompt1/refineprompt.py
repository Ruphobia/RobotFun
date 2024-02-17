#!/usr/bin/python3.8
import language_tool_python

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

def correct_text(text: str) -> str:
    """Corrects spelling and grammar in the input text."""
    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)
    return corrected_text

def main():
    print("Spelling and Grammar Correction System (type 'exit' to quit):")
    while True:
        input_text = input("\nEnter text: ")
        if input_text.lower() == "exit":
            break
        corrected_text = correct_text(input_text)
        print(f"\nCorrected Text: {corrected_text}")

if __name__ == "__main__":
    main()
