from google import genai
from dotenv import load_dotenv
import pathlib
import os,sys
load_dotenv()
from google.genai import types
from e2b_code_interpreter import Sandbox
import base64
import time

e2b_key=os.getenv("E2B_API_KEY")


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_ID="gemini-2.5-flash-preview-05-20" # @param ["gemini-2.5-flash-preview-05-20", "gemini-2.5-pro-preview-03-25", "gemini-2.0-flash", "gemini-2.0-flash-lite"] {"allow-input":true, isTemplate: true}


def generate_from_gemini(path,plot_type=None):
    max_retries = 4 
    delay = 2
    retry_count = 0

    data_file_local=pathlib.Path(path)
    if plot_type is None:
        plot_type=[]

    datafile = client.files.upload(
        file=pathlib.Path(path),
        config=types.FileDict(display_name='Dynamic Dataset')
    )

    # print(f"Uploaded file '{iris_datafile.display_name}' as: {iris_datafile.uri}")
    prompt=f"""
             "This csv file provides information about a dataset",
            "Create a function with name Generated_Code_Gemini. Take the uploaded csv file as input.",
            "Inside the function, Analyse the data and perform data cleaning if needed. ",
            "Shows basic info and summary statistics",
            "Plots useful graphs as mentioned in {plot_type}",
            "Use matplotlib and seaborn. Ensure matplotlib does not use `plt.show()`, and use `plt.savefig().` Make sure there are no errors and have exception handling ",
            "Log messages only when data is loaded or failed and successfully completed the analysis/plotting or when it failed.",
            "Create a folder Plots and Then save the plot as an image file and display the image. File name should be saved as <file_name>_<Plot_Type>_timestamp.png ",
            "In the end, the function should return a dictionary that says summary and it should have info about the dataset that can be helpful to show in the frontend. Do not return the logs, generate a comprehensive summary about the dataset in a paragraph. ",
            "Generated the python executable code for this. The executable code should not contain comments from gemini. It Should have import statements, function and its logic and the necessary documentation inside the function. That's all",
            "After the function is closed, call the function with the path mentioned for the file provided" """
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[
                types.Part.from_bytes(data=data_file_local.read_bytes(),
                                    mime_type='text/csv'),
            prompt
            ]
        )
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(delay)
    retry_count+=1

    return response.text


def run_ai_generated_code(csv_path, plot_type=None):
    sbx=Sandbox()
    print('Running the code in the sandbox....')
    ai_generated_code=generate_from_gemini(csv_path, plot_type)

    if ai_generated_code.startswith("```python"):
        ai_generated_code = ai_generated_code[len("```python"):].strip()
    elif ai_generated_code.startswith("```"):
        ai_generated_code = ai_generated_code[len("```"):].strip()

    if ai_generated_code.endswith("```"):
        ai_generated_code = ai_generated_code[: -len("```")].strip()

    execution = sbx.run_code(ai_generated_code)
    print('Code execution finished!')

    # First let's check if the code ran successfully.
    if execution.error:
        print('AI-generated code had an error.')
        print(execution.error.name)
        print(execution.error.value)
        print(execution.error.traceback)
        sys.exit(1)

    plot_dir="./Plots"
    #os.makedirs(plot_dir, exist_ok=True)
    plot_files = []
    result_idx = 0

    print(execution.results)
    
    for result in execution.results:
        if result.png:
            # Save the png to a file
            # The png is in base64 format.
            plot_filename = f'chart-{result_idx}.png'
            plot_path = os.path.join(plot_dir, plot_filename)
            with open(plot_path, 'wb') as f:
                f.write(base64.b64decode(result.png))
            print(f'Chart saved to {plot_path}')
            plot_files.append(f'/Plots/{plot_filename}')
            result_idx += 1

    return {
        "stdout": ', '.join(execution.logs.stdout),
        "plots": plot_files
        }



