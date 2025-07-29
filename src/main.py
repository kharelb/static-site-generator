import sys
from pathlib import Path

from generate_content import  (
    copy_from_static_to_public,
    generate_pages_recursive,
)

args = sys.argv

try:
    basepath = Path(args[1])
except IndexError:
    basepath = Path("/")

def main():
    source_dir = "static"
    destination_dir = "docs"  # Changing from public to docs to serve the site in Github
    copy_from_static_to_public(source_dir, destination_dir)
    template_path = "template.html"
    from_dir = "content"
    generate_pages_recursive(from_dir, template_path, destination_dir, basepath)



if __name__ == "__main__":
    main()
