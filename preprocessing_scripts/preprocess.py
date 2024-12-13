import os

def preprocess_files(data_folder):
    # Step 1: Delete non-.txt files and empty files
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        
        # Check if it's not a .txt file or is empty
        if not filename.endswith('.txt') or os.path.getsize(file_path) == 0:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    
    # Step 2: Process remaining .txt files
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        if filename.endswith('.txt'):
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Process lines
            processed_lines = []
            short_line_count = 0
            include_mode = True  # Whether to include content
            
            for line in lines:
                line = line.strip()  # Remove leading/trailing whitespace
                
                if len(line) >= 20:
                    short_line_count = 0
                    include_mode = True
                else:
                    short_line_count += 1
                    if short_line_count >= 3:
                        include_mode = False
                
                if include_mode:
                    processed_lines.append(line)
            
            # Write back processed content to the same file
            with open(file_path, 'w') as file:
                file.write("\n".join(processed_lines))
            
            print(f"Processed: {file_path}")

# Path to your data folder
data_folder = "data"
preprocess_files(data_folder)
