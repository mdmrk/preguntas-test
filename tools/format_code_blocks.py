#!/usr/bin/env python3

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
            print(f"Using config file: {clang_format_config}")
            # Run clang-format from the script directory so it finds the config
            result = subprocess.run(
                [clang_format_path, f'-style=file:{clang_format_config}', temp_file_path],
                capture_output=True,
                text=True,
                check=True,
                cwd=script_dir  # Run from script directory
            )
        else:
            print("No .clang-format config found, using Google style")
            # Fallback to Google style
            result = subprocess.run(
                [clang_format_path, '-style=Google', temp_file_path],
                capture_output=True,
                text=True,
                check=True
            )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return result.stdout.strip()
    
    except subprocess.CalledProcessError as e:
        print(f"Error running clang-format: {e}")
        return code  # Return original code if formatting fails
    except Exception as e:
        print(f"Unexpected error: {e}")
        return code

def is_cpp_code(code):
    """
    Basic heuristic to detect if code block contains C++ code
    """
    cpp_indicators = [
        r'\b(unsigned|int|char|float|double|bool|void|class|struct|namespace)\b',
        r'#include\s*[<"]',
        r'\bstd::\w+',
        r'\b(cout|cin|endl)\b',
        r'\b(if|for|while|switch|return)\s*\(',
        r'\b(public|private|protected)\s*:',
        r'->\s*\w+',
        r'::\w+',
        r'\w+\s*\([^)]*\)\s*\{',  # function definitions
    ]
    
    return any(re.search(pattern, code, re.IGNORECASE) for pattern in cpp_indicators)

def format_code_blocks(text):
    """
    Find and format C++ code blocks using the specified regex
    """
    # Regex pattern as provided by user
    code_block_regex = r'```(?:\w+)?\s*([\s\S]*?)\s*```'
    
    blocks_formatted = 0
    
    def replace_code_block(match):
        nonlocal blocks_formatted
        code = match.group(1)
        
        # Check if this looks like C++ code
        if is_cpp_code(code):
            print(f"Formatting C++ code block {blocks_formatted + 1}...")
            formatted_code = format_cpp_with_clang(code)
            blocks_formatted += 1
            return f"```cpp\n{formatted_code}\n```"
        else:
            # For non-C++ blocks, just clean up whitespace
            cleaned_code = code.strip()
            return f"```\n{cleaned_code}\n```"
    
    # Apply the regex replacement
    result = re.sub(code_block_regex, replace_code_block, text, flags=re.MULTILINE)
    
    return result, blocks_formatted

def process_directory(input_dir, output_dir=None):
    """
    Process all files in a directory
    """
    input_path = Path(input_dir)
    
    if not input_path.exists():
        print(f"Error: Directory '{input_path}' not found.")
        return
    
    if not input_path.is_dir():
        print(f"Error: '{input_path}' is not a directory.")
        return
    
    # Get all files in the directory
    files = [f for f in input_path.iterdir() if f.is_file()]
    
    if not files:
        print(f"No files found in '{input_path}'")
        return
    
    print(f"Found {len(files)} files in '{input_path}'")
    
    total_blocks = 0
    processed_files = 0
    
    for file_path in files:
        try:
            print(f"\nProcessing: {file_path.name}")
            
            # Read the file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            # Format code blocks
            formatted_text, blocks_count = format_code_blocks(text)
            
            if blocks_count > 0:
                # Write back to the same file (overwrite)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_text)
                print(f"  ✅ Formatted {blocks_count} C++ code blocks and updated file")
                total_blocks += blocks_count
                processed_files += 1
            else:
                print(f"  ⚪ No C++ code blocks found")
                
        except Exception as e:
            print(f"  ❌ Error processing {file_path.name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"SUMMARY:")
    print(f"Files processed: {processed_files}/{len(files)}")
    print(f"Total C++ blocks formatted: {total_blocks}")
    print(f"{'='*50}")

def main():
    """
    Main function to process text file, directory, or stdin
    
    Expected directory structure:
    ├── formatter.py          # This script
    ├── .clang-format         # Your custom clang-format config
    ├── clang-format          # (Optional) clang-format executable
    └── src/data/            # Directory with files to format
        ├── file1.txt
        ├── file2.md
        └── ...
    """
    
    # Process ../src/data directory
    script_dir = Path(__file__).parent.absolute()
    data_dir = script_dir / ".." / "src" / "data"
    
    print(f"Processing all files in: {data_dir.resolve()}")
    process_directory(data_dir)

if __name__ == "__main__":
    main()