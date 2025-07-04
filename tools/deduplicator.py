#!/usr/bin/env python3

import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Set, Tuple
import itertools

@dataclass
class Question:
    """Represents a test question"""
    question_text: str
    options: List[str]
    correct_answer_index: int
    image: Optional[str] = None
    categories: Optional[str] = None  # Categories separated by semicolons
    raw_chunk: str = ""  # Store original text for reconstruction

class TestParser:
    """Parser for test text files"""
    
    @staticmethod
    def parse_test_text(text: str) -> List[Question]:
        """Parse test text into Question objects"""
        chunks = re.split(r'^,$', text, flags=re.MULTILINE)
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
            categories = None
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
                elif line.startswith("C:"):
                    categories = line[2:].strip()
                    parsing_question = False
                    parsing_option = False
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
                    categories=categories,
                    raw_chunk=chunk  # Store the original chunk
                ))
        
        return questions

class TestDeduplicator:
    """Remove duplicate questions from test files"""
    
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
        if TestDeduplicator.normalize_text(q1.question_text) != TestDeduplicator.normalize_text(q2.question_text):
            return False
        
        # Compare option sets (order doesn't matter)
        options1_normalized = {TestDeduplicator.normalize_text(opt) for opt in q1.options}
        options2_normalized = {TestDeduplicator.normalize_text(opt) for opt in q2.options}
        
        return options1_normalized == options2_normalized
    
    @staticmethod
    def standardize_option_order(canonical_question: Question, duplicate_question: Question) -> Question:
        """
        Reorder the options of duplicate_question to match the order in canonical_question.
        Also updates the correct_answer_index accordingly.
        """
        # Create mapping from normalized option text to original option text for both questions
        canonical_options_normalized = [TestDeduplicator.normalize_text(opt) for opt in canonical_question.options]
        duplicate_options_normalized = [TestDeduplicator.normalize_text(opt) for opt in duplicate_question.options]
        
        # Create reordered options list matching canonical order
        reordered_options = []
        new_correct_answer_index = -1
        
        # For each option in canonical order, find the corresponding option in duplicate
        for i, canonical_opt_norm in enumerate(canonical_options_normalized):
            # Find this option in the duplicate question
            for j, duplicate_opt_norm in enumerate(duplicate_options_normalized):
                if canonical_opt_norm == duplicate_opt_norm:
                    reordered_options.append(duplicate_question.options[j])
                    # If this was the correct answer in the duplicate, update the index
                    if j == duplicate_question.correct_answer_index:
                        new_correct_answer_index = i
                    break
        
        # Create new question with reordered options
        return Question(
            question_text=duplicate_question.question_text,
            options=reordered_options,
            correct_answer_index=new_correct_answer_index,
            image=duplicate_question.image,
            categories=duplicate_question.categories,
            raw_chunk=duplicate_question.raw_chunk
        )
    
    @staticmethod
    def merge_categories(cat1: Optional[str], cat2: Optional[str]) -> Optional[str]:
        """
        Merge two category strings, removing duplicates and maintaining order.
        Categories are separated by semicolons.
        
        If one question has categories and the other doesn't, preserves the categories.
        """
        if not cat1 and not cat2:
            return None
        if not cat1:  # First has no categories, second has categories
            return cat2
        if not cat2:  # First has categories, second has no categories
            return cat1
        
        # Split categories by semicolon and normalize
        cats1 = [cat.strip() for cat in cat1.split(';') if cat.strip()]
        cats2 = [cat.strip() for cat in cat2.split(';') if cat.strip()]
        
        # Merge while preserving order and removing duplicates
        merged = []
        seen = set()
        
        for cat in cats1 + cats2:
            if cat.lower() not in seen:
                merged.append(cat)
                seen.add(cat.lower())
        
        return ';'.join(merged) if merged else None
    
    @staticmethod
    def find_duplicates(questions: List[Question]) -> List[Tuple[int, int]]:
        """
        Find all pairs of duplicate questions.
        Returns list of (index1, index2) tuples where index1 < index2.
        """
        duplicates = []
        
        for i in range(len(questions)):
            for j in range(i + 1, len(questions)):
                if TestDeduplicator.questions_are_duplicate(questions[i], questions[j]):
                    duplicates.append((i, j))
        
        return duplicates
    
    @staticmethod
    def remove_duplicates(questions: List[Question]) -> Tuple[List[Question], int]:
        """
        Remove duplicate questions, keeping the first occurrence and merging categories.
        Standardizes option order across duplicates to match the first occurrence.
        Returns (unique_questions, num_removed).
        """
        if not questions:
            return [], 0
        
        # Find all duplicate pairs
        duplicate_pairs = TestDeduplicator.find_duplicates(questions)
        
        if not duplicate_pairs:
            return questions, 0
        
        # Create a mapping of which questions are duplicates of which
        duplicate_groups = {}
        indices_to_remove = set()
        
        for first_idx, second_idx in duplicate_pairs:
            # Find the group leader (lowest index in the group)
            if first_idx in duplicate_groups:
                leader = duplicate_groups[first_idx]
            else:
                leader = first_idx
                duplicate_groups[first_idx] = first_idx
            
            # Add the second question to the same group
            duplicate_groups[second_idx] = leader
            indices_to_remove.add(second_idx)
        
        # Merge categories for each group and standardize option orders
        category_merges = {}
        standardized_questions = {}
        
        for idx, leader in duplicate_groups.items():
            if leader not in category_merges:
                category_merges[leader] = questions[leader].categories
                # The leader question is the canonical version for option ordering
                standardized_questions[leader] = questions[leader]
            
            if idx != leader:
                # Merge categories
                category_merges[leader] = TestDeduplicator.merge_categories(
                    category_merges[leader], 
                    questions[idx].categories
                )
                
                # Standardize the duplicate's option order to match the leader
                standardized_duplicate = TestDeduplicator.standardize_option_order(
                    questions[leader], questions[idx]
                )
                # Store the standardized version (though we'll remove it anyway)
                standardized_questions[idx] = standardized_duplicate
        
        # Create the result list
        unique_questions = []
        for i, question in enumerate(questions):
            if i not in indices_to_remove:
                # If this question had duplicates, use the merged categories
                if i in category_merges:
                    # Create a new question with merged categories
                    merged_question = Question(
                        question_text=question.question_text,
                        options=question.options,
                        correct_answer_index=question.correct_answer_index,
                        image=question.image,
                        categories=category_merges[i],
                        raw_chunk=question.raw_chunk
                    )
                    unique_questions.append(merged_question)
                else:
                    unique_questions.append(question)
        
        num_removed = len(indices_to_remove)
        return unique_questions, num_removed
    
    @staticmethod
    def reconstruct_test_text(questions: List[Question]) -> str:
        """Reconstruct test text from Question objects using original formatting"""
        if not questions:
            return ""
        
        chunks = []
        for question in questions:
            # Reconstruct the chunk with proper formatting
            chunk_lines = []
            
            # Add question
            if '\n' in question.question_text:
                lines = question.question_text.split('\n')
                chunk_lines.append(f"Q: {lines[0]}")
                for line in lines[1:]:
                    chunk_lines.append(line)
            else:
                chunk_lines.append(f"Q: {question.question_text}")
            
            # Add answer
            chunk_lines.append(f"A: {question.correct_answer_index}")
            
            # Add categories if present
            if question.categories:
                chunk_lines.append(f"C: {question.categories}")
            
            # Add options
            for option in question.options:
                if '\n' in option:
                    lines = option.split('\n')
                    chunk_lines.append(f"O: {lines[0]}")
                    for line in lines[1:]:
                        chunk_lines.append(line)
                else:
                    chunk_lines.append(f"O: {option}")
            
            # Add image if present
            if question.image:
                chunk_lines.append(f"I: {question.image}")
            
            chunks.append('\n'.join(chunk_lines))
        
        return '\n,\n'.join(chunks)

