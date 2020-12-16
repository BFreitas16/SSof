import itertools
from Node import Node, search_for_node
from Util import load_json, get_contained, remove_duplicates, indices

# strategies -> represents all the supported strategies for flow analysis
strategies = {
    "Literal" : "literal_strategy", "Identifier" : "identifier_strategy", "MemberExpression" : "member_expression_strategy",
    "ExpressionStatement" : "expression_statement_strategy", "AssignmentExpression" : "assignment_expression_strategy",
    "BinaryExpression" : "binary_expression_strategy", "LogicalExpression" : "binary_expression_strategy",
    "CallExpression" : "call_expression_strategy", "IfStatement" : "conditional_expression_strategy",
    "ConditionalExpression" : "conditional_expression_strategy", "WhileStatement" : "while_statement_strategy",
    "BlockStatement" : "block_statement_strategy", "VariableDeclaration" : "variable_declaration_strategy",
    "VariableDeclarator" : "variable_declarator_strategy", "FunctionDeclaration" : "function_declaration_strategy"
}

class ProgramParser:
    """
    A class used to parse the program. It will build a graph and then evaluate the flow.
    The flow is source -> sink and can have sanitizers in between.

    Attributes
    ----------
    program_json
        represents the json with the program flow
    patterns_json
        represents the json with the patterns to search
    flow_graph
        represents the graph dynamically built of the program's flow
    """


    def __init__(self, program_path, patterns_path):
        self.program_json = load_json(program_path)
        self.patterns_json = load_json(patterns_path)
        self.flow_graph = Node('root')


    def evaluate_flows(self):
        """ 
        A function that evaluate the flows (source -> sink) in a graph
        Searches for source and sinks and tells when a sanitizer is found in the flow
        """
        # Find all possible paths in nodes
        paths = self.flow_graph.paths()
        possible_vulns = []

        for path, pattern in list(itertools.product(paths, self.patterns_json)):
            # Get all sources, sinks and sanitizers in the path
            sources_in_path = get_contained(path, pattern['sources'])
            sinks_in_path = get_contained(path, pattern['sinks'])
            sanitizers_in_path = get_contained(path, pattern['sanitizers'])

            for source, sink in list(itertools.product(sources_in_path, sinks_in_path)):
                # Get all sources and sinks indexes
                source_indexes = [i for i, x in enumerate(path) if x == source]
                sink_indexes = [i for i, x in enumerate(path) if x == sink]

                # Get all the valid pairs of source -> sink
                source_sink_pairs = self.__flow_pairs(source_indexes, sink_indexes)

                # Get all the sanitizers between the source -> sink pairs
                sanitizers_in_between = self.__valid_sanitizers(
                    sanitizers_in_path, path, source_sink_pairs)

                for (source_index, sink_index) in source_sink_pairs:
                    vuln = {
                        "vulnerability": pattern['vulnerability'],
                        "source": path[source_index],
                        "sink": path[sink_index],
                        "sanitizer": sanitizers_in_between
                    }
                    if vuln not in possible_vulns:
                        possible_vulns.append(vuln)

        # Remove duplicates (same path, same vuln) (hopefully)
        # possible_vulns = remove_duplicates(possible_vulns)

        return possible_vulns


    def __right_to_left_op(self, left, right):
        """ A function that appends each of nodes on the left as children of all the right ones """
        # TODO:
        # Create sub-graph for 'if' option
        # Return the sub-graph
        # find what to do with that sub-graphs

        if not isinstance(left, list):
            left = [left]

        if not isinstance(right, list):
            right = [right]

        left_nodes = []  # List of all left nodes
        for left_token in left:
            left_node = search_for_node(self.flow_graph, left_token)
            if not left_node:
                left_node = Node(left_token)
            left_nodes.append(left_node)

        for token in right:
            # get the node with the token
            right_node = search_for_node(self.flow_graph, token)
            if not right_node:  # if it doesnt exist create a new one
                right_node = Node(token)

            for left_node in left_nodes:
                # make the left token a child of the right one
                right_node.add_child(left_node)

            # if the right node has no parent, it becomes a child of root
            if not right_node.has_parents():
                self.flow_graph.add_child(right_node)


    def build_graph(self):
        """ A function that builds a flow graph """
        return self.__build_graph_aux(self.program_json['body'])


    def __build_graph_aux(self, curr_tree):
        """ 
        An auxiliar function to build a flow graph 
        
        Parameters
        ----------
        curr_tree -> graph
            represents the current sub-graph
        """
        if curr_tree is None:
            return []

        if isinstance(curr_tree, list):
            return self.__build_graph_from_list_aux(curr_tree)

        # Call the indicated strategy
        strategy = strategies[curr_tree['type']]
        if strategy is not None:
            return getattr(self, strategy)(curr_tree)
        else: # e.g BreakStatement
            return []


    def __build_graph_from_list_aux(self, curr_tree):
        """ A function that searches in a element that is a list """
        result_list = []
        for el in curr_tree:
            result = self.__build_graph_aux(el)
            if isinstance(result, list):
                result_list += result
            else:
                result_list.append(result)
        return result_list

    
    def __flow_pairs(self, source_indexes, sink_indexes):
        """ A function that returns the valid flow pairs """
        return [(x, y) for x in source_indexes for y in sink_indexes if x < y]

    
    def __valid_sanitizers(self, sanitizers_in_path, path, pairs):
        """ A function that returns all the valid sanitizers between source-sink pairs """
        result = []
        for sanitizer in sanitizers_in_path:
            index = path.index(sanitizer)
            for (source, sink) in pairs:
                if source < index < sink and sanitizer not in result:
                    result.append(sanitizer)

        return result



    ## ========================= ##
    ##     Strategies
    ## ========================= ##


    def literal_strategy(self, curr_tree):
        return curr_tree['value']

    def identifier_strategy(self, curr_tree):
        return curr_tree['name']

    def member_expression_strategy(self, curr_tree):
        return self.__build_graph_aux(curr_tree['object']) + "." + self.__build_graph_aux(curr_tree['property'])

    def expression_statement_strategy(self, curr_tree):
        return self.__build_graph_aux(curr_tree['expression'])

    def assignment_expression_strategy(self, curr_tree):
        left = str(self.__build_graph_aux(curr_tree['left']))
        right = self.__build_graph_aux(curr_tree['right'])

        self.__right_to_left_op(
            left, right if isinstance(right, list) else [right])

        return [left]

    def binary_expression_strategy(self, curr_tree):
        left = self.__build_graph_aux(curr_tree['left'])
        right = self.__build_graph_aux(curr_tree['right'])
        if not isinstance(left, list):
            left = [left]

        if not isinstance(right, list):
            right = [right]

        return left + right

    def call_expression_strategy(self, curr_tree):
        c_name = self.__build_graph_aux(curr_tree['callee'])
        args = self.__build_graph_aux(curr_tree['arguments'])
        if args is None:  # if there are no arguments
            args = []

        self.__right_to_left_op(c_name, args)

        return c_name

    def conditional_expression_strategy(self, curr_tree):
        test = self.__build_graph_aux(curr_tree['test'])
        consequent = self.__build_graph_aux(curr_tree['consequent'])
        alternate = self.__build_graph_aux(curr_tree['alternate'])

        self.__right_to_left_op(consequent, test)
        self.__right_to_left_op(alternate, test)

        return [consequent, alternate]

    def while_statement_strategy(self, curr_tree):
        test = self.__build_graph_aux(curr_tree['test'])
        body = self.__build_graph_aux(curr_tree['body'])

        self.__right_to_left_op(body, test)

    def block_statement_strategy(self, curr_tree):
        return self.__build_graph_aux(curr_tree['body'])

    def variable_declaration_strategy(self, curr_tree):
        return self.__build_graph_aux(curr_tree['declarations'])

    def variable_declarator_strategy(self, curr_tree):
        var_id = self.__build_graph_aux(curr_tree['id'])
        init = self.__build_graph_aux(curr_tree['init'])

        self.__right_to_left_op(var_id, init)

    def function_declaration_strategy(self, curr_tree):
        func_id = self.__build_graph_aux(curr_tree['id'])
        args = self.__build_graph_aux(curr_tree['params'])
        if args is None:  # if there are no arguments
            args = []

        self.__right_to_left_op(func_id, args)

        return self.__build_graph_aux(curr_tree['body'])

