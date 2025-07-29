import re
from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_node = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_node.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_node.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_node)

    return  new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        markdown_images = extract_markdown_images(old_node.text)

        if len(markdown_images) == 0:
            new_nodes.append(old_node)
            continue

        text_to_be_splitted = old_node.text
        split_nodes = []
        for i, image in enumerate(markdown_images):
            splitted = re.split(fr"!\[{image[0]}\]\({image[1]}\)", text_to_be_splitted, maxsplit=1)
            text_to_be_splitted = splitted[1]
            if splitted[0] != "":
                split_nodes.append(TextNode(splitted[0], TextType.TEXT))
            split_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

            if i == len(markdown_images) - 1 and text_to_be_splitted != "":
                split_nodes.append(TextNode(text_to_be_splitted, TextType.TEXT))

        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        markdown_links = extract_markdown_links(old_node.text)
        if len(markdown_links) == 0:
            new_nodes.append(old_node)
            continue

        text_to_be_splitted = old_node.text
        split_nodes = []
        for i, link in enumerate(markdown_links):
            splitted = re.split(fr"\[{link[0]}\]\({link[1]}\)", text_to_be_splitted, maxsplit=1)
            text_to_be_splitted = splitted[1]
            if splitted[0] != "":
                split_nodes.append(TextNode(splitted[0], TextType.TEXT))
            split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

            if i == len(markdown_links) - 1 and text_to_be_splitted != "":
                split_nodes.append(TextNode(text_to_be_splitted, TextType.TEXT))

        new_nodes.extend(split_nodes)

    return new_nodes

def text_to_text_nodes(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if text == "":
        return []
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes