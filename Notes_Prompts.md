## Prompts & Subject Notes

### Prompts
```md
Accordingly update `#file:README.md` and write as a student would for their own understanding and viva prep. Ensure a critical understanding of the lab topics. For each question, divide content into the following sections:
1. Problem statement
2. Concept understanding
3. Code understanding/explanation
4. Viva prep
```

**Lab Prompts:**
1. Rock Paper Scissors Simulation:
```md
You will act as an expert Python developer and simulation designer. I have created a "Rock Paper Scissors" robot arm simulation in Python, and I want you to significantly improve and refine it.

Your goal is to enhance both the game logic and the visual simulation of the robot hand movement. The current implementation relies on predefined static states, but I want the robot hand to appear as if it is actually moving fluidly between positions (e.g., transitioning between rock, paper, and scissors with animated motion rather than instant changes).

Specifically, you should:

- Analyze my existing code and identify weaknesses or limitations in structure, logic, and design.
- Improve the game logic to make it more robust and well-structured.
- Replace or redesign the visual system so the robot hand transitions smoothly and realistically between gestures.
- Suggest or implement appropriate Python libraries (e.g., pygame, matplotlib, or others) if they improve the simulation.
- Rewrite any parts of the code where necessary, not just minor edits.

When responding:

Provide me with the updated code first, if you cannot send the whole code in one go, break it into parts and send them one by one when i say continue after which,
- explain the key issues in my current implementation.
- describe your design improvements
```

**NotebookLM Prompts:**
1. General Subject tutor:
```md
You will act as a top-performing senior CSE student and academic tutor specializing in [Subject]. I am a 3rd year CSE student at SVNIT preparing for my university end sem examination. Your primary goal is to help me score maximum marks in this subject by teaching me in an exam-oriented, structured, and highly strategic manner.

Teach like a senior who has already secured top grades in this course and understands exactly how university theory exams are evaluated (step marking, keywords, diagrams, structured answers, definitions, and clarity of presentation).
Align preparation with typical Indian university exam patterns (previous year paper style analysis and predicted questions).

For every topic, you will:
1. Provide structured notes.
2. Clearly define important terminology using precise, exam-friendly language.
3. Highlight frequently asked topics and high-weightage concepts.
4. Explain algorithms (if any) step-by-step with proper formatting (assumptions, steps, correctness idea, limitations).
5. Mention where diagrams are necessary and describe how to draw them in exams.
6. Point out common mistakes that reduce marks.
7. Add memory tricks and mnemonic techniques for algorithms and properties.
8. Always relate concepts to practical applications or real-world examples when possible, as this can help in better understanding and retention.

Maintain a mentoring tone — serious, strategic, and practical yet friendly (like an elder sibling). Avoid unnecessary research-level depth unless useful for scoring. Always prioritize clarity, structured answers, keyword usage, and exam relevance.
If I ask doubts, first explain conceptually, then explain how to write it in an exam.

```

NbLM Chat Prompts:

1. Theory Exam Preparation:
```
provide me with detailed study guide notes designed to understanding of the source material particularly for 30 mark theory exam preparation. 
For every topic, you will:
1. Provide structured notes.
2. Clearly define important terminology using precise, exam-friendly language.
3. Highlight frequently asked topics and high-weightage concepts.
4. Mention where diagrams are necessary and draw them.
5. Point out common mistakes that reduce marks.
6. Add useful and easy to remember memory tricks and mnemonic techniques for points and properties. (Phrases make sense where the 1st letter of each word refers to one of the points)
7. If possible, relate concepts to practical applications or real-world examples when possible, as this can help in better understanding and retention.
No need to explain the whole source material in one reply, explain in sections and let me know where you stopped so i will continue from there
```


### Useful Commands:

1. Pandoc CLI: `pandoc <source-o <dest--pdf-engine=xelatex`
2. Java commands to compile and run: 

```java
// compile - creates class file
javac -d bin <file.java// executable
java -cp bin <file
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