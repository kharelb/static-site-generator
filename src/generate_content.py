import re
import shutil
from pathlib import Path
from markdown_blocks import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_path_content = Path(dir_path_content)
    dest_dir_path = Path(dest_dir_path)
    if not dir_path_content.exists():
        raise FileNotFoundError(f"Source path '{dir_path_content}' does not exist.")
    if not dest_dir_path.exists():
        print(f"Destination path '{dest_dir_path}' does not exist. Creating it..")
        dest_dir_path.mkdir(parents=True, exist_ok=True)
    # List all the files and directories in the current directory
    for item in dir_path_content.iterdir():
        if item.is_file() and item.suffix == '.md':
            # If it's a markdown file, generate the page
            print(f"Generating page for file: {item}")
            generate_page(item.parent, template_path, dest_dir_path)
        elif item.is_dir():
            # If it's a directory, recursively call this function
            print(f"Entering directory: {item}")
            generate_pages_recursive(item, template_path, dest_dir_path / item.name)


def generate_page(from_path, template_path, dest_path):
    from_path = f"{from_path}/index.md"
    dest_path = f"{dest_path}/index.html"
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, 'r') as f:
        contents = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    html_node = markdown_to_html_node(contents)
    html = html_node.to_html()
    title = extract_title(contents)

    html = template.replace("{{ Content }}", html).replace("{{ Title }}", title)

    # Check if the destination directory exists, if not create it
    dest_dir = Path(dest_path).parent
    if not dest_dir.exists():
        print(f"Creating destination directory: {dest_dir}")
        dest_dir.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html)

def extract_title(markdown):
    if not markdown:
        raise Exception("The markdown content is empty.")
    stripped_markdown = markdown.strip()
    split_markdown = stripped_markdown.splitlines()
    if not split_markdown[0].startswith("# "):
        raise Exception(f"No title found in the first line of the markdown: {stripped_markdown[0]}")

    else:
        return re.match(r"#*\s*(.*)", split_markdown[0]).group(1).strip()

def copy_from_static_to_public(source, destination):
    source_dir = Path(source)
    destination_dir = Path(destination)

    if not source_dir.exists():
        raise FileNotFoundError(f"Source path '{source}' does not exist.")

    if not destination_dir.exists():
        print(f"Destination path '{destination}' does not exist. Creating it..")
        destination_dir.mkdir(parents=True, exist_ok=True)

    else:
        print(f"Destination path '{destination}' already exists. Removing it..")
        shutil.rmtree(destination_dir)
        print(f"Creating destination path '{destination}'..")
        destination_dir.mkdir(parents=True, exist_ok=True)

    for item in source_dir.iterdir():
        if item.is_file():
            print(f"Copying file '{item.name}' to '{destination_dir}'")
            shutil.copy(item, destination_dir)

        elif item.is_dir():
            print(f"Copying directory '{item.name}' to '{destination_dir}'")
            copy_from_static_to_public(item, destination_dir/item.name)