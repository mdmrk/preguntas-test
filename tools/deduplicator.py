#!/usr/bin/env python3

import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple
import itertools

@dataclass
class Question:
    """Represents a quiz question"""
    question_text: str
    options: List[str]
    correct_answer_index: int
    image: Optional[str] = None
    raw_chunk: str = ""  # Store original text for reconstruction

class QuizParser:
    """Parser for quiz text files"""
    
    @staticmethod
    def parse_quiz_text(text: str) -> List[Question]:
        """Parse quiz text into Question objects"""
        chunks = text.split("\n\n")
        questions = []
        
        for chunk in chunks:
            if not chunk.strip():
                continue
                
            lines = [line for line in chunk.split("\n") if line.strip()]
            if not lines:
                continue
            
            question_text = ""
            correct_answer_index = -1
            image = None
            options = []
            
            parsing_question = False
            parsing_option = False
            current_option_index = -1
            
            for line in lines:
                if line.startswith("O:"):
                    options.append(line[2:].strip())
                    current_option_index = len(options) - 1
                    parsing_question = False
                    parsing_option = True
                elif line.startswith("Q:"):
                    question_text = line[2:].strip()
                    parsing_question = True
                    parsing_option = False
                elif line.startswith("A:"):
                    try:
                        correct_answer_index = int(line[2:].strip())
                    except ValueError:
                        correct_answer_index = -1
                    parsing_question = False
                    parsing_option = False
                elif line.startswith("I:"):
                    image = line[2:].strip()
                    parsing_question = False
                    parsing_option = False
                elif parsing_question:
                    question_text += "\n" + line.strip()
                elif parsing_option and current_option_index >= 0:
                    options[current_option_index] += "\n" + line.strip()
            
            # Only add valid questions
            if question_text and correct_answer_index >= 0 and options:
                questions.append(Question(
                    question_text=question_text.strip(),
                    options=[opt.strip() for opt in options],
                    correct_answer_index=correct_answer_index,
                    image=image,
                    raw_chunk=chunk  # Store the original chunk
                ))
        
        return questions

