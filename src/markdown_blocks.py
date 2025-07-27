import re
from enum import Enum

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from parentnode import ParentNode
from leafnode import LeafNode
from inline_markdown import  (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    text_to_text_nodes
)

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    if not markdown:
        return []
    splitted = markdown.split("\n\n")
    splitted = [block.strip() for block in splitted]
    final_splitted = [block for block in splitted if block != ""]
    return final_splitted

def block_to_block_type(block):
    heading_pattern = bool(re.match(r"#{1,6}\s", block))
    code_pattern = bool(re.match(r"^`{3}[^`{3}]*`{3}$", block))
    quote_pattern = bool(re.match(r"^>.+(?:\n\n>.+)*", block))
    unordered_list_pattern = bool(re.match(r"^-\s.+(?:\n-\s.+)*", block))
    ordered_list_pattern = bool(re.match(r"^\d\.\s.*(?:\n\d\.\s.*)*", block))
    if heading_pattern:
        return BlockType.HEADING
    elif code_pattern:
        return BlockType.CODE
    elif quote_pattern:
        return BlockType.QUOTE
    elif unordered_list_pattern:
        return BlockType.ULIST
    elif ordered_list_pattern:
        return BlockType.OLIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:

def text_to_children(text):
    text_nodes = text_to_text_nodes()







