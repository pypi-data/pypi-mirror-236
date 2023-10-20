from pathlib import Path

import fitz

from .processed_page import ProcessedPage


class ProcessedDoc:
    """Class to provide extra methods to pymupdf doc class"""

    def __init__(self, fname: Path = None, stream: bytes = None) -> None:
        if not fname:
            self.doc = fitz.open(stream=stream)
        else:
            self.doc = fitz.open(str(fname))

    def __len__(self) -> int:
        return len(self.doc)

    def __getitem__(self, key) -> ProcessedPage:
        return ProcessedPage(self.doc[key])
