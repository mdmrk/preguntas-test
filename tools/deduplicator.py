#!/usr/bin/env python3

import json
import re
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional, Set, Tuple, Dict, Any

@dataclass
class Question:
    """Represents a test question"""
    id: int
    question: str
    options: List[str]
    correctAnswer: int
    image: Optional[str] = None
    tags: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            "id": self.id,
            "question": self.question,
            "options": self.options,
            "correctAnswer": self.correctAnswer,
        }
        if self.image:
            result["image"] = self.image
        if self.tags:
            result["tags"] = self.tags
        return result

class TestParser:
    """Parser for test JSON files"""
    
    @staticmethod
    def parse_json(data: List[Dict[str, Any]]) -> List[Question]:
        """Parse JSON data into Question objects"""
        questions = []
        
        for item in data:
            # Handle potential variations in field names if necessary, 
            # but strictly following the current schema:
            q = Question(
                id=item.get("id", 0),
                question=item.get("question", ""),
                options=item.get("options", []),
                correctAnswer=item.get("correctAnswer", -1),
                image=item.get("image"),
                tags=item.get("tags")
            )
            questions.append(q)
        
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
        if TestDeduplicator.normalize_text(q1.question) != TestDeduplicator.normalize_text(q2.question):
            return False
        
        # Compare option sets (order doesn't matter)
        options1_normalized = {TestDeduplicator.normalize_text(opt) for opt in q1.options}
        options2_normalized = {TestDeduplicator.normalize_text(opt) for opt in q2.options}
        
        return options1_normalized == options2_normalized
    
    @staticmethod
    def standardize_option_order(canonical_question: Question, duplicate_question: Question) -> Question:
        """
        Reorder the options of duplicate_question to match the order in canonical_question.
        Also updates the correctAnswer accordingly.
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
                    if j == duplicate_question.correctAnswer:
                        new_correct_answer_index = i
                    break
        
        # Create new question with reordered options
        return Question(
            id=duplicate_question.id,
            question=duplicate_question.question,
            options=reordered_options,
            correctAnswer=new_correct_answer_index,
            image=duplicate_question.image,
            tags=duplicate_question.tags
        )
    
    @staticmethod
    def merge_tags(tags1: Optional[List[str]], tags2: Optional[List[str]]) -> Optional[List[str]]:
        """
        Merge two lists of tags, removing duplicates and maintaining order.
        """
        if not tags1 and not tags2:
            return None
        if not tags1:
            return tags2
        if not tags2:
            return tags1
        
        # Merge while preserving order and removing duplicates
        merged = []
        seen = set()
        
        for tag in tags1 + tags2:
            normalized_tag = tag.lower().strip()
            if normalized_tag not in seen:
                merged.append(tag.strip())
                seen.add(normalized_tag)
        
        return merged
    
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
        Remove duplicate questions, keeping the first occurrence and merging tags.
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
        
        # Merge tags for each group and standardize option orders
        tags_merges = {}
        standardized_questions = {}
        
        for idx, leader in duplicate_groups.items():
            if leader not in tags_merges:
                tags_merges[leader] = questions[leader].tags
                # The leader question is the canonical version for option ordering
                standardized_questions[leader] = questions[leader]
            
            if idx != leader:
                # Merge tags
                tags_merges[leader] = TestDeduplicator.merge_tags(
                    tags_merges[leader], 
                    questions[idx].tags
                )
                
                # Standardize the duplicate's option order to match the leader
                # (This part might be redundant if we are removing the duplicate key,
                # but good for consistency if we ever kept duplicates)
                
        # Create the result list
        unique_questions = []
        for i, question in enumerate(questions):
            if i not in indices_to_remove:
                # If this question had duplicates, use the merged tags
                if i in tags_merges:
                    # Create a new question with merged tags
                    merged_question = Question(
                        id=question.id,
                        question=question.question,
                        options=question.options,
                        correctAnswer=question.correctAnswer,
                        image=question.image,
                        tags=tags_merges[i]
                    )
                    unique_questions.append(merged_question)
                else:
                    unique_questions.append(question)
        
        num_removed = len(indices_to_remove)
        return unique_questions, num_removed

def process_file(file_path: Path) -> Tuple[int, int]:
    """
    Process a single JSON file to remove duplicates.
    Returns (original_count, final_count).
    """
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"  ❌ Error: {file_path.name} is not a list of questions.")
            return 0, 0

        # Parse questions
        questions = TestParser.parse_json(data)
        original_count = len(questions)
        
        if original_count == 0:
            return 0, 0
        
        # Remove duplicates and merge tags
        unique_questions, num_removed = TestDeduplicator.remove_duplicates(questions)
        final_count = len(unique_questions)
        
        if num_removed > 0:
            # Reconstruct and write the file
            # Re-index questions to ensure sequential IDs if necessary?
            # The user didn't explicitly ask for re-indexing, but it might be good practice.
            # For now, let's keep IDs as they are or potentially re-assign them.
            # The original script didn't seem to care about IDs (it was text based).
            # Let's just write them back.
            
            output_data = [q.to_dict() for q in unique_questions]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            
            print(f"  ✅ Merged {num_removed} duplicate(s): {original_count} → {final_count}")
        else:
            print(f"  ⚪ No duplicates found ({original_count} questions)")
        
        return original_count, final_count
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Error decoding JSON in {file_path.name}: {e}")
        return 0, 0
    except Exception as e:
        print(f"  ❌ Error processing {file_path.name}: {e}")
        return 0, 0

def process_directory(input_dir: Path) -> None:
    """Process all JSON files in a directory to remove duplicates"""
    
    if not input_dir.exists():
        print(f"Error: Directory '{input_dir}' not found.")
        return
    
    if not input_dir.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        return
    
    # Get all JSON files in the directory
    files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix == '.json']
    
    if not files:
        print(f"No JSON files found in '{input_dir}'")
        return
    
    print(f"Found {len(files)} JSON files in '{input_dir}'")
    
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
    print("Merging duplicate questions and combining tags...")
    process_directory(data_dir)

if __name__ == "__main__":
    main()