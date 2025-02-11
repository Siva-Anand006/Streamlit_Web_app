import os

# Define the folder structure
folders = [
    "Sentiment_Analysis/Datasets",
    "Sentiment_Analysis/src"
]

# Define the files and their content
files = {
    "Sentiment_Analysis/src/__init__.py": "",
    "Sentiment_Analysis/src/data_loader.py": "",
    "Sentiment_Analysis/src/model.py": "",
    "Sentiment_Analysis/src/predictor.py": "",
    "Sentiment_Analysis/.gitignore": "",
    "Sentiment_Analysis/requirements.txt": "",
    "Sentiment_Analysis/README.md": "",
    "Sentiment_Analysis/app.py": "",
}

# Create directories first
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create the files
for file_path, content in files.items():
    # Ensure the parent directories exist before creating the file
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as file:
        file.write(content)

print("✅ Folders and files created successfully!")
