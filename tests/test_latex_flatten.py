

"""
# From the project root directory
python3 -m unittest discover tests/


"""

import unittest
import os
import tempfile
import shutil
from pathlib import Path

from osbbs import flatten_tex_main_file


class TestLatexFlatten(unittest.TestCase):
    """Test flatten_tex_main_file function"""

    def setUp(self):
        """Create temporary directory with test LaTeX files"""
        self.test_dir = tempfile.mkdtemp(prefix="latex_flatten_test_")

        # Create main.tex with one include and one input
        self.main_tex = os.path.join(self.test_dir, "main.tex")
        with open(self.main_tex, 'w') as f:
            f.write(r"""\documentclass{article}
\begin{document}
\section{Main Content}
This is the main file.

% Include a chapter
\include{chapter1}

% Input some definitions
\input{definitions}

Back to main content.
\end{document}""")

        # Create chapter1.tex
        self.chapter_tex = os.path.join(self.test_dir, "chapter1.tex")
        with open(self.chapter_tex, 'w') as f:
            f.write(r"""\chapter{First Chapter}
This is an included chapter.
With multiple lines.
""")

        # Create definitions.tex
        self.defs_tex = os.path.join(self.test_dir, "definitions.tex")
        with open(self.defs_tex, 'w') as f:
            f.write(r"""\section{Definitions}
\begin{itemize}
\item Definition 1
\item Definition 2
\end{itemize}
""")

        # Create output file path
        self.output_file = os.path.join(self.test_dir, "output.tex")

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_flatten_basic_include_input(self):
        """Test flattening with one include and one input"""
        # Call the function
        result = flatten_tex_main_file(self.main_tex, self.output_file)

        # Verify output file was created
        self.assertTrue(os.path.exists(self.output_file))

        # Read the output
        with open(self.output_file, 'r') as f:
            output_content = f.read()

        # Verify all expected content is present
        self.assertIn(r"\documentclass{article}", output_content)
        self.assertIn("This is the main file.", output_content)
        self.assertIn("This is an included chapter.", output_content)
        self.assertIn("Definition 1", output_content)
        self.assertIn("Back to main content.", output_content)

        # Verify commands were replaced (check for markers or absence of commands)
        self.assertNotIn(r"\include{chapter1}", output_content)
        self.assertNotIn(r"\input{definitions}", output_content)

        # Check that included content markers are present (if your implementation adds them)
        # Remove or modify this based on your actual implementation
        self.assertIn("--- Start of chapter1.tex ---", output_content)
        self.assertIn("--- Start of definitions.tex ---", output_content)

    def test_flatten_returns_string(self):
        """Test that function returns string when no output_path provided"""
        result = flatten_tex_main_file(self.main_tex)

        self.assertIsInstance(result, str)
        self.assertIn("This is the main file.", result)
        self.assertIn("This is an included chapter.", result)
        self.assertIn("Definition 1", result)

    def test_missing_included_file(self):
        """Test behavior when included file is missing"""
        # Remove one included file
        os.remove(self.defs_tex)

        # Should still work but handle missing file gracefully
        result = flatten_tex_main_file(self.main_tex, self.output_file)

        with open(self.output_file, 'r') as f:
            output_content = f.read()

        # Should contain error message or skip the missing file
        # Adjust assertion based on your implementation
        self.assertIn("definitions", output_content.lower())

    def test_circular_inclusion(self):
        """Test circular inclusion handling"""
        # Create circular reference
        with open(self.chapter_tex, 'a') as f:
            f.write(r"\input{main}")

        # Should handle without infinite recursion
        result = flatten_tex_main_file(self.main_tex, self.output_file)

        with open(self.output_file, 'r') as f:
            output_content = f.read()

        # Should complete and produce output
        self.assertIn("This is the main file.", output_content)
        self.assertIn("This is an included chapter.", output_content)


if __name__ == '__main__':
    unittest.main()