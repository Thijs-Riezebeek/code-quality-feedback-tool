from redbaron import RedBaron


class FileContext:
    def __init__(self, line_number, line_content, source_file_name):
        self.line_number = line_number  # type: int
        self.line_content = line_content  # type: str
        self.source_file_name = source_file_name  # type: str


class LineLengthExceededContext:
    def __init__(self, file_context, source_file_fst):
        self.file_context = file_context  # type: FileContext
        self.source_file_fst = source_file_fst  # type: RedBaron
