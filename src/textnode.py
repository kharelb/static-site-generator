from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and
         self.text_type==other.text_type and
         self.url == other.url)
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, props=None)
    
        case TextType.BOLD:
            return LeafNode("b", text_node.text, props=None)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, props=None)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text, props=None)
        
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href":text_node.url})

        case TextType.IMAGE:
            return LeafNode("img", "", props={"src":text_node.url, "alt":text_node.text})

        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

