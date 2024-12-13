import os
import psutil  # To identify processes holding files (requires `pip install psutil`)

def force_delete(file_path):
    """Force delete a file by ensuring no processes are using it."""
    try:
        # Check if the file is being used and terminate the process
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                for open_file in proc.open_files():
                    if open_file.path == file_path:
                        proc.terminate()
                        proc.wait()
            except Exception:
                continue  # Ignore processes we can't access

        # Remove the file
        os.remove(file_path)
        return True
    except Exception as e:
        print(f"Could not delete file '{file_path}': {e}")
        return False

def delete_error_files(results_folder, error_message, not_useful_message):
    if not os.path.exists(results_folder):
        print(f"Folder '{results_folder}' does not exist.")
        return

    error_count = 0
    not_useful_count = 0

    for filename in os.listdir(results_folder):
        file_path = os.path.join(results_folder, filename)
        
        # Skip non-file entries
        if not os.path.isfile(file_path):
            continue
        
        # Read file content and check for specific strings
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            if error_message in content:
                if force_delete(file_path):
                    error_count += 1
            elif not_useful_message in content:
                if force_delete(file_path):
                    not_useful_count += 1

    # Print results
    print(f"Deleted {error_count} files containing the error '{error_message}'.")
    print(f"Deleted {not_useful_count} files containing the string '{not_useful_message}'.")

if __name__ == "__main__":
    results_folder = "results"
    error_message = "Error: Error code: 429"
    not_useful_message = "DOC_NOT_USEFUL"
    delete_error_files(results_folder, error_message, not_useful_message)
