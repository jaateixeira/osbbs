# OSBBS - One Steep Back Before Submitting ... your paper to a publisher 

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
safd s
