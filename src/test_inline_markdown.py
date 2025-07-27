import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_text_nodes,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_single_image(self):
        node = TextNode(
            "Text before ![alt text](https://example.com/image.png) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_images(self):
        node = TextNode(
            "Start ![first](https://img1.png) middle ![second](https://img2.png) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "https://img1.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "https://img2.png"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_only_image(self):
        node = TextNode("![solo image](https://img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("solo image", TextType.IMAGE, "https://img.png")],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode(
            "![first](https://img.png) then some text", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.IMAGE, "https://img.png"),
                TextNode(" then some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode(
            "Text first then ![last](https://img.png)", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Text first then ", TextType.TEXT),
                TextNode("last", TextType.IMAGE, "https://img.png"),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First node", TextType.TEXT),
            TextNode("Second ![img](https://img.png) node", TextType.TEXT),
            TextNode("Third node", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("First node", TextType.TEXT),
                TextNode("Second ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://img.png"),
                TextNode(" node", TextType.TEXT),
                TextNode("Third node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_single_link(self):
        node = TextNode(
            "Text before [link text](https://example.com) text after",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text before ", TextType.TEXT),
                TextNode("link text", TextType.LINK, "https://example.com"),
                TextNode(" text after", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_links(self):
        node = TextNode(
            "Start [first link](https://link1.com) middle [second](https://link2.com) end",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("first link", TextType.LINK, "https://link1.com"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.LINK, "https://link2.com"),
                TextNode(" end", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("This is just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_only_link(self):
        node = TextNode("[solo link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [TextNode("solo link", TextType.LINK, "https://example.com")],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode(
            "[first link](https://example.com) then some text", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first link", TextType.LINK, "https://example.com"),
                TextNode(" then some text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode(
            "Text first then [last link](https://example.com)", TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Text first then ", TextType.TEXT),
                TextNode("last link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )

    def test_multiple_nodes_link(self):
        nodes = [
            TextNode("First node", TextType.TEXT),
            TextNode("Second [link](https://example.com) node", TextType.TEXT),
            TextNode("Third node", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("First node", TextType.TEXT),
                TextNode("Second ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" node", TextType.TEXT),
                TextNode("Third node", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_back_to_back_links(self):
        node = TextNode(
            "[first](https://link1.com)[second](https://link2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("first", TextType.LINK, "https://link1.com"),
                TextNode("second", TextType.LINK, "https://link2.com"),
            ],
            new_nodes,
        )

    def test_invalid_link_syntax(self):
        node = TextNode("Text with [invalid link(missing paren", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_mixed_formatting(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_only_bold(self):
        text = "This is **bold** text"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            nodes
        )

    def test_only_italic(self):
        text = "This is *italic* text"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            nodes
        )

    def test_only_code(self):
        text = "This is `code` text"
        nodes = text_to_text_nodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ],
            nodes
        )
    def test_empty_text(self):
        text = ""
        nodes = text_to_text_nodes(text)
        self.assertListEqual([], nodes)

if __name__ == "__main__":
    unittest.main()