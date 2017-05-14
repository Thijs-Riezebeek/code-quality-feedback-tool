from abc import abstractmethod
from contexts import FileContext


class Feedback:
    def __init__(self, text, line_number, source_file_name, code):
        """
        :type text: str 
        :type line_number: int 
        :type source_file_name: str 
        :type code: str 
        """
        self._text = text
        self._line_number = line_number
        self._source_file_name = source_file_name
        self._code = code

    def get_text(self):
        return self._text

    def get_line_number(self):
        return self._line_number

    def get_source_file_name(self):
        return self._source_file_name

    def get_code(self):
        return self._code


_feedback_texts = {
    "comment": "Try splitting your comment into multiple lines so that it doesn't exceed the line length limit.",
    "comment_after_statement": "Try placing your comment above the relevant line to prevent exceeding the line length limit",
    "extract_variable": "This line contains a lot of expressions. Storing the results in a variable with a descriptive name will increase the readability."
}


class FeedbackFactory:
    def __init__(self):
        pass

    def comment(self, file_context):
        """
        :type file_context: FileContext
        :rtype: Feedback 
        """
        return self._feedback_from_file_context(_feedback_texts["comment"], file_context)

    def comment_after_statement(self, file_context):
        """
        :type file_context: FileContext
        :rtype: Feedback 
        """
        return self._feedback_from_file_context(_feedback_texts["comment_after_statement"], file_context)

    def extract_variable(self, file_context):
        """
        :type file_context: FileContext
        :rtype: Feedback 
        """
        return self._feedback_from_file_context(_feedback_texts["extract_variable"], file_context)

    def _feedback_from_file_context(self, text, file_context):
        """
        :type file_context: FileContext
        :rtype: Feedback 
        """
        return Feedback(text, file_context.line_number, file_context.source_file_name, file_context.line_content)


listeners = []  # type: list[FeedbackListener]


def listen(listener):
    """
    :type listener: FeedbackListener 
    """
    listeners.append(listener)


def emit(feedback):
    """
    :type feedback: Feedback 
    """
    for listener in listeners:
        listener.on_feedback(feedback)


class FeedbackListener:
    def __init__(self):
        pass

    @abstractmethod
    def on_feedback(self, feedback):
        """
        :type feedback: Feedback 
        """
        raise NotImplementedError('method on_feedback must be implemented by listener')


class FeedbackCollector(FeedbackListener):
    def __init__(self):
        FeedbackListener.__init__(self)
        self._feedback = []  # type: list[Feedback]
        self._feedback_per_file = {}  # type: dict[str, list[Feedback]]

    def on_feedback(self, feedback):
        """
        :type feedback: Feedback 
        """
        self._feedback.append(feedback)
        self._store_feedback_per_file(feedback)

    def _store_feedback_per_file(self, feedback):
        """
        :type feedback: Feedback 
        """
        file_name = feedback.get_source_file_name()
        path_components = file_name.split('/')
        last_three_path_components = path_components[-3:]

        if len(last_three_path_components) < len(path_components):
            file_name = ".../" + "/".join(last_three_path_components)

        if file_name not in self._feedback_per_file:
            self._feedback_per_file[file_name] = [feedback]
        else:
            self._feedback_per_file[file_name].append(feedback)

    def get_feedback(self):
        """
        :rtype: list[Feedback] 
        """
        return self._feedback

    def get_feedback_per_file(self):
        """
        :rtype: dict[str, list[Feedback]]
        """
        return self._feedback_per_file

    def get_feedback_for_file(self, file_name):
        """
        :type file_name: str
        :rtype: Feedback | None 
        """
        if file_name not in self._feedback_per_file:
            return None

        return self._feedback_per_file[file_name]
