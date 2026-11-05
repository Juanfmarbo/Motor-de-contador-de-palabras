# Efficient Word Searcher in Text Files

**Final project — Data Structures**  
**University of La Sabana · 2026**  
**Professor:** Arley Calderón  
**Team:** Juan, Daniel, and Sara

## About the project

We developed a Python console application that loads a `.txt` file and lets us explore its content in several ways: exact searches, case-insensitive searches, prefix searches, statistics, word retrieval by position, and a comparison of two search methods.

Our main objective was **to avoid scanning the entire text for every query**. When the file is loaded, the program builds data structures that preserve the original order of the words and provide fast access to their information.

The solution combines **dictionaries (hash tables), lists, compact arrays, and binary search**. It only uses Python's standard library.

## Requirements

- **Python 3.10 or newer** (the main menu uses `match/case`).
- A `.txt` file encoded in **UTF-8** (UTF-8 with BOM is also supported).
- **Windows, macOS, or Linux**.

The modules used by the project, such as `pathlib`, `array`, `time`, `bisect`, and `heapq`, are included with Python. **No `pip install` command is required.**

## Project structure

```text
Project/
├── main.py         # Main menu and program control
├── librerias.py    # File loading, data structures, and search functions
├── Files/          # Folder for the .txt files to analyze
├── README.md       # Project documentation
└── .gitignore      # Files excluded from version control
```

Text files can be stored in `Files/` or accessed through a valid relative or absolute path. The project can be copied to another computer without changing the source code.

## How to run the program

1. Download or clone the repository.
2. Keep `main.py` and `librerias.py` in the same project folder.
3. Place the text file in `Files/`, or have its path ready.
4. Open a terminal in the project folder.
5. Run the program using the command for your operating system.

**Windows:**

```powershell
py main.py
```

**macOS or Linux:**

```bash
python3 main.py
```

6. Select **1 — Load file** and enter the file's path, for example `Files/text.txt`.
7. Once the file loads successfully, choose any of the available queries.

If a file is already loaded, the program asks whether we want to replace it.

> **Important:** When moving the project to another computer, copy both Python files and any text files you want to analyze. There are no additional dependencies to install.

## Menu options

| Option | Function | What it does |
|:---:|---|---|
| **1** | Load file | Reads and validates a `.txt` file and builds the search structures. |
| **2** | Exact search | Finds a complete word, respecting uppercase and lowercase letters. |
| **3** | Simple search | Finds a complete word without distinguishing uppercase and lowercase letters. |
| **4** | Prefix search | Finds occurrences of words beginning with a given prefix. |
| **5** | Statistics | Displays general information, including the total number of words and the first, middle, and last words. |
| **6** | Word No. X | Retrieves the word and its line number from a valid position in the text. |
| **7** | Comparative analysis | Compares a sequential search with a dictionary-based search and reports their execution times. |
| **0** | Exit | Closes the program. |

**Options 2–7 require a file to be loaded successfully first.**

## What counts as a word?

Following the assignment's rules, a **word is a sequence of characters separated by whitespace**, including spaces, tabs, and line breaks. The program does not automatically remove punctuation.

For example:

- `casa` and `casa,` are **different** words.
- `casa` and `Casa` are **different** in an exact search.
- `casa` and `Casa` are treated as **equivalent** in a simple search because their case is normalized.

Prefix searches also use normalized words, so they do not distinguish uppercase and lowercase letters.

## How the data is organized

During the initial load, the program builds these structures:

| Structure | Type | Stored information | Purpose |
|---|---|---|---|
| `vocabulario` | `list` | Each distinct original word, stored once. | Retrieves a word from its identifier without repeating its string for every occurrence. |
| `normalizadas` | `list` | Normalized forms associated with the original vocabulary. | Supports case-insensitive queries. |
| `orden_ids` | `array('I')` | Word identifiers for **every occurrence**, in the file's original order. | Retrieves words by position using compact integers. |
| `lineas` | `array('I')` | Line number corresponding to each occurrence. | Retrieves the location of a word. |
| `indice_exacto` | `dict` | Original word → identifier, frequency, first line, and last line. | Answers exact searches quickly. |
| `indice_simple` | `dict` | Normalized word → compact array of occurrence positions. | Locates every appearance regardless of case. |
| `claves_ordenadas` | `list` | Distinct normalized keys sorted alphabetically. | Enables prefix searches with binary search. |

The entries at the same position in `orden_ids` and `lineas` describe the **same occurrence**. This allows us to preserve both the order of the text and the line numbers without storing every word as a separate string.

## Efficiency and complexity

Let:

- **N** be the total number of word occurrences in the file.
- **U** be the number of distinct original words.
- **V** be the number of distinct normalized words.
- **m** be the number of distinct normalized words matching a prefix.
- **k** be the number of occurrences returned by a query.

| Operation | Expected time complexity | Why |
|---|---|---|
| Load and index file | `O(N + V log V)` | Processes the occurrences and sorts the normalized search keys once. |
| Exact search | `O(1)` | Looks up the original word in a dictionary. |
| Simple search | `O(1 + k)` | Uses a dictionary to find the word, then visits its matching positions if they must be displayed. |
| Prefix search | `O(log V + m + k)` | Uses binary search to reach the first matching key, then processes matching keys and occurrences. |
| Statistics / direct positional access | `O(1)` for precomputed totals and direct positions | Reads stored counts or accesses an array position without scanning the text. |
| Sequential search (comparison) | `O(N)` | May need to inspect every word occurrence. |
| Indexed search (comparison) | `O(1)` on average | Uses a dictionary instead of checking each occurrence. |

Dictionary lookup is **O(1) on average**, not a guaranteed worst-case bound. When a search prints multiple matches, the time needed to display them also depends on the number of results.

The main data structures require **O(N + U + V)** space, excluding the character storage needed for the distinct words. The arrays keep repeated identifiers and line numbers in a compact format, which is useful when working with large files.

### Why we chose these structures

- **Dictionaries:** fast access to words without a complete scan for every search.
- **Lists:** direct access to the unique vocabulary by identifier.
- **`array('I')`:** more compact storage for large sequences of nonnegative integers than regular Python lists of integers.
- **Sorted keys + binary search:** fast access to the beginning of a prefix range without examining every distinct word.
- **Sequential search in option 7:** a baseline that lets us measure the practical benefit of the index.

The trade-off is that **loading and indexing require extra time and memory at the beginning**, but repeated searches become much faster. This design is especially helpful when we want to make many queries against the same large text file.

---

**Final project for Data Structures — University of La Sabana, 2026.**

