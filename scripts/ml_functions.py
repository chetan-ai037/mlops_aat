import os
import re
from typing import List, Dict, Optional
from collections import Counter
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TextProcessor:
    def __init__(self, input_dir: str = 'data/input', output_dir: str = 'data/output'):
        """
        Initialize TextProcessor with input and output directories.
        
        Args:
            input_dir (str): Directory for input text files
            output_dir (str): Directory for processed output files
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        # Create directories if they don't exist
        os.makedirs(input_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"TextProcessor initialized with input_dir: {input_dir}, output_dir: {output_dir}")

    def read_text_file(self, filename: str) -> str:
        """
        Read content from a text file.
        
        Args:
            filename (str): Name of the file to read
            
        Returns:
            str: Content of the file
        """
        try:
            file_path = os.path.join(self.input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            logger.info(f"Successfully read file: {filename}")
            return content
        except Exception as e:
            logger.error(f"Error reading file {filename}: {str(e)}")
            raise

    def write_text_file(self, filename: str, content: str) -> None:
        """
        Write content to a text file.
        
        Args:
            filename (str): Name of the file to write
            content (str): Content to write to the file
        """
        try:
            file_path = os.path.join(self.output_dir, filename)
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            logger.info(f"Successfully wrote to file: {filename}")
        except Exception as e:
            logger.error(f"Error writing to file {filename}: {str(e)}")
            raise

    def analyze_text(self, text: str) -> Dict:
        """
        Analyze text content and return statistics.
        
        Args:
            text (str): Text content to analyze
            
        Returns:
            dict: Dictionary containing text statistics
        """
        try:
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            
            analysis = {
                'word_count': len(words),
                'character_count': len(text),
                'sentence_count': len(sentences),
                'average_word_length': sum(len(word) for word in words) / len(words) if words else 0,
                'most_common_words': Counter(words).most_common(5)
            }
            
            logger.info("Text analysis completed successfully")
            return analysis
        except Exception as e:
            logger.error(f"Error analyzing text: {str(e)}")
            raise

    def merge_text_files(self, file_list: List[str], output_filename: str) -> None:
        """
        Merge multiple text files into one.
        
        Args:
            file_list (List[str]): List of input filenames to merge
            output_filename (str): Name of the output merged file
        """
        try:
            merged_content = []
            for filename in file_list:
                content = self.read_text_file(filename)
                merged_content.append(f"--- {filename} ---\n{content}\n")
            
            self.write_text_file(output_filename, '\n'.join(merged_content))
            logger.info(f"Successfully merged {len(file_list)} files into {output_filename}")
        except Exception as e:
            logger.error(f"Error merging files: {str(e)}")
            raise

    def search_text(self, text: str, pattern: str) -> List[str]:
        """
        Search for pattern matches in text.
        
        Args:
            text (str): Text to search in
            pattern (str): Regular expression pattern to search for
            
        Returns:
            List[str]: List of matches found
        """
        try:
            matches = re.findall(pattern, text)
            logger.info(f"Found {len(matches)} matches for pattern: {pattern}")
            return matches
        except Exception as e:
            logger.error(f"Error searching text: {str(e)}")
            raise

    def create_backup(self, filename: str) -> str:
        """
        Create a backup of a text file.
        
        Args:
            filename (str): Name of the file to backup
            
        Returns:
            str: Name of the backup file created
        """
        try:
            content = self.read_text_file(filename)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"{os.path.splitext(filename)[0]}_{timestamp}.bak"
            self.write_text_file(backup_filename, content)
            logger.info(f"Created backup: {backup_filename}")
            return backup_filename
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            raise

def main():
    # Initialize the text processor
    processor = TextProcessor()
    
    # Example 1: Process a plain text file (.txt)
    text_content = """This is a plain text file example.
It contains multiple lines of text.
We can process any kind of text content!"""
    processor.write_text_file("example.txt", text_content)
    
    # Example 2: Process a Python file (.py)
    python_content = """def hello_world():
    print("Hello, World!")
    return True

if __name__ == "__main__":
    hello_world()"""
    processor.write_text_file("script_example.py", python_content)
    
    # Example 3: Process a Markdown file (.md)
    markdown_content = """# Sample Markdown
## Features
- Point 1
- Point 2

### Code Example
```python
print("Hello from markdown!")
```"""
    processor.write_text_file("readme.md", markdown_content)
    
    # Example 4: Process a configuration file (.ini)
    config_content = """[Database]
host = localhost
port = 5432
name = mydb

[API]
key = abc123
timeout = 30"""
    processor.write_text_file("config.ini", config_content)
    
    # Now let's demonstrate various operations on these files
    
    # 1. Merge all created files
    files_to_merge = ["example.txt", "script_example.py", "readme.md", "config.ini"]
    processor.merge_text_files(files_to_merge, "merged_files.txt")
    
    # 2. Analyze each file
    print("\nAnalyzing different file types:")
    for filename in files_to_merge:
        try:
            content = processor.read_text_file(filename)
            analysis = processor.analyze_text(content)
            print(f"\nAnalysis for {filename}:")
            for key, value in analysis.items():
                print(f"{key}: {value}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")
    
    # 3. Search for patterns in merged file
    print("\nSearching for patterns in merged file:")
    merged_content = processor.read_text_file("merged_files.txt")
    
    # Search for Python print statements
    print_statements = processor.search_text(merged_content, r'print\([^)]+\)')
    print("\nFound print statements:", print_statements)
    
    # Search for markdown headers
    headers = processor.search_text(merged_content, r'#+ .+')
    print("\nFound markdown headers:", headers)
    
    # Create backups of all files
    print("\nCreating backups:")
    for filename in files_to_merge:
        backup_file = processor.create_backup(filename)
        print(f"Backup created: {backup_file}")

if __name__ == "__main__":
    main() 