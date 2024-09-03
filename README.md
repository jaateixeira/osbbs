# OSBBS - One Steep Back Before Submitting ... your paper to a publisher 

The **osbbs** script automates some of the common old-school requests commonly asked by editorial offices that do not make much sense for LaTeX submissions but can be easily automated and done in seconds (e.g., put footnotes at the end, and all figures in separate files). A simple step back before submitting your article to a journal that does not welcome good-looking, latex-produced,  publication-ready submissions.

# Table of Contents

1. [Problem Statement](#problem-statement)
2. [Vision](#vision)
3. [OSBBS inputs](#osbbs-input)
4. [OSBBS outputs](#osbbs-outputs)
5  [What OSBBS does](#osbbs-outputs)
6 [What OSBBS does](#osbbs-outputs)
7 [Installation](#installation)
   - [Prerequisites](#prerequisites)
   - [Setup](#setup)
8. [Usage](#usage)
   - [Running the Application](#running-the-application)
   - [Configuration](#configuration)
9. [Contributing](#contributing)
   - [Code of Conduct](#code-of-conduct)
   - [Pull Requests](#pull-requests)
10. [License](#license)
11. [Contact](#contact)
12. [Acknowledgments](#acknowledgments)


# Problem statement
Researchers produce original articles in Latex that are formatted in a publication-ready quality in pdf,  to be asked then by some editorial office to do some things that only eases the job of the publisher's typesetter after work is accepted : 
* Put all footnotes in the end.
* Put all figures in the end or submit them separately.  
* Put all tables in the end or submit them separately.
* Format everything in with double space between lines. 
* Submit the work in the proprietary, expensive and non-interoperable. Microsoft Word format.  
  
Then after the reviewer is satisfied and the article is accepted, publishers will often send the MS Word file to an offshore location (usually India),
where they will typeset (i.e., create a PDF that is to be printed or distributed online) and produce a final document 
that can be even worst that the original articles formatted in Latex by the original author.  Worst than that, the researcher often needs to pay article processing fees, and extra fees for including colour figures and is given just a few days to approve the final typesetting version. 

It looks like we are before the pre-Internet production times and articles are delivered to university libraries in paper !!  Just journal subscriptions are way more expensive !! 

This is a highly inefficient way of work. While ACM, IEEE and other academic associations receive and publish directly the work by researchers, other traditional publishers in general, 
or specific journals in particular force authors to submit their work in MS Word. While I agree that most researchers in social sciences do not want to learn Latex, PdfLatex, Overleaf or anything new other than the proprietary, expensive and non-interoperable Microsoft Word office suite, the others should not be forced to use MS Word. In my view, MS Word is a really bad format for articles that are complex with a lot of tables, high-resolution figures, math, equations,  a lot of references, lot of footnotes that are co-written by multiple scholars at the same time. 

Publishers know that and in the last years they started providing latex classes and author guides for their journals. But even if you submit work based on the publisher's latex packages provided by the publisher, many  editorial offices will demand the old way (submit an MS word file with figures and tables in the end, footnotes in the end, not coloured figures, etc.) 

We can not change the world, but with obsbbs, we can automate some of the common old-school requests (e.g., put footnotes at the end, and all figures in separate files) in osbbs. A simple 
step back before submitting your article to a journal that does not welcome good-looking, latex-produced, publication-ready submissions. 

Don't get mad with academia, the publisher, the journal, or the editorial office, just run **osbbs** against your latex main file (e.g., main.tex) and **osbbs** will help you address many of the common requests by the editorial offices that love the MS WORD format.  Note you can always prioritize journals under the umbrella of Academic Associations (e.g., Cambridge University Press, AoM ) or Professional Organizations (e.g., IEEE, ACM) over the big corporation publishers to disseminate your research. Consider also the open-access options and the price of the article processing fees. Note some Academic Associations and Professional Organizations might work in the same way as traditional publishers work today in the future. 

# Vision

A world where researchers use Latex instead of Word, even if the dinosaurs keep requesting "We want MS Word", "We want MS Word" without saying  "I don't know anything else"  

# Intended audience / Targeted users 

Researches proficient with Tex&/LaTex, can open a terminal and type in the command line, but still wants to deal with publishers that ask them to submit their journal in awkward and old-fashioned formats.  

# OSBBS inputs 

**osbbs** will receive a main TeX/LaTex file (e.g., main.tex) as input. 

# OSBBS outputs 
- **osbbs**  produces a TeX/LaTex file that is named osbbs.(main-file).tex. After running **osbbs**, run Latex/PdfLaTex once on the output file and you should be ready to submit.
- **osbbs** also produces a configuration file osbbs.config.tex file that is included in the final osbbs.(main-file).tex output file. That configuration file can be changed according to your needs - after all, you might be resubmitting the document somewhere else. 

# What OSBBS does? 

It will interactively ask: 

* Do you want all your text to be formatted with double space between lines (except the references?). 
* Do you want all footnotes at the end of the document as endnotes, after refrences in a separate section? 
* Do you want all figures at the end of the document, after the references in a separate section? 
* Do you want all figures in a separate document that includes only your figures?
* Do you want all figures in a zip file that includes all your figures? 
* Do you want all tables at the end of the document, after the references in a separate section?
* Do you want all tables in a zip file that includes all your tables in pdf format? 
* Do you want to remove all headers, footers and page numbers (it helps for converting to the MS Word format)? 
* Do you want to convert to the proprietary, expensive and non-interoperable? Microsoft Word format?
* To convert to MS Word, do you want to use (1):
** Pandoc?
** Mathpix?
** An online "free" converter and hope for the best?
** Import the pdf directly on MS Word and hope for the best? 

**osbbs**  then creates a new version of you LaTex main file with the  osbbs prefix (e.g., osbbs.main.tex) according your answers. 
**osbbs**  will attempt convert to MS Word using Pandoc (free), MathPix (paid)  directly, or offer tips on how to deal with other ways of converting PDF documents
created with LaTex to the proprietary, expensive and non-interoperable? Microsoft Word format?


# How OSBBS works?

**osbbs**  changes the input LaTeX documnent (e.g., main.tex) by loading certaing packages (e.g., endnotes, endfloat, collections) and adding realted commands to perform the actions requested by the user. 

## To move Figures and Tables to the end 

The **endfloat** package in LaTeX [https://ctan.org/pkg/endfloat](https://ctan.org/pkg/endfloat) is used to move all figures and tables to the end of a document. By including the package in the preamble of your LaTeX document with `\usepackage{endfloat}`, the package will automatically repositions all figures and tables to the end of the document, while leaving markers (aka placeholders) in the text where they were originally placed. Additionally, it generates lists of figures and tables at the end, making it easier to reference them.  **osbbs** uses **endfloat** for simplicity. Howwever, note that the **collections** [https://ctan.org/pkg/collect?lang=en](https://ctan.org/pkg/collect) can also be used. Please cosider it for complex documents with multiple types of floats.

# To transform footnotes into endnotes 
The **endnotes** package in LaTeX [https://ctan.org/pkg/endnotes](https://ctan.org/pkg/endnotes) is used transform all footnotes that appear as we read the documento into endnotes at the end of the document.

# To remove page numbers 
- **osbbs** removes page numbers by removing all `\pagenumbering{...}` and `\thispagestyle{...}` commands in the document (e.g., main.tex) and adding then `\pagestyle{empty}` to the preamble.

# To remove footers and headers 
- **osbbs** removes footers and headers by removing all commands like `\fancyhead[...]{...}`, `\fancyfoot[...]{...}`, `\lhead{...}`, `\chead{...}`, `\rhead{...}`, `\lfoot{...}`, \cfoot`{...}`, and `\rfoot{...}` that customize fancy headers and footers. Then it adds the following comments to the code before and after `\begin{document}`

```latex
% added by the osbbs script
% to check if the `fancyhdr` package is already loaded

 \makeatletter
   \@ifpackageloaded{fancyhdr}{}{
     \usepackage{fancyhdr}
   }
   \makeatother


% added by the osbbs script
% to set the header and footer to be empty
\fancyhf{} % Clear all header and footer fields

% added by the osbbs script
% to apply the fancy page style
\pagestyle{fancy}

\begin{document}

% added by the osbbs script
% to ensure the first page also has no header or footer
% you might want to move this command somewhere else if you wish to keep fancy header or footer in the first page of the document
\thispagestyle{fancy}

```
Please note removing page numbers, footers, headers can improve the quality of translatation from the LaTeX word to the MS WORD doc or docx format.

**osbbs** lets you know when something was added or removed from the document (e.g., main.tex) by using comments (e.g., `% added by the osbbs script`  or  `% commented by the ossbs script`). It also adds `% The latex document was minimally processed by the ossbs script (see https://github.com/jaateixeira/osbbs/).` to guide future readers of the modified LaTeX code.

# Installation 

# Usage 

# Contributors guide

## Planned features 

### Easy hacks 

- Integrate with the Google Docs API to create a Google Docs document that can then be exported by the users to MS word 
- Integrate with several PDF 2 MS word APIs available in the market such as Adobe PDF Services API and Zamzar and ConvertAPI 