def process_file(file_path: Path) -> Tuple[int, int]:
    """
    Process a single test file to remove duplicates.
    Returns (original_count, final_count).
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        
        # Parse questions
        questions = TestParser.parse_test_text(text)
        original_count = len(questions)
        
        if original_count == 0:
            return 0, 0
        
        # Remove duplicates and merge categories
        unique_questions, num_removed = TestDeduplicator.remove_duplicates(questions)
        final_count = len(unique_questions)
        
        if num_removed > 0:
            # Reconstruct and write the file
            new_text = TestDeduplicator.reconstruct_test_text(unique_questions)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_text)
            
            print(f"  ✅ Merged {num_removed} duplicate(s): {original_count} → {final_count}")
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
    print(f"Total duplicates merged: {total_removed}")
    if total_original > 0:
        percentage = (total_removed / total_original) * 100
        print(f"Reduction: {percentage:.1f}%")
    print(f"{'='*50}")

def main():
    """Main function to process ../src/data directory"""
    script_dir = Path(__file__).parent.absolute()
    data_dir = script_dir / ".." / "src" / "data"
    
    print(f"Processing all test files in: {data_dir.resolve()}")
    print("Merging duplicate questions and combining categories...")
    process_directory(data_dir)

if __name__ == "__main__":
    main()