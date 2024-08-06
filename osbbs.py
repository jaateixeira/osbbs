#!/usr/bin/env python3

import re
import argparse
from rich import print as rprint
from loguru import logger

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

def process_latex_document(input_file, output_file):
    logger.info(f"Reading input file: {input_file}")
    with open(input_file, 'r') as file:
        content = file.readlines()

    logger.info("Adding endfloat package")
    content = add_endfloat_package(content)

    logger.info("Adding endnotes package")
    content = add_endnotes_package(content)

    logger.info("Transforming footnotes to endnotes")
    content = transform_footnotes_to_endnotes(content)

    logger.info("Removing page numbers, headers, and footers")
    content = remove_page_numbers_headers_footers(content)

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

