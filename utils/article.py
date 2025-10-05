class Article:
    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body
        self.word_count = self._calculate_word_count()
        self.first_paragraph = self._get_first_paragraph()

    def _calculate_word_count(self) -> int:
        return len(self.body.split())

    def _get_first_paragraph(self) -> str:
        words = self.body.split()
        return ' '.join(words[:50])

    def __repr__(self):
        return f"Article(title={self.title!r}, word_count={self.word_count})"