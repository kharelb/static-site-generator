from generate_content import  (
    copy_from_static_to_public,
    generate_pages_recursive,
)

def main():
    source_dir = "static"
    destination_dir = "public"
    copy_from_static_to_public(source_dir, destination_dir)
    template_path = "template.html"
    from_dir = "content"
    generate_pages_recursive(from_dir, template_path, destination_dir)



if __name__ == "__main__":
    main()
