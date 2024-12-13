import os
import asyncio
from openai import AsyncOpenAI
from tqdm import tqdm

API_KEY = "open_ai_api_key"
client = AsyncOpenAI(api_key=API_KEY)


async def get_openai_response(prompt):
    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


async def process_file(file_path, prompt_template, results_folder, progress_bar):
    filename = os.path.basename(file_path)
    try:
        # Log the file being processed
        progress_bar.set_description(f"Processing: {filename}")
        
        # Read the file content
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        # Construct the prompt
        prompt = f"{prompt_template}\n\n{file_content}"

        # Get the response from the OpenAI API
        response = await get_openai_response(prompt)

        # Save the response to a new file in the results folder
        result_file_path = os.path.join(results_folder, f"{filename}_result.txt")
        with open(result_file_path, "w", encoding="utf-8") as result_file:
            result_file.write(response)

        # Log success
        progress_bar.update(1)
    except Exception as e:
        print(f"Error processing file {filename}: {e}")


async def process_files_in_folder(folder_path):
    prompt_template = """
    Your task is as following:

    You'll be fed a text document, scrapped from a skincare website.
    There will be random irrelevant headers and footers that you'll have to ignore.
    There will be useful information somewhere in the middle of the document. What you need to do is: Rewrite the document with high quality content style, while preserving maximum information.

    There might be mentions of skin care products. PAY SPECIFIC ATTENTION TO THEM. If you have some useful information about them that is relevant to the topic, you may augment that while rewriting the document. However, if you do not know anything - keep things as it is - DO NOT GUESS.

    There might be instances when the document has zero information related to skin care. In that case, just return a simple string called DOC_NOT_USEFUL.

    Also, summarize the document's content on the top by providing a fitting title, which should not be more than 10 words (can be lower).
    """

    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    # Create a results folder to save outputs
    results_folder = "results"
    os.makedirs(results_folder, exist_ok=True)

    # Gather all tasks for processing files
    tasks = []
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)

    if total_files == 0:
        print(f"No files to process in folder '{folder_path}'.")
        return

    # Initialize the progress bar
    with tqdm(total=total_files, desc="Processing files", unit="file") as progress_bar:
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            tasks.append(process_file(file_path, prompt_template, results_folder, progress_bar))

        # Run all tasks asynchronously
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    data_folder = "data"
    asyncio.run(process_files_in_folder(data_folder))
