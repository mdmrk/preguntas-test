import json
import re
import sys
from pathlib import Path

def parse_quiz_data(text):
    """
    Parse quiz data from the given text format into a list of question dictionaries.
    """
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
    questions = []
    i = 0
    question_id = 1
    
    while i < len(lines):
        # First line is always the question
        if i < len(lines):
            question_text = lines[i]
            i += 1
        else:
            break
            
        # Second line is always the answer index (1-4)
        if i < len(lines) and lines[i].isdigit() and lines[i] in ['1', '2', '3', '4']:
            answer_num = int(lines[i]) - 1
            i += 1
        else:
            # Skip this question if no valid answer found
            continue
            
        # Collect the options (remaining lines until next question or end)
        options = []
        option_count = 0
        
        while i < len(lines) and option_count < 4:
            option_line = lines[i]
            
            # Stop if we hit a line that looks like a new question
            # (but only if we already have at least 2 options)
            if option_count >= 2 and (
                (i + 1 < len(lines) and lines[i + 1].isdigit() and lines[i + 1] in ['1', '2', '3', '4']) or
                option_line.endswith(':')
            ):
                break
            
            # Clean up the option
            cleaned_option = option_line
            
            # Remove trailing markers
            if cleaned_option.endswith(' NO MARCAR'):
                cleaned_option = cleaned_option.replace(' NO MARCAR', '').strip()
            if cleaned_option.endswith(' REVISADA'):
                cleaned_option = cleaned_option.replace(' REVISADA', '').strip()
            if cleaned_option == 'NO MARCAR' or cleaned_option == 'REVISADA':
                i += 1
                continue
            
            # Remove "- " from beginning of options only
            cleaned_option = re.sub(r'^- ', '', cleaned_option)
            
            if cleaned_option:
                options.append(cleaned_option)
                option_count += 1
            
            i += 1
        
        # Only add if we have a complete question with at least 2 options
        if len(options) >= 2:
            questions.append({
                'id': question_id,
                'question': question_text,
                'options': options[:4],  # Take only first 4 options
                'correctAnswer': answer_num
            })
            question_id += 1
    
    return questions

def main():
    script_dir = Path(__file__).parent.absolute()
    data_dir = script_dir / ".." / "src" / "data"
    
    if len(sys.argv) < 2:
        print("Usage: python parse-netlify.py <input_filename>")
        return

    input_filename = sys.argv[1]
    name = data_dir / input_filename
    output_filename = input_filename.rsplit('.', 1)[0] + '.json'
    output_path = data_dir / output_filename
    
    # Read the input file
    content = None
    try:
        with open(name, 'r', encoding='utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{input_filename}' not found in {data_dir}.")
        return
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(name, 'r', encoding='latin-1') as file:
                content = file.read()
        except:
            print("Could not read file with UTF-8 or Latin-1 encoding.")
            return
    
    # Parse the questions
    questions = parse_quiz_data(content)
    
    print(f"Found {len(questions)} questions")
    
    # Save to output file
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            json.dump(questions, file, indent=2, ensure_ascii=False)
        print(f"Formatted quiz saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving JSON file: {e}")
        return
    
    # Only print first question as preview if available
    if questions:
        print("\nPreview of first question:")
        print("=" * 50)
        print(json.dumps(questions[0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()