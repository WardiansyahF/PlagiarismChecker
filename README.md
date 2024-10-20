# Plagiarism Checker

A simple plagiarism checker application built using Python and Tkinter. The program extracts text from various file formats (.txt, .pdf, and .docx) and calculates the cosine similarity between them to identify potential plagiarism.

## Features

- Supports file formats: `.txt`, `.pdf`, and `.docx`
- Calculates cosine similarity between files
- Displays results in a user-friendly interface
- Highlights high similarity scores
- Allows users to set a similarity threshold
- Option to save results to a file (feature to be implemented)

## Requirements

Make sure you have the following Python packages installed:

- `tkinter` (usually comes pre-installed with Python)
- `PyPDF2`
- `python-docx`
- `scikit-learn`

You can install the required packages using pip:

```bash
pip install PyPDF2 python-docx scikit-learn
```

## Usage

1. Clone this repository or download the code files.
2. Run the `plagiarism_checker.py` file:

```bash
python plagiarism_checker.py
```

3. Select the directory containing the files you want to check for plagiarism.
4. Set the similarity threshold (default is 70%).
5. Click the "Check Plagiarism" button to start the analysis.
6. Review the results displayed in the Treeview.

## Screenshots

(You can add screenshots of your application here)

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request.


Feel free to customize it further based on your preferences and any additional features you might add in the future!