from abc import abstractmethod

import logging

import feedback
from contexts import LineLengthExceededContext
from feedback import FeedbackFactory

NODE_TYPE_COMMENT = 'comment'
NODE_TYPE_ASSIGNMENT = 'assignment'


class LineLengthExceededListener:
    def __init__(self):
        pass

    @abstractmethod
    def on_line_length_exceeded(self, context):
        """
        :type context: LineLengthExceededContext 
        """
        raise NotImplementedError("Method on_line_length_exceeded must be implemented")


class LineLengthViolationCounter(LineLengthExceededListener):
    def __init__(self):
        LineLengthExceededListener.__init__(self)
        self._line_length_violations = 0
        self._line_length_violations_per_file = {}  # type: dict[str, int]

    def on_line_length_exceeded(self, context):
        """
        :type context: LineLengthExceededContext 
        """
        self._line_length_violations += 1
        self._store_violation_for_file(context.file_context.source_file_name)

    def _store_violation_for_file(self, source_file_name):
        if source_file_name not in self._line_length_violations_per_file:
            self._line_length_violations_per_file[source_file_name] = 1
        else:
            self._line_length_violations_per_file[source_file_name] += 1

    def get_total_violation_count(self):
        """
        :rtype: int 
        """
        return self._line_length_violations

    def get_violation_count_for_file(self, file_name):
        """
        :type file_name: str
        :rtype: int 
        """
        if file_name not in self._line_length_violations_per_file:
            return 0

        return self._line_length_violations_per_file[file_name]

    def get_violation_count_per_file(self):
        """
        :rtype: dict[str, int] 
        """
        return self._line_length_violations_per_file


class LineLengthViolationExtractVariableListener(LineLengthExceededListener):
    def __init__(self):
        LineLengthExceededListener.__init__(self)
        self._feedback_factory = FeedbackFactory()

    def on_line_length_exceeded(self, context):
        """
        :type context: LineLengthExceededContext 
        """
        line_number = context.file_context.line_number
        try:
            first_node_on_line = context.source_file_fst.at(line_number)
        except IndexError:
            # Sometimes RedBaron doesn't understand multi-line strings correctly
            file_name = context.file_context.source_file_name
            logging.warn('RedBaron failed to find a node on line {} in file {}'.format(line_number, file_name))
            return

        if self._count_all_binops_on_same_line(first_node_on_line) > 4:
            feedback.emit(self._feedback_factory.extract_variable(context.file_context))

    def _count_all_binops_on_same_line(self, node):
        return len(self._find_all_binops_on_same_line(node))

    def _find_all_binops_on_same_line(self, node):
        """
        :type node: Node 
        :rtype: list[Node] 
        """
        binop_nodes_on_same_line = []
        binop_nodes = node.find_all('BinaryOperatorNode')

        for binop_node in binop_nodes:
            if _nodes_are_on_same_line(node, binop_node):
                binop_nodes_on_same_line.append(binop_node)

        return binop_nodes_on_same_line


class LineLengthExceededListenerForComments(LineLengthExceededListener):
    def __init__(self):
        LineLengthExceededListener.__init__(self)
        self._feedback_factory = FeedbackFactory()

    def on_line_length_exceeded(self, context):
        """
        :type context: LineLengthExceededContext 
        """
        # TODO: Find a way to find comments after if statements (same line)
        line_number = context.file_context.line_number
        # TODO: Remove code duplication in other listeners
        try:
            first_node_on_line = context.source_file_fst.at(line_number)
        except IndexError:
            # Sometimes RedBaron doesn't understand multi-line strings correctly
            file_name = context.file_context.source_file_name
            logging.warn('RedBaron failed to find a node on line {} in file {}'.format(line_number, file_name))
            return

        self._detect_comments(first_node_on_line, context)

    def _detect_comments(self, node, context):
        """
        :type node: Node 
        :type context: LineLengthExceededContext
        """
        nodes_on_same_line = _get_nodes_on_same_line(node)

        if len(nodes_on_same_line) == 1 and nodes_on_same_line[0].type == NODE_TYPE_COMMENT:
            comment_feedback = self._feedback_factory.comment(context.file_context)
            feedback.emit(comment_feedback)
        elif len(nodes_on_same_line) > 1 and nodes_on_same_line[-1].type == NODE_TYPE_COMMENT:
            comment_feedback = self._feedback_factory.comment_after_statement(context.file_context)
            feedback.emit(comment_feedback)


# TODO: Move elsewhere
def _get_nodes_on_same_line(node):
    """
    :type node: Node 
    :rtype: list[Node] 
    """
    nodes_on_same_line = []
    current_node = node

    while _nodes_are_on_same_line(node, current_node):
        nodes_on_same_line.append(current_node)

        tmp_node = current_node.next
        if not tmp_node:
            tmp_node = current_node.next_intuitive

        current_node = tmp_node

    return nodes_on_same_line


# TODO: Move elsewhere
def _nodes_are_on_same_line(node, other_node):
    """
    :type node: Node 
    :type other_node: Node 
    :rtype: bool 
    """
    if not node or not other_node:
        return False

    if not _node_is_on_single_line(node) or not _node_is_on_single_line(other_node):
        return False

    node_box = node.absolute_bounding_box
    other_node_box = other_node.absolute_bounding_box

    if node_box.top_left.line != other_node_box.top_left.line:
        return False

    return node_box.bottom_right.line == other_node_box.bottom_right.line

# TODO: Move elsewhere
def _node_is_on_single_line(node):
    """
    :type node: Node
    :rtype: bool
    """
    bounding_box = node.absolute_bounding_box

    return bounding_box.top_left.line == bounding_box.bottom_right.line
