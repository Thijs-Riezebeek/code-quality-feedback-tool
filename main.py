# coding=utf-8
from baron import ParsingError
from redbaron import RedBaron, Node, CommentNode
import abc
import os

# TODO: requirements.txt/setup.py for pip
from contexts import LineLengthExceededContext, FileContext
from listeners import LineLengthExceededListenerForComments


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

        self._line_length_exceeded_listeners = []  # type: list[LineLengthExceededListenerForComments]

    def analyze(self, file_path, file_contents):
        source_file_fst = None

        for line_number, line_content in self._yield_all_lengthy_lines(file_path):
            if source_file_fst is None:
                try:
                    source_file_fst = RedBaron(file_contents)
                except ParsingError as parse_error:
                    # Should probably be a return
                    continue

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


if __name__ == "__main__":
    filename_1 = "./input_files/single_line_too_long.py"
    filename_2 = "./input_files/comment_after_statement_same_line.py"

    line_length_analyzer = LineLengthAnalyzer()
    line_length_analyzer.add_line_length_exceeded_listener(LineLengthExceededListenerForComments())

    code_analyzer = CodeAnalyzer()
    code_analyzer.add_file_analyzer(line_length_analyzer)

    # code_analyzer.analyze_file(filename_1)
    # code_analyzer.analyze_file(filename_2)
    code_analyzer.analyze_directory("./input_files/students/ProgNS2014/5679699")
