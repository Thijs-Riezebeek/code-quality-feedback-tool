from abc import abstractmethod

import logging

from cases import LineLengthExceededCase, CaseType
from contexts import LineLengthExceededContext

NODE_TYPE_COMMENT = 'comment'


class LineLengthExceededListener:
    def __init__(self):
        pass

    @abstractmethod
    def on_line_length_exceeded(self, context):
        """
        :type context: LineLengthExceededContext 
        """
        raise NotImplementedError("Method on_line_length_exceeded must be implemented")


class LineLengthExceededListenerForComments(LineLengthExceededListener):
    def __init__(self):
        LineLengthExceededListener.__init__(self)

    def on_line_length_exceeded(self, context):
        """
        :type context: LineLengthExceededContext 
        """
        # TODO: Find a way to find comments after if statements (same line)
        line_number = context.file_context.line_number
        try:
            first_node_on_line = context.source_file_fst.at(line_number)
        except IndexError:
            # Sometimes RedBaron doesn't understand multi-line strings correctly
            file_name = context.file_context.source_file_name
            logging.warn('RedBaron failed to find a node on line {} in file {}'.format(line_number, file_name))
            return

        comment_too_long_case = self.find_comment_too_long_case_on_line(first_node_on_line, context)

        if comment_too_long_case:
            pass

    def find_comment_too_long_case_on_line(self, node, context):
        """
        :type node: Node
        :type context: LineLengthExceededContext 
        :rtype: LineLengthExceededCase 
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
