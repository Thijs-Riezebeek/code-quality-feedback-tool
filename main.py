# coding=utf-8
from redbaron import RedBaron, Node, CommentNode
import abc
import os

NODE_TYPE_COMMENT = 'comment'

# TODO: requirements.txt/setup.py for pip


class CaseType:
    COMMENT = 'comment'


class SourceCodeFileFinder:
    def __init__(self):
        pass

    def find_python_files_in_directory(self, directory_path, recursively=True):
        absolute_file_paths = []

        for file_path in self._yield_all_absolute_file_paths_in_directory(directory_path):
            if file_path.endswith(".py"):
                absolute_file_paths.append(file_path)

        return absolute_file_paths

    @staticmethod
    def _yield_all_absolute_file_paths_in_directory(directory_path):
        for path_to_directory, _, file_names in os.walk(directory_path):
            for file_name in file_names:
                yield os.path.abspath(os.path.join(path_to_directory, file_name))


class CodeAnalyzer:
    def __init__(self):
        self._file_analyzers = []  # type: list[FileAnalyzer]
        self._source_code_file_finder = SourceCodeFileFinder()  # type: SourceCodeFileFinder

    def analyze_directory(self, directory_location, recursively=True):
        python_file_paths = self._source_code_file_finder.find_python_files_in_directory(directory_location)

        for python_file_path in python_file_paths:
            self.analyze_file(python_file_path)

    def analyze_file(self, file_path):
        with open(file_path) as file:
            file_contents = file.read()

        for file_analyzer in self._file_analyzers:
            file_analyzer.analyze(file_path, file_contents)

    def add_file_analyzer(self, file_analyzer):
        self._file_analyzers.append(file_analyzer)


class FileAnalyzer:
    def __init__(self):
        pass

    @abc.abstractmethod
    def analyze(self, file_path, file_contents):
        """
        :type file_path: str
        :type file_contents: str
        """
        raise NotImplementedError


class LineLengthAnalyzer(FileAnalyzer):
    def __init__(self):
        FileAnalyzer.__init__(self)

        self._line_length_exceeded_listeners = [] # type: list[LineLengthExceededListenerForComments]

    def analyze(self, file_path, file_contents):
        source_file_fst = None

        for line_number, line_content in self._yield_all_lengthy_lines(file_path):
            if  source_file_fst is None:
                source_file_fst = RedBaron(file_contents)

            context = LineLengthExceededContext(
                file_context=FileContext(line_number, line_content, file_path),
                source_file_fst=source_file_fst
            )

            self._notify_listeners(context)

    def _yield_all_lengthy_lines(self, file_path):
        with open(file_path) as file:
            for i, line in enumerate(file):
                line_number = i + 1

                if len(line) > 100:
                    self._debug_line(line_number, line, too_long=True)
                    yield line_number, line
                else:
                    self._debug_line(line_number, line)

    def _debug_line(self, line_number, line_contents, too_long=False):
        validity_char = "✓" if not too_long else "✗"

        print "[{:>3s}] {} {}".format(str(line_number), validity_char, line_contents.rstrip())


    def _notify_listeners(self, context):
        """
        :type context: LineLengthExceededContext 
        """
        for listener in self._line_length_exceeded_listeners:
            listener.on_line_length_exceeded(context)

    def add_line_length_exceeded_listener(self, line_too_long_listener):
        self._line_length_exceeded_listeners.append(line_too_long_listener)


class LineLengthExceededListenerForComments:
    def __init__(self):
        pass

    def on_line_length_exceeded(self, context):
        """
        :type context: LineLengthExceededContext 
        """
        # TODO: Find a way to find comments after if statements (same line)

        first_node_on_line = context.source_file_fst.at(context.file_context.line_number)

        comment_too_long_case = self.find_comment_too_long_case_on_line(first_node_on_line, context)

        if comment_too_long_case:
            print '*** DETECTED COMMMENT THAT IS TOO LONG {} ***'.format(comment_too_long_case.line_length_exceeded_context.file_context.line_number)

    def find_comment_too_long_case_on_line(self, node, context):
        """
        :type node: Node
        :type context: LineLengthExceededContext 
        :rtype: CommentTooLongCase 
        """
        comment_node = self.detect_comment_node_on_same_line(node)
        if not comment_node:
            return None

        return LineLengthExceededCase(context, node, CaseType.COMMENT)

    # TODO: Move elsewhere
    def detect_comment_node_on_same_line(self, node):
        """
        :type node: Node 
        """
        current_node = node

        while self._nodes_are_on_same_line(current_node, node):
            if current_node.type == NODE_TYPE_COMMENT:
                return current_node

            tmp_node = current_node.next
            if not tmp_node:
                tmp_node = current_node.next_intuitive

            current_node = tmp_node

        return None

    # TODO: Move elsewhere
    def _nodes_are_on_same_line(self, node, other_node):
        """
        :type node: Node 
        :type other_node: Node 
        :rtype: bool 
        """
        if not node or not other_node:
            return False

        if not self._node_is_on_single_line(node) or not self._node_is_on_single_line(other_node):
            return False

        node_box = node.absolute_bounding_box
        other_node_box = other_node.absolute_bounding_box

        if node_box.top_left.line != other_node_box.top_left.line:
            return False

        return node_box.bottom_right.line == other_node_box.bottom_right.line

    # TODO: Move elsewhere
    def _node_is_on_single_line(self, node):
        """
        :type node: Node
        :rtype: bool
        """
        bounding_box = node.absolute_bounding_box

        return bounding_box.top_left.line == bounding_box.bottom_right.line


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




class CommentTooLongCase:
    def __init__(self, comment_node, line_length_exceeded_context):
        self.comment_node = comment_node  # type: CommentNode
        self.line_length_exceeded_context = line_length_exceeded_context  # type: LineLengthExceededContext


class FileContext:
    def __init__(self, line_number, line_content, source_file_name):
        self.line_number = line_number  # type: int
        self.line_content = line_content  # type: str
        self.source_file_name = source_file_name  # type: str


class LineLengthExceededContext:
    def __init__(self, file_context, source_file_fst):
        self.file_context = file_context  # type: FileContext
        self.source_file_fst = source_file_fst  # type: RedBaron


if __name__ == "__main__":
    filename_1 = "./input_files/single_line_too_long.py"
    filename_2 = "./input_files/comment_after_statement_same_line.py"

    line_length_analyzer = LineLengthAnalyzer()
    line_length_analyzer.add_line_length_exceeded_listener(LineLengthExceededListenerForComments())

    code_analyzer = CodeAnalyzer()
    code_analyzer.add_file_analyzer(line_length_analyzer)
    code_analyzer.analyze_file(filename_2)
