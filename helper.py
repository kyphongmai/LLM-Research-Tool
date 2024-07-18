import os

def list_pdf_files(directory):
    try:
        # List all files and directories in the specified directory
        files_and_dirs = os.listdir(directory)
        
        # Filter out the .pdf files
        pdf_file_paths = [os.path.join(directory, f) for f in files_and_dirs if f.lower().endswith('.pdf') and os.path.isfile(os.path.join(directory, f))]
        return pdf_file_paths
    except FileNotFoundError:
        print(f"The directory {directory} does not exist.")
        return []
    except PermissionError:
        print(f"Permission denied to access the directory {directory}.")
        return []