## Prompts & Subject Notes

### Prompts
```md
Accordingly update `#file:README.md` and write as a student would for their own understanding and viva prep. Ensure a critical understanding of the lab topics. For each question, divide content into the following sections:
1. Problem statement
2. Concept understanding
3. Code understanding/explanation
4. Viva prep
```

### Useful Commands:

1. Pandoc CLI: `pandoc <source> -o <dest> --pdf-engine=xelatex`
2. Java commands: 

```java
// compile - creates class file
javac -d bin <file.java>
// executable
java -cp bin <file>
```

**Front-Matter:**
```yaml
---
geometry: margin=0.75in
mainfont: Arial
monofont: JetBrains Mono
highlight-style: tango
header-includes:
  - \usepackage{xcolor}
  - \usepackage{mdframed}
  - \usepackage{fvextra}
  - \definecolor{codebg}{RGB}{245,245,245}
  - \definecolor{inlinebg}{RGB}{240,240,240}
  - \definecolor{inlinefg}{RGB}{200,50,50}
  - \fvset{breaklines=true, breakanywhere=true, fontsize=\small}
  - \let\oldtexttt\texttt
  - \renewcommand{\texttt}[1]{\colorbox{inlinebg}{\oldtexttt{\textcolor{inlinefg}{#1}}}}
  - \BeforeBeginEnvironment{Highlighting}{\begin{mdframed}[backgroundcolor=codebg,linewidth=0pt,innerleftmargin=8pt,innerrightmargin=8pt,innertopmargin=8pt,innerbottommargin=8pt]}
  - \AfterEndEnvironment{Highlighting}{\end{mdframed}}
  - \setlength{\parskip}{0.5em}
---
```

### Subject Notes (Future Use)
- #### Topic Overview
	- Key definitions
	- Core concepts
	- Common pitfalls
- #### Worked Examples
	- Problem setup
	- Step-by-step solution
	- Checks/validation
- #### Lab/Lecture Summaries
	- Objectives
	- Methods/tools used
	- Observations & learnings
- #### Revision/Viva Prep
	- Expected questions
	- Short answers
	- Quick formulas/snippets