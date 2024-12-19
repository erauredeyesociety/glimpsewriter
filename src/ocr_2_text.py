import os
from PyPDF2 import PdfReader
from colorama import Fore
from tqdm import tqdm

# use this tool to convert text to mp3
# https://audio.online-convert.com/convert/txt-to-mp3

file_names = []

prog_str = Fore.GREEN + "[+] " + Fore.RESET
neg_str = Fore.RED + "[-] " + Fore.RESET

replace_with_space = [
    "\t",
    ",\n",
    "(\n",
    ")\n",
    "[\n",
    "]\n",
    "{\n",
    "}\n",
    '"\n',
    "'\n",
    ":\n",
    ";\n",
    # the alphabet
    "A\n",
    "B\n",
    "C\n",
    "D\n",
    "E\n",
    "F\n",
    "G\n",
    "H\n",
    "I\n",
    "J\n",
    "K\n",
    "L\n",
    "M\n",
    "N\n",
    "O\n",
    "P\n",
    "Q\n",
    "R\n",
    "S\n",
    "T\n",
    "U\n",
    "V\n",
    "W\n",
    "X\n",
    "Y\n",
    "Z\n",
    "a\n",
    "b\n",
    "c\n",
    "d\n",
    "e\n",
    "f\n",
    "g\n",
    "h\n",
    "i\n",
    "j\n",
    "k\n",
    "l\n",
    "m\n",
    "n\n",
    "o\n",
    "p\n",
    "q\n",
    "r\n",
    "s\n",
    "t\n",
    "u\n",
    "v\n",
    "w\n",
    "x\n",
    "y\n",
    "z\n",
    # numbers
    "0\n",
    "1\n",
    "2\n",
    "3\n",
    "4\n",
    "5\n",
    "6\n",
    "7\n",
    "8\n",
    "9\n",
]

replace_with_newline = [
    "\n",
    "\n\t",
]

punctuation_2_newline = [".", "!", "?"]

super_specific_edits = {
    ".\n.\n.\n": ", ",
    ".\n.\n.\n": ", ",
    " ." : ".",
    "\n\"" : "\"",
    "!\n?" : "!?",
    "?\n!" : "?!",
    "!\n!" : "!!",
    ".\"" : ".\"",
    "?\"" : "?\"",
    "!\"" : "!\"",
    "!\n\"" : "!\"",
    "?\n\"" : "?\"",
    ".\n'" : ".'",
    "?\n'" : "?'",
    "!\n'" : "!'",
    "\n''" : "''",
    "\n”" : "”",
    "\n“" : "“",
    "\n’" : "’",
    "\n‘" : "‘",
    ",  " : ", ",
    ":  " : ": ",
    ";  " : "; ",
    " ," : ",",
    " :" : ":",
    " ;" : ";",
    "\n.com": ".com\n",
    "\n.net": ".net\n",
    "\n.org": ".org\n",
    "\n.gov": ".gov\n",
    "\n.edu": ".edu\n",
    "\n.info": ".info\n",
    "\n.biz": ".biz\n",
    "\n.COM": ".COM\n",
    "\n.NET": ".NET\n",
    "\n.ORG": ".ORG\n",
    "\n.GOV": ".GOV\n",
    "\n.EDU": ".EDU\n",
    "\n.INFO": ".INFO\n",
    "\n.BIZ": ".BIZ\n",
}

from tqdm import tqdm
import os
from colorama import Fore
from PyPDF2 import PdfReader

class To_Sentences:
    prog_str = Fore.GREEN + "[+] " + Fore.RESET
    neg_str = Fore.RED + "[-] " + Fore.RESET

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def check_dir_path(self, dir_path):
        if os.name == "nt":
            if not dir_path.endswith("\\"):
                dir_path += "\\"
        else:
            if not dir_path.endswith("/"):
                dir_path += "/"
        return dir_path

    def pdf_to_sentences(self, infile, outfile):
        try:
            print(Fore.BLUE + f"Processing file: {infile}..." + Fore.RESET)
            pdfreader = PdfReader(infile)

            with open(outfile, "w", encoding="utf-8") as f:
                for page in pdfreader.pages:
                    text = page.extract_text()

                    # Clean up and format text
                    text = text.replace("\n", " ")

                    for r in replace_with_space:
                        text = text.replace(r, " ")

                    for r in replace_with_newline:
                        text = text.replace(r, "\n")

                    newtext = ""
                    for line in text.split("\n"):
                        for p in punctuation_2_newline:
                            if not line.endswith(p):
                                line = line.replace("\n", "")
                        newtext += line

                    for p in punctuation_2_newline:
                        newtext = newtext.replace(p, p + "\n")

                    for k, v in super_specific_edits.items():
                        newtext = newtext.replace(k, v)

                    f.write(newtext)

            print(Fore.GREEN + f"Saved to: {outfile}" + Fore.RESET)
        except Exception as e:
            print(self.neg_str + f"Failed to process file {infile}: {e}")

    def run_dir(self, input_dir, output_dir):
        input_dir = self.check_dir_path(input_dir)
        output_dir = self.check_dir_path(output_dir)

        if not os.path.exists(input_dir):
            raise IOError(f"Input directory does not exist: {input_dir}")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(self.prog_str + f"Created output directory: {output_dir}")

        files = [f for f in os.listdir(input_dir) if f.lower().endswith(".pdf")]
        num_files = len(files)

        if num_files == 0:
            print(self.neg_str + "No PDF files found in input directory.")
            return

         # Using tqdm to display progress and use tqdm.write for logging
        for i, file in enumerate(tqdm(files, desc="Processing files", unit="file", dynamic_ncols=True), start=1):
            infile = os.path.join(input_dir, file)
            outfile = os.path.join(output_dir, os.path.splitext(file)[0] + ".txt")
            
            # Update tqdm description with the file name (in blue)
            tqdm.write(f"{Fore.BLUE}Processing: {file}{Fore.RESET}")

            self.pdf_to_sentences(infile, outfile)

            # Log completed processing (in green)
            tqdm.write(f"{Fore.GREEN}Processed: {file}{Fore.RESET}")


def ocr_2_text_run(input_dir, output_dir):
    print(Fore.GREEN + "Processing OCR PDFs 2 Plain Text..." + Fore.RESET)
    processor = To_Sentences()
    processor.run_dir(input_dir, output_dir)



#if __name__ == "__main__":
#    input_dir = "data/pdfs_4_sentences"
#    output_dir = "data/data_4_sumz"
#    ocr_2_text_run(input_dir, output_dir)
