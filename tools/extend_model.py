import ast
import re


def extract_class_contents(filename):
    with open(filename, "r") as file:
        source = file.read()

    parsed_source = ast.parse(source)
    classes = [node for node in parsed_source.body if isinstance(node, ast.ClassDef)]

    class_contents = {}

    for class_node in classes:
        start_line = class_node.lineno
        end_line = class_node.end_lineno

        # Extract lines and handle skipping
        class_lines = []
        skip = False
        for line in source.splitlines()[start_line:end_line]:
            if line.strip() == "# skip":
                skip = True
                continue
            if line.strip() == "# /skip":
                skip = False
                continue
            if not skip:
                class_lines.append(line)

        class_contents[class_node.name] = "\n".join(class_lines)

    return class_contents


def append_or_replace_in_jinja_template(template_filename, classes_content):
    with open(template_filename, "r") as file:
        template_content = file.read()

    for class_name, content in classes_content.items():
        class_block_pattern = (
            r"{%- if class_name == \"" + re.escape(class_name) + r"\" %}.*?{%- endif %}"
        )
        new_block = (
            '{%- if class_name == "'
            + class_name
            + '" %}\n'
            + content
            + "\n{%- endif %}"
        )

        # Check if class block exists
        if re.search(class_block_pattern, template_content, re.DOTALL):
            # Replace existing block
            template_content = re.sub(
                class_block_pattern, new_block, template_content, flags=re.DOTALL
            )
        else:
            # Append new block
            template_content += new_block

    # Write back to the template file
    with open(template_filename, "w") as file:
        file.write(template_content)


# Example Usage
source_filename = "tools/model.py"
template_filename = "tools/custom_template/pydantic_v2/BaseModel.jinja2"
classes_content = extract_class_contents(source_filename)
append_or_replace_in_jinja_template(template_filename, classes_content)
