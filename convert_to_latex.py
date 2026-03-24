#!/usr/bin/env python3
"""Converts index.md (digital CV) into a LaTeX document."""

import re
import sys
from pathlib import Path


def parse_contact_table(html: str) -> dict[str, str]:
    """Extract contact fields from the HTML table."""
    contacts = {}
    rows = re.findall(r"<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>\s*</tr>", html, re.DOTALL)
    for label, value in rows:
        label = label.strip()
        # Strip anchor tags, keep text
        link_match = re.search(r'<a\s+href="([^"]+)"[^>]*>([^<]+)</a>', value)
        if link_match:
            contacts[label] = (link_match.group(2).strip(), link_match.group(1).strip())
        else:
            contacts[label] = (value.strip(), None)
    return contacts


def parse_experience_entry(block: str) -> dict:
    """Parse a single experience block (### header + body)."""
    header_match = re.match(
        r'\*\*(.+?)\*\*\s*`(.+?)`', block.strip()
    )
    if not header_match:
        return None
    company = header_match.group(1)
    dates = header_match.group(2)
    rest = block[header_match.end():].strip()

    role_match = re.search(r'_(.+?)_', rest)
    role = role_match.group(1) if role_match else ""

    # Description lines after <br> and before Technologies:
    desc_part = re.sub(r'_.*?_\s*(<br>|<br/>)?\s*', '', rest).strip()
    tech_match = re.search(r'Technologies?:\s*(.+)', desc_part)
    technologies = tech_match.group(1).strip().rstrip('.') if tech_match else ""
    description = desc_part[:tech_match.start()].strip() if tech_match else desc_part

    return {
        "company": company,
        "dates": dates,
        "role": role,
        "description": description,
        "technologies": technologies,
    }


def parse_course(line: str) -> dict | None:
    """Parse a course line like ### [**Name**](url)."""
    m = re.match(r'\[?\*\*(.+?)\*\*\]?\(?([^)]*)\)?', line.strip())
    if not m:
        return None
    return {"name": m.group(1), "url": m.group(2)}


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
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def build_latex(md_path: Path) -> str:
    content = md_path.read_text()
    lines = content.split('\n')

    # --- Name ---
    name = lines[0].lstrip('# ').strip()

    # --- Summary ---
    summary_lines = []
    i = 1
    while i < len(lines) and not lines[i].strip().startswith('<table'):
        if lines[i].strip():
            summary_lines.append(lines[i].strip())
        i += 1

    summary = ' '.join(summary_lines)

    # --- Contacts ---
    table_block = content[content.index('<table'):content.index('</table>') + len('</table>')]
    contacts = parse_contact_table(table_block)

    # --- Sections ---
    # Split by ## headers
    section_splits = re.split(r'^## ', content, flags=re.MULTILINE)

    education_section = ""
    experience_entries = []
    courses = []

    for section in section_splits:
        if section.startswith("Education"):
            edu_match = re.search(r'\*\*(.+?)\*\*\s*`(.+?)`', section)
            edu_desc_lines = section.split('\n')
            edu_degree = ""
            for el in edu_desc_lines:
                el = el.strip()
                if el and not el.startswith('#') and not el.startswith('Education') and '**' not in el and '`' not in el:
                    edu_degree = el
                    break
            if edu_match:
                education_section = {
                    "institution": edu_match.group(1),
                    "dates": edu_match.group(2),
                    "degree": edu_degree,
                }

        elif section.startswith("Experience"):
            entries = re.split(r'^### ', section, flags=re.MULTILINE)[1:]
            for entry in entries:
                parsed = parse_experience_entry(entry)
                if parsed:
                    experience_entries.append(parsed)

        elif section.startswith("Courses"):
            course_lines = re.split(r'^### ', section, flags=re.MULTILINE)[1:]
            for cl in course_lines:
                parsed = parse_course(cl.strip())
                if parsed:
                    courses.append(parsed)

    # --- Build LaTeX ---
    e = escape_latex

    contact_items = []
    if "email" in contacts:
        email = contacts["email"][0]
        contact_items.append(rf'\href{{mailto:{email}}}{{{e(email)}}}')
    if "phone" in contacts:
        phone = contacts["phone"][0]
        contact_items.append(e(phone))
    if "location" in contacts:
        loc = contacts["location"][0]
        contact_items.append(e(loc))
    if "linkedin" in contacts:
        text, url = contacts["linkedin"]
        contact_items.append(rf'\href{{{url}}}{{{e(text)}}}')
    if "github" in contacts:
        text, url = contacts["github"]
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
        courses_latex += rf"""  \item \href{{{course['url']}}}{{{e(course['name'])}}}
"""

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

%% ---- Summary ----
{e(summary)}

%% ---- Education ----
\section*{{Education}}
\subsection*{{{e(education_section['institution'])} \hfill \normalfont\textit{{{e(education_section['dates'])}}}}}
{e(education_section['degree'])}

%% ---- Experience ----
\section*{{Experience}}
{exp_latex}

%% ---- Courses ----
\section*{{Courses}}
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
