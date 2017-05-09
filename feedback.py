from abc import abstractmethod
from contexts import FileContext


class Feedback:
    def __init__(self, text, line_number, source_file_name):
        """
        :type text: str 
        :type line_number: int 
        :type source_file_name: str 
        """
        self._text = text
        self._line_number = line_number
        self._source_file_name = source_file_name

    def get_text(self):
        return self._text

    def get_line_number(self):
        return self._line_number

    def get_source_file_name(self):
        return self._source_file_name


class FeedbackFactory:
    def __init__(self):
        pass

    def comment(self, file_context):
        """
        :type file_context: FileContext
        :rtype: Feedback 
        """
        return Feedback(
            "Comment exceeds the line length",
            file_context.line_number,
            file_context.source_file_name
        )


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
