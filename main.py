import os
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2
import docx
import csv

# Function to extract text from .txt, .pdf, and .docx files
def extract_text_from_file(filepath):
    if filepath.endswith(".txt"):
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    elif filepath.endswith(".pdf"):
        text = ""
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text
    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    return ""

# Function to load files from a directory (supports .txt, .pdf, and .docx)
def load_files_from_directory(directory_path):
    files_content = []
    filenames = []
    for filename in os.listdir(directory_path):
        if filename.endswith((".txt", ".pdf", ".docx")):
            filepath = os.path.join(directory_path, filename)
            content = extract_text_from_file(filepath)
            if content:  # Only include files with valid content
                files_content.append(content)
                filenames.append(filename)
    return files_content, filenames

# Function to calculate cosine similarity and return results
def calculate_cosine_similarity(files_content, filenames):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(files_content)
    similarity_matrix = cosine_similarity(tfidf_matrix)

    return similarity_matrix

# Function to display results in the Treeview
def display_results(similarity_matrix, filenames, threshold):
    for i in range(len(filenames)):
        for j in range(i + 1, len(filenames)):
            score = similarity_matrix[i][j] * 100
            if score > threshold:
                tree.insert("", tk.END, values=(filenames[i], filenames[j], f"{score:.2f}%"), 
                             tags=("high_similarity",))
            else:
                tree.insert("", tk.END, values=(filenames[i], filenames[j], f"{score:.2f}%"))

# Function to check plagiarism and display results
def check_plagiarism(directory_path, result_text_widget, threshold):
    files_content, filenames = load_files_from_directory(directory_path)
    if files_content:
        similarity_matrix = calculate_cosine_similarity(files_content, filenames)
        display_results(similarity_matrix, filenames, threshold)
        save_button.config(state="normal")  # Enable save button
    else:
        messagebox.showwarning("Warning", "No valid files found in the directory!")

# Function to select a directory
def select_directory():
    directory_path = filedialog.askdirectory()
    if directory_path:
        directory_label.config(text=directory_path)

# Main GUI application
root = tk.Tk()
root.title("Plagiarism Checker")

# Menu bar
menu_bar = Menu(root)
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save Results", command=lambda: save_results_to_file(results_text, result_data))
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Directory selection
directory_label = tk.Label(root, text="No directory selected", width=50)
directory_label.pack(pady=10)
select_dir_button = tk.Button(root, text="Select Directory", command=select_directory)
select_dir_button.pack(pady=5)

# Similarity threshold input
threshold_label = tk.Label(root, text="Similarity Threshold (%):")
threshold_label.pack(pady=5)
threshold_entry = tk.Entry(root)
threshold_entry.pack(pady=5)
threshold_entry.insert(0, "70")  # Default threshold value

# Result display using Treeview
tree = ttk.Treeview(root, columns=("File 1", "File 2", "Similarity Score"), show='headings')
tree.heading("File 1", text="File 1")
tree.heading("File 2", text="File 2")
tree.heading("Similarity Score", text="Similarity Score")
tree.pack(pady=10)

# Tag configuration for highlighting
tree.tag_configure("high_similarity", background="lightcoral")  # Heat color for high similarity

# Save button (disabled initially)
save_button = tk.Button(root, text="Save Results", state="disabled")
save_button.pack(pady=5)

# Status bar
status_bar = tk.Label(root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor='w')
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Check plagiarism button
def on_check_plagiarism():
    threshold = float(threshold_entry.get())  # Get threshold from entry
    status_bar.config(text="Status: Checking for plagiarism...")
    check_plagiarism(directory_label.cget("text"), None, threshold)
    status_bar.config(text="Status: Ready")

check_button = tk.Button(root, text="Check Plagiarism", command=on_check_plagiarism)
check_button.pack(pady=10)

# Run the GUI application
root.mainloop()