class QuizDeduplicator:
    """Remove duplicate questions from quiz files"""
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for comparison (remove extra whitespace, etc.)"""
        # Remove extra whitespace, normalize line breaks
        normalized = re.sub(r'\s+', ' ', text.strip())
        return normalized.lower()
    
    @staticmethod
    def questions_are_duplicate(q1: Question, q2: Question) -> bool:
        """
        Check if two questions are duplicates.
        Questions are duplicates if they have the same question text and the same set of options
        (regardless of order).
        """
        # Compare normalized question texts
        if QuizDeduplicator.normalize_text(q1.question_text) != QuizDeduplicator.normalize_text(q2.question_text):
            return False
        
        # Compare option sets (order doesn't matter)
        options1_normalized = {QuizDeduplicator.normalize_text(opt) for opt in q1.options}
        options2_normalized = {QuizDeduplicator.normalize_text(opt) for opt in q2.options}
        
        return options1_normalized == options2_normalized
    
    @staticmethod
    def find_duplicates(questions: List[Question]) -> List[Tuple[int, int]]:
        """
        Find all pairs of duplicate questions.
        Returns list of (index1, index2) tuples where index1 < index2.
        """
        duplicates = []
        
        for i in range(len(questions)):
            for j in range(i + 1, len(questions)):
                if QuizDeduplicator.questions_are_duplicate(questions[i], questions[j]):
                    duplicates.append((i, j))
        
        return duplicates
    
    @staticmethod
    def remove_duplicates(questions: List[Question]) -> Tuple[List[Question], int]:
        """
        Remove duplicate questions, keeping the first occurrence of each.
        Returns (unique_questions, num_removed).
        """
        if not questions:
            return [], 0
        
        # Find all duplicate pairs
        duplicate_pairs = QuizDeduplicator.find_duplicates(questions)
        
        # Get indices of questions to remove (keep first occurrence)
        indices_to_remove = set()
        for _, second_index in duplicate_pairs:
            indices_to_remove.add(second_index)
        
        # Keep questions that are not marked for removal
        unique_questions = []
        for i, question in enumerate(questions):
            if i not in indices_to_remove:
                unique_questions.append(question)
        
        num_removed = len(indices_to_remove)
        return unique_questions, num_removed
    
    @staticmethod
    def reconstruct_quiz_text(questions: List[Question]) -> str:
        """Reconstruct quiz text from Question objects using original formatting"""
        if not questions:
            return ""
        
        chunks = []
        for question in questions:
            # Use the original raw_chunk to preserve formatting
            if question.raw_chunk:
                chunks.append(question.raw_chunk)
            else:
                # Fallback to reconstruction if raw_chunk is missing
                chunk_lines = []
                
                # Add question
                if '\n' in question.question_text:
                    lines = question.question_text.split('\n')
                    chunk_lines.append(f"Q: {lines[0]}")
                    for line in lines[1:]:
                        chunk_lines.append(line)
                else:
                    chunk_lines.append(f"Q: {question.question_text}")
                
                # Add options
                for option in question.options:
                    if '\n' in option:
                        lines = option.split('\n')
                        chunk_lines.append(f"O: {lines[0]}")
                        for line in lines[1:]:
                            chunk_lines.append(line)
                    else:
                        chunk_lines.append(f"O: {option}")
                
                # Add answer
                chunk_lines.append(f"A: {question.correct_answer_index}")
                
                # Add image if present
                if question.image:
                    chunk_lines.append(f"I: {question.image}")
                
                chunks.append('\n'.join(chunk_lines))
        
        return '\n\n'.join(chunks)

def process_file(file_path: Path) -> Tuple[int, int]:
    """
    Process a single quiz file to remove duplicates.
    Returns (original_count, final_count).
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        # Parse questions
        questions = QuizParser.parse_quiz_text(text)
        original_count = len(questions)
        
        if original_count == 0:
            return 0, 0
        
        # Remove duplicates
        unique_questions, num_removed = QuizDeduplicator.remove_duplicates(questions)
        final_count = len(unique_questions)
        
        if num_removed > 0:
            # Reconstruct and write the file
            new_text = QuizDeduplicator.reconstruct_quiz_text(unique_questions)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_text)
            
            print(f"  ✅ Removed {num_removed} duplicate(s): {original_count} → {final_count}")
        else:
            print(f"  ⚪ No duplicates found ({original_count} questions)")
        
        return original_count, final_count
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path.name}: {e}")
        return 0, 0

def process_directory(input_dir: Path) -> None:
    """Process all files in a directory to remove duplicates"""
    
    if not input_dir.exists():
        print(f"Error: Directory '{input_dir}' not found.")
        return
    
    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        return
    
    # Get all files in the directory
    files = [f for f in input_dir.iterdir() if f.is_file()]
    
    if not files:
        print(f"No files found in '{input_dir}'")
        return
    
    print(f"Found {len(files)} files in '{input_dir}'")
    
    total_original = 0
    total_final = 0
    processed_files = 0
    
    for file_path in files:
        print(f"\nProcessing: {file_path.name}")
        original_count, final_count = process_file(file_path)
        
        if original_count > 0:
            total_original += original_count
            total_final += final_count
            processed_files += 1
    
    total_removed = total_original - total_final
    
    print(f"\n{'='*50}")
    print(f"SUMMARY:")
    print(f"Files processed: {processed_files}/{len(files)}")
    print(f"Total questions: {total_original} → {total_final}")
    print(f"Total duplicates removed: {total_removed}")
    if total_original > 0:
        percentage = (total_removed / total_original) * 100
        print(f"Reduction: {percentage:.1f}%")
    print(f"{'='*50}")

def main():
    """Main function to process ../src/data directory"""
    script_dir = Path(__file__).parent.absolute()
    data_dir = script_dir / ".." / "src" / "data"
    
    print(f"Processing all quiz files in: {data_dir.resolve()}")
    print("Removing duplicate questions (accounting for shuffled options)...")
    process_directory(data_dir)

if __name__ == "__main__":
    main()