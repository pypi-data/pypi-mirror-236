from dataclasses import Field


class PMDocument():
    """Class for storing a piece of text and associated metadata."""
    page_content: str
    """String text."""
    metadata: dict
    """Arbitrary metadata about the page content (e.g., source, relationships to other
        documents, etc.).
    """

    def __init__(self, page_content=None, metadata=None):
        self.page_content = page_content
        self.metadata = {"source": metadata}


    @classmethod
    def is_lc_serializable(cls) -> bool:
        """Return whether this class is serializable."""
        return True
