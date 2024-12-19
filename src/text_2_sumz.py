import os
from transformers import T5Tokenizer, T5ForConditionalGeneration, BartTokenizer, BartForConditionalGeneration
import torch
from colorama import Fore
from tqdm import tqdm

# Set the environment variable for Hugging Face cache directory
transf_cache_dir = "./cache/transformers"
os.makedirs(transf_cache_dir, exist_ok=True)
os.environ["TRANSFORMERS_CACHE"] = transf_cache_dir

# Function to summarize using T5
def summarize_t5(input_text, model, tokenizer, device, max_length=1024, min_length=50, num_beams=4):
    inputs = tokenizer(input_text, return_tensors="pt", max_length=max_length, truncation=True, padding=True)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    summary_ids = model.generate(inputs['input_ids'], max_length=max_length, min_length=min_length, num_beams=num_beams, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Function to summarize using BART
def summarize_bart(input_text, model, tokenizer, device, max_length=1024, min_length=50, num_beams=4):
    inputs = tokenizer(input_text, return_tensors="pt", max_length=max_length, truncation=True, padding=True)
    inputs = {key: value.to(device) for key, value in inputs.items()}
    summary_ids = model.generate(inputs['input_ids'], max_length=max_length, min_length=min_length, num_beams=num_beams, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


# Function to save the summary to the appropriate file
def save_summary(summary, input_filename, model_name, output_dir):
    # Determine the output directory and filename
    if model_name == "T5":
        model_output_dir = os.path.join(output_dir, "T5_summaries")
        output_filename = os.path.join(model_output_dir, f"{input_filename}_t5.txt")
    elif model_name == "BART":
        model_output_dir = os.path.join(output_dir, "Bart_summaries")
        output_filename = os.path.join(model_output_dir, f"{input_filename}_bart.txt")
    
    if not os.path.exists(model_output_dir):
        os.makedirs(model_output_dir)
        print(f"Created directory: {model_output_dir}")
        
    # Save the summary to a file (append mode)
    with open(output_filename, "a", encoding="utf-8") as f:
        f.write(summary + "\n")  # Add a newline between summaries
    print(f"Summary for {input_filename} saved to {output_filename}")


# Function to process large input texts and split them into chunks if needed
def process_large_text(input_text, max_token_length=1024):
    # Split the input into manageable chunks if it's too large
    tokenized_text = input_text.split()
    if len(tokenized_text) > max_token_length:
        # Split into chunks of max_token_length
        chunks = [' '.join(tokenized_text[i:i+max_token_length]) for i in range(0, len(tokenized_text), max_token_length)]
        return chunks
    else:
        return [input_text]  # No splitting needed

# Main function to process all input files
def text_2_sumz_run(input_dir, output_dir):
    
    print(Fore.GREEN + "Summarizing Plain Text Files..." + Fore.RESET)

    # Ensure the output directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Load models and tokenizers
    t5_model_name = "t5-large"
    bart_model_name = "facebook/bart-large"
    
    # Initialize device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    # Load T5 model and tokenizer
    t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_name)
    t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_name).to(device)

    # Load BART model and tokenizer
    bart_tokenizer = BartTokenizer.from_pretrained(bart_model_name)
    bart_model = BartForConditionalGeneration.from_pretrained(bart_model_name).to(device)

    files = [filename for filename in os.listdir(input_dir) if filename.endswith(".txt")]

    for filename in tqdm(files, desc="Processing files", unit="file", dynamic_ncols=True):
        input_filepath = os.path.join(input_dir, filename)
        
        # Log the current file being processed (in blue)
        tqdm.write(f"{Fore.BLUE}Processing: {filename}{Fore.RESET}")

        try:
            # Read the input file
            with open(input_filepath, "r", encoding="utf-8") as f:
                input_text = f.read()

            # Process large text by splitting if necessary
            text_chunks = process_large_text(input_text)

            # Summarize using BART
            for chunk in text_chunks:
                bart_summary = summarize_bart(chunk, bart_model, bart_tokenizer, device)
                save_summary(bart_summary, filename.replace(".txt", ""), "BART", output_dir)
            
            # Log successful processing (in green)
            tqdm.write(f"{Fore.GREEN}Processed: {filename}{Fore.RESET}")

        except Exception as e:
            # Log failure (in red)
            tqdm.write(f"{Fore.RED}Failed to process {filename}: {e}{Fore.RESET}")

            # Summarize using T5
            for chunk in text_chunks:
                t5_summary = summarize_t5(chunk, t5_model, t5_tokenizer, device)
                save_summary(t5_summary, filename.replace(".txt", ""), "T5", output_dir)

#if __name__ == "__main__":
#    input_dir = "data/data_4_sumz"
#    output_dir = "data/data_sumz"
#    text_2_sumz_run(input_dir, output_dir)
