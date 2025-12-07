#!/usr/bin/env python3

import re
import argparse
from typing import Optional

from rich import print as rprint
from rich.console import Console
console = Console()
from loguru import logger
from rich.panel import Panel
from rich.prompt import Prompt


def flatten_tex_main_file(main_file_path: str, output_path: str = None) -> str:
    """
    Flattens a LaTeX main file by recursively replacing \input and \include
    commands with the actual file content.

    Args:
        main_file_path: Path to the main .tex file
        output_path: Optional output file path (if None, returns flattened content as string)

    Returns:
        Flattened LaTeX content as string if output_path is None, else writes to file
    """
    import os
    import re

    def process_file(file_path, processed_files):
        """Recursive helper to process files and track included files"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"LaTeX file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Track processed files to avoid circular includes
        processed_files.add(os.path.abspath(file_path))

        # Get directory for relative paths
        file_dir = os.path.dirname(os.path.abspath(file_path))

        # Patterns for \input and \include commands
        patterns = [
            r'\\input\s*\{([^}]+)\}',  # \input{file}
            r'\\include\s*\{([^}]+)\}',  # \include{file}
        ]

        def replace_include(match):
            # Extract filename from match
            include_file = match.group(1).strip()

            # Ensure .tex extension if not present
            if not include_file.endswith('.tex'):
                include_file += '.tex'

            # Resolve path relative to current file
            include_path = os.path.join(file_dir, include_file)
            include_path = os.path.normpath(include_path)

            # Avoid circular includes
            if os.path.abspath(include_path) in processed_files:
                return f"% Circular include avoided: {include_file}\n"

            try:
                # Recursively process included file
                included_content = process_file(include_path, processed_files)
                return f"% --- Start of {include_file} ---\n{included_content}\n% --- End of {include_file} ---\n"
            except FileNotFoundError:
                return f"% ERROR: Could not find included file: {include_file}\n"

        # Apply all patterns
        for pattern in patterns:
            content = re.sub(pattern, replace_include, content)

        return content

    # Process main file
    processed_files = set()
    flattened_content = process_file(main_file_path, processed_files)

    # Output result
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(flattened_content)
        return output_path
    else:
        return flattened_content

def add_endfloat_package(content):
    usepackage_pattern = re.compile(r'\\usepackage.*')
    endfloat_added = False
    new_content = []

    for line in content:
        if usepackage_pattern.match(line):
            if not endfloat_added:
                new_content.append(line)
                new_content.append('\\usepackage{endfloat}\n')
                endfloat_added = True
            else:
                new_content.append(line)
        else:
            new_content.append(line)

    if not endfloat_added:
        new_content.insert(0, '\\usepackage{endfloat}\n')

    return new_content

def add_endnotes_package(content):
    usepackage_pattern = re.compile(r'\\usepackage.*')
    endnotes_added = False
    new_content = []

    for line in content:
        if usepackage_pattern.match(line):
            if not endnotes_added:
                new_content.append(line)
                new_content.append('\\usepackage{endnotes}\n')
                endnotes_added = True
            else:
                new_content.append(line)
        else:
            new_content.append(line)

    if not endnotes_added:
        new_content.insert(0, '\\usepackage{endnotes}\n')

    return new_content

def transform_footnotes_to_endnotes(content):
    footnotes = []
    new_content = []
    footnote_pattern = re.compile(r'\\footnote{(.*?)}')

    for line in content:
        if footnote_pattern.search(line):
            footnotes.append(footnote_pattern.findall(line)[0])
            line = footnote_pattern.sub(r'\\endnote{\1}', line)
        new_content.append(line)

    new_content.append('\n\\theendnotes\n')
    return new_content

def remove_page_numbers_headers_footers(content):
    new_content = []
    page_number_pattern = re.compile(r'\\pagenumbering{.*?}')
    header_footer_pattern = re.compile(r'\\(lhead|chead|rhead|lfoot|cfoot|rfoot){.*?}')

    for line in content:
        line = page_number_pattern.sub('', line)
        line = header_footer_pattern.sub('', line)
        new_content.append(line)

    return new_content


def ask_single_question(question_number: int, question_text: str,
                        requires_warning: Optional[str] = None,
                        warning_style: str = "yellow") -> bool:
    """
    Ask a single formatting question and return the boolean answer.

    Args:
        question_number: The question number
        question_text: The question to ask
        requires_warning: Optional warning about requirements
        warning_style: Style for the warning text

    Returns:
        bool: True if user answered 'y', False if 'n'
    """

    console.print("\n")
    panel_content = f"[bold]{question_number}. {question_text}[/bold]"

    if requires_warning:
        panel_content += f"\n\n[italic {warning_style}]{requires_warning}[/italic {warning_style}]"

    console.print(Panel.fit(panel_content, border_style="blue"))

    answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
    return answer == "y"


def process_latex_document(input_file, output_file):
    logger.info(f"Reading input file: {input_file}")
    with open(input_file, 'r') as file:
        content = file.readlines()

    # Alternative: Ask questions one by one with immediate action
    def ask_and_process_sequentially() -> None:
        """
        Ask questions sequentially and process each one immediately.
        This allows you to call functions after each question.
        """

        console.print("\n")
        console.print(Panel.fit(
            "[bold cyan]📝 Sequential LaTeX Processing[/bold cyan]",
            border_style="cyan"
        ))

        # Initialize choices dictionary
        choices = {}

        # Question 1
        console.print(Panel.fit(
            "[bold]1. Line Spacing[/bold]\n"
            "Do you want all your text to be formatted with double space between lines (except the references)?",
            border_style="blue"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["double_space"] = answer == "y"

        # Question 2
        console.print("\n")
        console.print(Panel.fit(
            "[bold]2. Footnotes to Endnotes[/bold]\n"
            "Do you want all footnotes at the end of the document as endnotes, after references in a separate section?",
            border_style="blue"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["endnotes"] = answer == "y"

        # Question 3
        console.print("\n")
        console.print(Panel.fit(
            "[bold]3. Figures Placement[/bold]\n"
            "Do you want all figures at the end of the document, after the references in a separate section?",
            border_style="blue"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["figures_end"] = answer == "y"

        # Question 4
        console.print("\n")
        console.print(Panel.fit(
            "[bold]4. Separate Figures Document[/bold]\n"
            "Do you want all figures in a separate document that includes only your figures?",
            border_style="blue"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["figures_separate"] = answer == "y"

        # Question 5
        console.print("\n")
        console.print(Panel.fit(
            "[bold]5. Figures Zip Archive[/bold]\n"
            "Do you want all figures in a zip file that includes all your figures?",
            border_style="blue"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["figures_zip"] = answer == "y"

        # Question 6
        console.print("\n")
        console.print(Panel.fit(
            "[bold]6. Tables Placement[/bold]\n"
            "Do you want all tables at the end of the document, after the references in a separate section?",
            border_style="blue"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["tables_end"] = answer == "y"

        # Question 7
        console.print("\n")
        console.print(Panel.fit(
            "[bold]7. Tables Zip Archive[/bold]\n"
            "Do you want all tables in a zip file that includes all your tables in pdf format?",
            border_style="blue"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["tables_zip"] = answer == "y"

        # Question 8
        console.print("\n")
        console.print(Panel.fit(
            "[bold]8. Remove Headers/Footers[/bold]\n"
            "Do you want to remove all headers, footers and page numbers (it helps for converting to the MS Word format)?",
            border_style="blue"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["remove_headers"] = answer == "y"

        # Question 9
        console.print("\n")
        console.print(Panel.fit(
            "[bold]9. Flatten LaTeX Files[/bold]\n"
            "Do you want to 'flatten' your LaTeX source files by including all the \\input and \\include files into the main-file.tex root file?",
            border_style="yellow"
        ))
        console.print("[italic yellow]Note: Requires https://pypi.org/project/latex-flatten/[/italic yellow]")
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["flatten_latex"] = answer == "y"

        # Question 10
        console.print("\n")
        console.print(Panel.fit(
            "[bold]10. Remove Comments[/bold]\n"
            "Do you want to remove all the % commented lines?",
            border_style="yellow"
        ))
        console.print("[italic yellow]Note: Requires arxiv-latex-cleaner[/italic yellow]")
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["remove_comments"] = answer == "y"

        # Question 11
        console.print("\n")
        console.print(Panel.fit(
            "[bold]11. Convert to Microsoft Word[/bold]\n"
            "Do you want to convert to the proprietary, expensive and non-interoperable Microsoft Word format?",
            border_style="red"
        ))
        answer = Prompt.ask("Your choice", choices=["y", "n", "Y", "N"], default="n").lower()
        choices["convert_to_word"] = answer == "y"

        # Display summary
        console.print("\n" + "=" * 60)
        console.print("[bold green]📋 Formatting Options Summary[/bold green]\n")
    ask_and_process_sequentially()

    #logger.info("Adding endfloat package")
    #content = add_endfloat_package(content)

    #logger.info("Adding endnotes package")
    #content = add_endnotes_package(content)

    #logger.info("Transforming footnotes to endnotes")
    #content = transform_footnotes_to_endnotes(content)

    #logger.info("Removing page numbers, headers, and footers")
    #content = remove_page_numbers_headers_footers(content)

    logger.info(f"Writing output file: {output_file}")
    with open(output_file, 'w') as file:
        file.writelines(content)

    rprint(f"[green]Processing complete. Output written to {output_file}[/green]")

if __name__ == "__main__":
    logger.add("process_latex.log", rotation="500 MB")  # Automatically rotate too big file

    parser = argparse.ArgumentParser(description="Process a LaTeX document.")
    parser.add_argument("-i", "--input", required=True, help="Input LaTeX file")
    parser.add_argument("-o", "--output", default="output.tex", help="Output LaTeX file (default: output.tex)")

    args = parser.parse_args()

    rprint("[bold]Starting LaTeX document processing...[/bold]")
    process_latex_document(args.input, args.output)
    rprint("[bold]Processing finished.[/bold]")
