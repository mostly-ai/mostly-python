# Copyright 2024 MOSTLY AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Constant for the file path
FILE_PATH = "mostlyai/domain.py"

# Dictionary for enum replacements
enum_replace_dict = {
    "        'AUTO'": "        ModelEncodingType.auto",
    "        'NEW'": "        GeneratorCloneTrainingStatus.new",
    "        'CONSTANT'": "        RareCategoryReplacementMethod.constant",
    "Field('SOURCE'": "Field(ConnectorAccessType.source",
}


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
            new_lines.append(
                "import pandas as pd\nfrom pathlib import Path\n"
                "from pydantic import field_validator\nfrom mostlyai.client._base_utils import convert_to_base64"
            )
        elif "from typing" in line and not import_typing_updated:
            # Append ', ClassVar' to the line if it doesn't already contain ClassVar
            if "ClassVar" not in line:
                line = line.rstrip() + ", ClassVar, Union, Literal, Annotated\n"
                import_typing_updated = True
            new_lines.append(line)
        else:
            # Replace 'UUID' with 'str'
            new_line = line.replace("UUID", "str")

            # Apply replacements from enum_replace_dict
            for old, new in enum_replace_dict.items():
                if old in new_line:
                    new_line = new_line.replace(old, new)

            new_lines.append(new_line)

    # Write the modified contents back to the file
    with open(file_path, "w") as file:
        file.writelines(new_lines)


if __name__ == "__main__":
    # Perform postprocessing on the model file
    postprocess_model_file(FILE_PATH)
    print("Postprocessing completed.")
