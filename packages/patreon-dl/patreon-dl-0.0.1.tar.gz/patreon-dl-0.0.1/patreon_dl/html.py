from html.parser import HTMLParser as BaseHTMLParser


class HTMLParser(BaseHTMLParser):
    def __init__(self):
        self.images: list[str] = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


def extract_images(html: str) -> list[str]:
    parser = HTMLParser()
    parser.feed(html)
    return parser.images
