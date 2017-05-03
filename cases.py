from contexts import LineLengthExceededContext
from redbaron import Node


class CaseType:
    def __init__(self):
        pass

    COMMENT = 'comment'


class LineLengthExceededCase:
    def __init__(self, context, node, case_type):
        """
        :type context: LineLengthExceededContext 
        :type node: Node
        :type case_type: str 
        """
        self._context = context
        self._node = node
        self._case_type = case_type

    def get_line_number(self):
        return self._context.file_context.line_number

    def get_line_contents(self):
        return self._context.file_context.line_content

    def get_source_file_name(self):
        return self._context.file_context.source_file_name

    def get_offending_node(self):
        return self._node

    def get_case_type(self):
        return self._case_type
