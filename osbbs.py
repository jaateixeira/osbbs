import re
import sys
import subprocess
from pathlib import Path

def modify_latex_file(input_file):
    with open(input_file, 'r') as file:
        content = file.read()

    # Add necessary packages and setup
    preamble_additions = r"""
    % Packages for handling collections and endnotes
    \usepackage{etoolbox}
    \usepackage{collect}
    \usepackage{endnotes}
    \renewcommand{\footnote}{\endnote}

    % Define collections for figures
    \definecollection{allfigures}

    % Collect figures into the defined collection
    \AtBeginEnvironment{figure}{\addtocounter{figure}{-1}\begin{collect}{allfigures}}
    \AtEndEnvironment{figure}{\end{collect}}

    % Clear headers and footers, and remove page numbers
    \usepackage{fancyhdr}
    \usepackage{nopageno}
    \fancypagestyle{plain}{
      \fancyhf{} % Clear all header and footer fields
      \renewcommand{\headrulewidth}{0pt} % Remove the header rule
      \renewcommand{\footrulewidth}{0pt} % Remove the footer rule
    }
    \pagestyle{plain}
    """

    end_document_addition = r"""
    \AtEndDocument{
        \clearpage
        \section*{Figures}
        \printcollection{allfigures}
        \clearpage
        \section*{Endnotes}
        \theendnotes
    }
    """

    # Insert the preamble additions after \documentclass
    content = re.sub(r'(\\documentclass\[.*?\]{WileyNJDv5})', r'\1' + preamble_additions, content, 1)

    # Insert the end document additions before \end{document}
    content = re.sub(r'(\\end{document})', end_document_addition + r'\1', content, 1)

    # Write the modified content to a new file
    output_tex_file = input_file.replace('.tex', '_modified.tex')
    with open(output_tex_file, 'w') as file:
        file.write(content)

    return output_tex_file

def convert_to_word(tex_file):
    docx_file = tex_file.replace('.tex', '.docx')
    subprocess.run(['pandoc', tex_file, '-o', docx_file])
    return docx_file

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file.tex>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_tex_file = modify_latex_file(input_file)
    output_docx_file = convert_to_word(output_tex_file)
    print(f"Converted {input_file} to {output_docx_file}")

