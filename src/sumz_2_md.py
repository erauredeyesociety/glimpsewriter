import os
import spacy
import re
from colorama import Fore

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

def extract_key_elements(text):
    # Process the raw text to detect named entities
    doc = nlp(text)
    
    # Initialize variables
    title = None
    author = None
    themes = []
    conclusion = None
    
    # Extract named entities (works of art, people)
    for ent in doc.ents:
        if ent.label_ == "WORK_OF_ART":
            title = ent.text
        elif ent.label_ == "PERSON":
            author = ent.text
    
    # Extract themes using a simple heuristic (looking for 'themes' keyword)
    if "themes" in text.lower():
        themes_start = text.lower().find("themes")
        if themes_start != -1:
            themes_section = text[themes_start:text.find("\n", themes_start)]
            themes = [t.strip() for t in themes_section.split(",")]

    # Extract conclusion using a simple heuristic (looking for 'conclusion' keyword)
    if "conclusion" in text.lower():
        conclusion_start = text.lower().find("conclusion")
        if conclusion_start != -1:
            conclusion_section = text[conclusion_start:text.find("\n", conclusion_start)]
            conclusion = conclusion_section.strip()

    return title, author, themes, conclusion

def generate_markdown_from_summary(summary_text):
    # Extract key elements from the summary
    title, author, themes, conclusion = extract_key_elements(summary_text)

    # Start building the markdown text
    markdown = ""
    
    if title:
        markdown += f"# {title}\n\n"
    if author:
        markdown += f"## Author: {author}\n\n"
    
    # If themes are detected, list them
    if themes:
        markdown += "## Themes\n"
        for theme in themes:
            markdown += f"- {theme}\n"
    
    # If a conclusion is detected, add it as a section
    if conclusion:
        markdown += f"## Conclusion\n{conclusion}\n"
    
    # Append the raw summary as the final section
    markdown += "\n## Raw Summary\n"
    markdown += summary_text
    
    return markdown

def process_file(input_file, output_dir):
    # Open and read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        summary_text = file.read()

    # Process the summary in chunks (e.g., 1000 characters at a time)
    chunk_size = 1000
    markdown_output = ""
    for i in range(0, len(summary_text), chunk_size):
        chunk = summary_text[i:i + chunk_size]
        markdown_output += generate_markdown_from_summary(chunk) + "\n\n"
    
    # Get the filename without extension
    base_filename = os.path.basename(input_file)
    filename_without_ext = os.path.splitext(base_filename)[0]
    
    # Define the output path with markdown extension
    output_file = os.path.join(output_dir, f"{filename_without_ext}.md")
    
    # Write the markdown output to the file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_output)

def sumz_2_md_run(input_dir, output_dir):
    print(Fore.GREEN + "Plain Text Summaries To Meaningful Markdown..." + Fore.RESET)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Process each text file in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_file = os.path.join(input_dir, filename)
            print(f"Processing {input_file}...")
            process_file(input_file, output_dir)

#if __name__ == "__main__":
#    input_dir = "data/data_sumz"
#    output_dir = "data/data_sumz_md"
#    sumz_2_md_run(input_dir, output_dir)
