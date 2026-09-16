# Unit 3: Data Structures and Algorithms

Learn Key Institute, Undergraduate Diploma in Software Design (MQF Level 5).

Assignment: **inserting a new cell at the end of a linked list**. A list of twelve Info–Link cells is built in C++, and the cell pointed to by `New` is attached after the last cell, so that the Link that held Λ (`nullptr`) now points to `New`.

The report is in [`out/`](out/) as a PDF and as a Word document.

## Contents

| Folder | What it holds |
|---|---|
| `code/` | The linked list (`linked_list.hpp`, `linked_list.cpp`), the demonstration program (`main.cpp`), the tests (`test_linked_list.cpp`) and a `Makefile` |
| `diagrams/` | The script that draws the report's figures, and the rendered PNGs |
| `report/` | The report text (`content/*.md`), the cover-sheet details and the scripts that build the Word and PDF files |
| `out/` | The finished report, plus the captured program output quoted in it |

## Running the code

Needs a C++17 compiler (developed with Apple Clang 21).

```bash
cd code
make run      # builds the 12-cell list, inserts cell 13, prints both lists with memory addresses
make test     # 12 tests, 63 checks
make check    # tests, AddressSanitizer + UndefinedBehaviorSanitizer, and a leak check (macOS)
```

## Building the report

Needs Python with `python-docx`, `lxml` and `pypdf`, and LibreOffice (`soffice`) for the PDF.

```bash
cd report
./build.sh            # builds the .docx, renders it, fills in the contents page numbers, writes the PDF
python3 audit_docx.py # checks the formatting rules from the brief
```

## Author

Imran Hossain Chowdhury, registration no. 11248.
