#!/usr/bin/env python3
"""Converts index.md (digital CV) into a LaTeX document."""

import re
import sys
from pathlib import Path


def escape_latex(text: str) -> str:
    """Escape special LaTeX characters."""
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
        ('ã', r'\~{a}'),
        ('Ã', r'\~{A}'),
        ('ç', r'\c{c}'),
        ('Ç', r'\c{C}'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def parse_contact_line(lines: list[str]) -> dict:
    """Parse the plain-text contact lines (line 5 and 6 of the new format)."""
    contacts = {}
    # Line like: Porto, Portugal | +351 916 752 957 | diogosoares@drsoares.me
    # Line like: [github.com/drsoares](url) | [linkedin.com/in/drcsoares](url)
    for line in lines:
        parts = [p.strip() for p in line.split('|')]
        for part in parts:
            link_match = re.match(r'\[(.+?)\]\((.+?)\)', part)
            if link_match:
                text, url = link_match.group(1), link_match.group(2)
                if 'github' in text.lower():
                    contacts['github'] = (text, url)
                elif 'linkedin' in text.lower():
                    contacts['linkedin'] = (text, url)
            elif '@' in part and 'mailto' not in part:
                contacts['email'] = part
            elif re.search(r'\+?\d[\d\s]{6,}', part):
                contacts['phone'] = part
            elif part and not link_match:
                contacts['location'] = part
    return contacts


def parse_experience_entry(block: str) -> dict | None:
    """Parse a single experience block: Company — *Role* `dates` + body."""
    header_match = re.match(
        r'(.+?)\s*—\s*\*(.+?)\*\s*`(.+?)`', block.strip()
    )
    if not header_match:
        return None
    company = header_match.group(1).strip()
    role = header_match.group(2).strip()
    dates = header_match.group(3).strip()
    rest = block[header_match.end():].strip()

    tech_match = re.search(r'\*\*Technologies?:\*\*\s*(.+)', rest)
    technologies = tech_match.group(1).strip().rstrip('.') if tech_match else ""
    description = rest[:tech_match.start()].strip() if tech_match else rest

    return {
        "company": company,
        "dates": dates,
        "role": role,
        "description": description,
        "technologies": technologies,
    }


def parse_course(line: str) -> dict | None:
    """Parse a course line like: - [Name](url) — Provider."""
    line = line.strip().lstrip('- ')
    m = re.match(r'\[(.+?)\]\((.+?)\)\s*—\s*(.+)', line)
    if not m:
        return None
    return {"name": m.group(1), "url": m.group(2), "provider": m.group(3).strip()}


def build_latex(md_path: Path) -> str:
    content = md_path.read_text()
    lines = content.split('\n')

    # --- Name ---
    name = lines[0].lstrip('# ').strip()

    # --- Contact info (lines before first ---) ---
    contact_lines = []
    for i in range(1, len(lines)):
        if lines[i].strip() == '---':
            break
        stripped = lines[i].strip()
        if stripped and not stripped.startswith('**'):
            contact_lines.append(stripped)

    contacts = parse_contact_line(contact_lines)

    # --- Sections ---
    section_splits = re.split(r'^## ', content, flags=re.MULTILINE)

    profile = ""
    education_section = {}
    experience_entries = []
    courses = []

    for section in section_splits:
        if section.startswith("Profile"):
            profile_lines = section.split('\n')[1:]
            profile = ' '.join(l.strip() for l in profile_lines if l.strip() and l.strip() != '---')

        elif section.startswith("Education"):
            edu_entries = re.split(r'^### ', section, flags=re.MULTILINE)[1:]
            if edu_entries:
                entry = edu_entries[0]
                edu_match = re.match(r'(.+?)\s*`(.+?)`', entry.strip())
                if edu_match:
                    rest_lines = entry[edu_match.end():].strip().split('\n')
                    degree = next((l.strip() for l in rest_lines if l.strip()), "")
                    education_section = {
                        "institution": edu_match.group(1).strip(),
                        "dates": edu_match.group(2).strip(),
                        "degree": degree,
                    }

        elif section.startswith("Experience"):
            entries = re.split(r'^### ', section, flags=re.MULTILINE)[1:]
            for entry in entries:
                parsed = parse_experience_entry(entry)
                if parsed:
                    experience_entries.append(parsed)

        elif section.startswith("Certifications") or section.startswith("Courses"):
            course_lines = [l for l in section.split('\n') if l.strip().startswith('- ')]
            for cl in course_lines:
                parsed = parse_course(cl)
                if parsed:
                    courses.append(parsed)

    # --- Build LaTeX ---
    e = escape_latex

    contact_items = []
    if 'email' in contacts:
        email = contacts['email']
        contact_items.append(rf'\href{{mailto:{email}}}{{{e(email)}}}')
    if 'phone' in contacts:
        contact_items.append(e(contacts['phone']))
    if 'location' in contacts:
        contact_items.append(e(contacts['location']))
    if 'linkedin' in contacts:
        text, url = contacts['linkedin']
        contact_items.append(rf'\href{{{url}}}{{{e(text)}}}')
    if 'github' in contacts:
        text, url = contacts['github']
        contact_items.append(rf'\href{{{url}}}{{{e(text)}}}')

    contact_line = " \\quad|\\quad ".join(contact_items)

    exp_latex = ""
    for entry in experience_entries:
        exp_latex += rf"""
\subsection*{{{e(entry['company'])} \hfill \normalfont\textit{{{e(entry['dates'])}}}}}
\textit{{{e(entry['role'])}}}\\[4pt]
{e(entry['description'])}"""
        if entry["technologies"]:
            exp_latex += rf"""
\\[4pt]\textbf{{Technologies:}} {e(entry['technologies'])}"""
        exp_latex += "\n\\vspace{8pt}\n"

    courses_latex = ""
    for course in courses:
        courses_latex += rf"""  \item \href{{{course['url']}}}{{{e(course['name'])}}} — {e(course['provider'])}
"""

    edu_latex = ""
    if education_section:
        edu_latex = rf"""\subsection*{{{e(education_section['institution'])} \hfill \normalfont\textit{{{e(education_section['dates'])}}}}}
{e(education_section['degree'])}"""

    latex = rf"""\documentclass[11pt,a4paper]{{article}}

\usepackage[margin=1.8cm]{{geometry}}
\usepackage{{titlesec}}
\usepackage{{enumitem}}
\usepackage{{hyperref}}
\usepackage{{xcolor}}
\usepackage{{parskip}}

% Colors
\definecolor{{linkcolor}}{{HTML}}{{0563C1}}
\definecolor{{headingcolor}}{{HTML}}{{2E3A4F}}

% Hyperlinks
\hypersetup{{
  colorlinks=true,
  urlcolor=linkcolor,
  linkcolor=linkcolor,
}}

% Section formatting
\titleformat{{\section}}{{\Large\bfseries\color{{headingcolor}}}}{{}}{{0em}}{{}}[\titlerule]
\titlespacing{{\section}}{{0pt}}{{12pt}}{{6pt}}

\titleformat{{\subsection}}[runin]{{\bfseries}}{{}}{{0em}}{{}}
\titlespacing{{\subsection}}{{0pt}}{{6pt}}{{4pt}}

\setlist[itemize]{{leftmargin=1.5em, itemsep=2pt, parsep=0pt}}

\begin{{document}}

%% ---- Header ----
\begin{{center}}
  {{\LARGE\bfseries {e(name)}}}\\[6pt]
  {contact_line}
\end{{center}}

\vspace{{4pt}}

%% ---- Profile ----
{e(profile)}

%% ---- Education ----
\section*{{Education}}
{edu_latex}

%% ---- Experience ----
\section*{{Experience}}
{exp_latex}

%% ---- Certifications & Courses ----
\section*{{Certifications \& Courses}}
\begin{{itemize}}
{courses_latex}\end{{itemize}}

\end{{document}}
"""
    return latex


def main():
    md_path = Path(__file__).parent / "index.md"
    if not md_path.exists():
        print(f"Error: {md_path} not found", file=sys.stderr)
        sys.exit(1)

    output_path = Path(__file__).parent / "cv.tex"
    latex = build_latex(md_path)
    output_path.write_text(latex)
    print(f"LaTeX CV written to {output_path}")


if __name__ == "__main__":
    main()
