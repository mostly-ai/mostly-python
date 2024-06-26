# Constant for the file path
FILE_PATH = "mostlyai/model.py"


def postprocess_model_file(file_path):
    # Read the contents of the file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # Modify the contents
    new_lines = []
    import_typing_updated = False

    for line in lines:
        # Remove filename comment
        if "#   filename:" in line:
            pass
        # Skip the import line for UUID
        elif "import UUID" in line:
            new_lines.append("import pandas as pd\nfrom pathlib import Path")
        elif "from typing" in line and not import_typing_updated:
            # Append ', ClassVar' to the line if it doesn't already contain ClassVar
            if "ClassVar" not in line:
                line = line.rstrip() + ", ClassVar, Union, Literal\n"
                import_typing_updated = True
            new_lines.append(line)
        else:
            # Replace 'UUID' with 'str'
            new_line = line.replace("UUID", "str")
            new_lines.append(new_line)

    # Write the modified contents back to the file
    with open(file_path, "w") as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    # Perform postprocessing on the model file
    postprocess_model_file(FILE_PATH)
    print("Postprocessing completed.")
