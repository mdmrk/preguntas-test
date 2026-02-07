#!/usr/bin/env python3

import json
import re
import subprocess
import tempfile
import os
import sys
import platform
from pathlib import Path

def find_clang_format():
    """
    Find clang-format executable, first in script directory, then in PATH
    """
    script_dir = Path(__file__).parent.absolute()
    
    # Determine executable name based on OS
    exe_name = "clang-format"
    if platform.system() == "Windows":
        exe_name += ".exe"
    
    # First, try to find clang-format in the same directory as this script
    local_clang_format = script_dir / exe_name
    if local_clang_format.exists() and local_clang_format.is_file():
        return str(local_clang_format)
    
    # If not found locally, try system PATH
    try:
        result = subprocess.run(['which', exe_name], capture_output=True, text=True)
        if result.returncode == 0:
            return exe_name
    except:
        pass
    
    # On Windows, try 'where' command instead of 'which'
    if platform.system() == "Windows":
        try:
            result = subprocess.run(['where', exe_name], capture_output=True, text=True)
            if result.returncode == 0:
                return exe_name
        except:
            pass
    
    return None

def format_cpp_with_clang(code):
    """
    Format C++ code using clang-format with custom config
    """
    clang_format_path = find_clang_format()
    script_dir = Path(__file__).parent.absolute()
    
    if not clang_format_path:
        print("Error: clang-format not found.")
        print("Please either:")
        print("1. Copy clang-format executable to the same directory as this script, or")
        print("2. Install clang-format system-wide:")
        print("   - Ubuntu/Debian: sudo apt install clang-format")
        print("   - macOS: brew install clang-format") 
        print("   - Windows: Install LLVM from https://llvm.org/")
        return code
    
    try:
        # Create a temporary file with .cpp extension
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        # Check for .clang-format config file in script directory
        clang_format_config = script_dir / '.clang-format'
        
        if clang_format_config.exists():
            # Run clang-format from the script directory so it finds the config
            subprocess.run(
                [clang_format_path, f'-style=file:{clang_format_config}', '-i', temp_file_path],
                capture_output=True,
                text=True,
                check=True,
                cwd=script_dir  # Run from script directory
            )
        else:
            print("No .clang-format config found, using Google style")
            # Fallback to Google style
            subprocess.run(
                [clang_format_path, '-style=Google', '-i', temp_file_path],
                capture_output=True,
                text=True,
                check=True
            )
        
        # Read back the formatted code
        with open(temp_file_path, 'r') as f:
            formatted_code = f.read()
            
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return formatted_code.strip()
    
    except subprocess.CalledProcessError as e:
        print(f"Error running clang-format: {e}")
        return code  # Return original code if formatting fails
    except Exception as e:
        print(f"Unexpected error: {e}")
        return code

def format_code_blocks_in_text(text):
    """
    Find and format only ```cpp code blocks using clang-format in a string
    """
    # Only match code blocks specifically marked as cpp
    cpp_code_block_regex = r'```cpp\s*([\s\S]*?)\s*```'
    
    blocks_formatted = 0
    
    def replace_cpp_block(match):
        nonlocal blocks_formatted
        code = match.group(1)
        
        # Check if code needs formatting (simple check to avoid re-formatting identical code if possible,
        # but clang-format is idempotent so it's fine to run it)
        formatted_code = format_cpp_with_clang(code)
        
        if formatted_code != code.strip():
            blocks_formatted += 1
            
        return f"```cpp\n{formatted_code}\n```"
    
    # Apply the regex replacement only to cpp blocks
    result = re.sub(cpp_code_block_regex, replace_cpp_block, text, flags=re.MULTILINE)
    
    return result, blocks_formatted

def process_question(question_obj):
    """
    Process a single question object (dict) to format code blocks in its fields
    """
    blocks_count = 0
    
    # Format 'question' field
    if 'question' in question_obj and isinstance(question_obj['question'], str):
        formatted_text, count = format_code_blocks_in_text(question_obj['question'])
        if count > 0:
            question_obj['question'] = formatted_text
            blocks_count += count
            
    # Format 'options' field
    if 'options' in question_obj and isinstance(question_obj['options'], list):
        new_options = []
        for opt in question_obj['options']:
            if isinstance(opt, str):
                formatted_opt, count = format_code_blocks_in_text(opt)
                if count > 0:
                    blocks_count += count
                new_options.append(formatted_opt)
            else:
                new_options.append(opt)
        question_obj['options'] = new_options
        
    return blocks_count

def process_file(file_path):
    """
    Process a single JSON file
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            print(f"  ⚪ Skipping {file_path.name}: Not a list of questions")
            return 0
            
        total_file_blocks = 0
        
        for question in data:
            total_file_blocks += process_question(question)
            
        if total_file_blocks > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"  ✅ Formatted {total_file_blocks} C++ code blocks in {file_path.name}")
        else:
            print(f"  ⚪ No C++ code blocks formatted in {file_path.name}")
            
        return total_file_blocks
        
    except json.JSONDecodeError:
        print(f"  ❌ Error: {file_path.name} is not valid JSON")
        return 0
    except Exception as e:
        print(f"  ❌ Error processing {file_path.name}: {e}")
        return 0

def process_directory(input_dir):
    """
    Process all JSON files in a directory
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"Error: Directory '{input_path}' not found.")
        return
    
    if not input_path.is_dir():
        print(f"Error: '{input_path}' is not a directory.")
        return
    
    # Get all JSON files in the directory
    files = [f for f in input_path.iterdir() if f.is_file() and f.suffix == '.json']
    
    if not files:
        print(f"No JSON files found in '{input_path}'")
        return
    
    print(f"Found {len(files)} JSON files in '{input_path}'")
    
    total_blocks = 0
    processed_files = 0
    
    for file_path in files:
        print(f"\nProcessing: {file_path.name}")
        blocks_formatted = process_file(file_path)
        
        if blocks_formatted > 0:
            total_blocks += blocks_formatted
            processed_files += 1
    
    print(f"\n{'='*50}")
    print(f"SUMMARY:")
    print(f"Files processed: {processed_files}/{len(files)}")
    print(f"Total C++ blocks formatted: {total_blocks}")
    print(f"{'='*50}")

def main():
    """
    Main function
    """
    # Process ../src/data directory
    script_dir = Path(__file__).parent.absolute()
    data_dir = script_dir / ".." / "src" / "data"
    
    print(f"Processing all JSON files in: {data_dir.resolve()}")
    process_directory(data_dir)

if __name__ == "__main__":
    main()
