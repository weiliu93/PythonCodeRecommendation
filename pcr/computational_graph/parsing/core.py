import ast
import anytree
import functools
import os
import re


def fetch_attr(name, formatter="{}"):
    def ga(obj=None, name=None):
        return formatter.format(str(getattr(obj, name)))
    return functools.partial(ga, name=name)
    

SPT_NODE = {
    ast.If: "if{test}:{body}{orelse}",
    ast.Assign: "{targets}={value}",
    ast.Yield: "yield#",
    ast.Import: "Import#",
    ast.Attribute: "{value}.{attr}",
    ast.Call: "{func}({args}{keywords})",
    ast.Module: "{body}",
    ast.ClassDef: "{decorator_list}class{name}({bases}):{body}",
    ast.ImportFrom: "from{module}import{names}",
    ast.FunctionDef: "{decorator_list}def{name}({args}):{body},{returns}",
    ast.keyword: "#=#",
    ast.Return: "return#",
    ast.Try: "try:#except:#else:#finally:#",
    ast.With: "with#:#",
    ast.withitem: "withitem{context_expr}as{optional_vars}",
    ast.alias: "alias{name}as{asname}",
    ast.ExceptHandler: "except_handler#as#",
    ast.For: "for#in#:##",
    ast.Global: "global#",
    ast.YieldFrom: "yieldfrom#",
    ast.Nonlocal: "nolocal#",
    ast.Starred: "*#",
    ast.Assert: "assert{test}{msg}",
    ast.Subscript: "{value}[{slice}]",
    ast.ListComp: "[{elt} {generators}]",
    ast.comprehension: "for{target}in{iter}if{ifs}",
    ast.Slice: "[{lower}:{upper}:{step}]",
    ast.Raise: "raise{exc}{cause}",
    ast.While: "while{test}:{body}{orelse}",
    ast.Continue: "continue",
    ast.Pass: "pass",
    ast.Break: "break",
    ast.Delete: "delete#",
    ast.GeneratorExp: "generatorexp{elt}{generators}",
    ast.IfExp: "{body}if{test}{orelse}",
}

TOKEN_NODE = {
    ast.Bytes: fetch_attr('s'),
    ast.Name: fetch_attr('id'),
    ast.Str: fetch_attr('s', '"{}"'),
    ast.Num: fetch_attr('n'),
    ast.NameConstant: fetch_attr('value'),
    ast.arg: fetch_attr('arg'),
}

OPS_MAP = {
    ast.In: "in",
    ast.Lt: "<",
    ast.LtE: "<=",
    ast.Gt: ">",
    ast.GtE: ">=",
    ast.Is: "is",
    ast.Not: "not",
    ast.Eq: "==",
    ast.Add: "+",
    ast.Sub: "-",
    ast.Div: "/",
    ast.Mod: "%",
    ast.Pow: "**",
    ast.Mult: "*",
    ast.NotEq: "!=",
    ast.NotIn: "not_in",
    ast.Not: "not",
    ast.IsNot: "is_not",
    ast.LShift: "<<",
    ast.RShift: ">>",
    ast.BitOr: "|",
    ast.BitAnd: "&",
    ast.Or: "or",
    ast.And: "and",
    ast.BitXor: "^",
    ast.FloorDiv: "//",
    ast.Invert: "~",
    ast.UAdd: "+",
    ast.USub: "-",
}

FIELDS = {}
for k, v in SPT_NODE.items():
    FIELDS[k] = re.findall(r"\{(\w+)\}", v)


class SimplifiedParsedTreeTransformer(ast.NodeTransformer):
    def _produce_sptnode_by_tranforming_fields(self, node, label, fields=None):
        lineno = getattr(node, "lineno", "")
        label_map = {}
        sptnode = SptNode(lineno=lineno)
        fields = node._fields if not fields else fields
        for field in fields:
            if field == "ctx":
                continue
            attr = getattr(node, field)
            if attr is None:
                label_map[field] = ""
                continue
            elif isinstance(attr, list):
                attr_label = "#" * len(attr)
                if attr_label == "":
                    label_map[field] = ""
                    continue
                else:
                    attr_spttkn_node = self._aggregate_nodes(attr, True, label=attr_label, lineno=lineno)
            elif isinstance(attr, str):
                label_map[field] = "#"
                attr_spttkn_node = TokenNode(label=attr, lineno=lineno)
            elif isinstance(attr, int) or isinstance(attr, bool):
                label_map[field] = "#"
                attr_spttkn_node = TokenNode(label=str(attr), lineno=lineno)
            else:
                attr_spttkn_node = self.visit(attr)
            if attr_spttkn_node.label != "" and attr_spttkn_node.label is not None:
                label_map[field] = "#"
                attr_spttkn_node.set_parent(sptnode)
            else:
                label_map[field] = ""
                pass
        label = label.format(**label_map)
        sptnode.update_label(label)
        return sptnode

    def generic_visit(self, node):
        if type(node) in TOKEN_NODE:
            label = TOKEN_NODE[type(node)](obj=node)
            return TokenNode(label=label, lineno=node.lineno)
        elif type(node) in SPT_NODE:
            label = SPT_NODE[type(node)]
            fields = FIELDS[type(node)]
        else:
            # node_type = type(node).__name__.lower()
            # label = node_type + "#" * len(node._fields)
            # print(type(node))
            return SptNode(label="unknown", lineno=node.lineno)
        return self._produce_sptnode_by_tranforming_fields(node, label, fields)

    def _aggregate_nodes(self, nodes, promote_if_one=False, **kwargs):
        if promote_if_one and len(nodes) == 1:
            return self.visit(nodes[0])
        nodes_grp = SptNode(**kwargs)
        for node in nodes:
            spt_node = self.visit(node)
            spt_node.set_parent(nodes_grp)
        return nodes_grp

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_List(self, node):
        return self._aggregate_nodes(node.elts, label="[#]", lineno=node.lineno)

    def visit_Tuple(self, node):
        return self._aggregate_nodes(node.elts, label="(*,)", lineno=node.lineno)

    def visit_Compare(self, node):
        ops_str = ""
        for op in node.ops:
            ops_str += OPS_MAP[type(op)]
        label = "#{}#".format(ops_str)
        compare_sptnode = SptNode(label=label, lineno=node.lineno)

        left_spttkn_node = self.visit(node.left)
        left_spttkn_node.set_parent(compare_sptnode)

        comparators_sptnode = self._aggregate_nodes(node.comparators, True, label="comparators")
        comparators_sptnode.set_parent(compare_sptnode)
        return compare_sptnode

    def visit_BinOp(self, node):
        op_str = OPS_MAP[type(node.op)]
        label = "#{}#".format(op_str)
        binop_sptnode = SptNode(lable=label, lineno=node.lineno)

        left_spttkn_node = self.visit(node.left)
        left_spttkn_node.set_parent(binop_sptnode)

        right_spttkn_node = self.visit(node.right)
        right_spttkn_node.set_parent(binop_sptnode)
        return binop_sptnode
    
    def visit_BoolOp(self, node):
        boolop_sptnode = SptNode(lineno=node.lineno)
        op_str = OPS_MAP[type(node.op)]
        value_labels = []
        for value in node.values:
            value_spttkn_node = self.visit(value)
            value_spttkn_node.set_parent(boolop_sptnode)
            value_labels.append("#")
        boolop_sptnode.update_label(op_str.join(value_labels))
        return boolop_sptnode

    def visit_Index(self, node):
        return self.visit(node.value)

    def visit_arguments(self, astnode):
        '''Parse the arguments format:
        [arg]* + [arg=xx]* + [*args]? + [arg=xx]* + [**kwargs]?
        '''
        arguments_sptnode = SptNode()
        arg_label_part = ['#'] * len(astnode.args)
        arg_label_part = ",".join(arg_label_part)

        reqr_arg_number = len(astnode.args) - len(astnode.defaults)
        reqr_args = astnode.args[:reqr_arg_number]
        deft_args = astnode.args[reqr_arg_number:]

        for reqr_arg_astnode in reqr_args:
            reqr_arg_spttkn_node = self.visit(reqr_arg_astnode)
            reqr_arg_spttkn_node.set_parent(arguments_sptnode)

        for name, default in zip(deft_args, astnode.defaults):
            postn_arg_sptnode = SptNode(label="#=#")
            name_arg_tokennode = self.visit(name)
            name_arg_tokennode.set_parent(postn_arg_sptnode)
            deft_arg_spttkn_node = self.visit(default)
            deft_arg_spttkn_node.set_parent(postn_arg_sptnode)
            postn_arg_sptnode.set_parent(arguments_sptnode)

        vararg_label_part = "*#" if astnode.vararg is not None else ""
        if astnode.vararg is not None:
            vararg_spttkn_node = self.visit(astnode.vararg)
            vararg_spttkn_node.set_parent(arguments_sptnode)

        kwonly_label_part = ["#"] * len(astnode.kwonlyargs)
        kwonly_label_part = ','.join(kwonly_label_part)
        for name, default in zip(astnode.kwonlyargs, astnode.kw_defaults):
            kwonly_arg_sptnode = SptNode(label="#=#")
            name_arg_tokennode = self.visit(name)
            name_arg_tokennode.set_parent(kwonly_arg_sptnode)
            deft_arg_spttkn_node = self.visit(default)
            deft_arg_spttkn_node.set_parent(kwonly_arg_sptnode)
            kwonly_arg_sptnode.set_parent(arguments_sptnode)

        kwarg_label_part = "**#" if astnode.kwarg is not None else ""
        if astnode.kwarg is not None:
            kwarg_sptnode = self.visit(astnode.kwarg)
            kwarg_sptnode.set_parent(arguments_sptnode)

        label_parts = filter(lambda part: part != "", [arg_label_part, vararg_label_part, kwonly_label_part, kwarg_label_part])
        label = ','.join(label_parts)
        arguments_sptnode.update_label(label)
        return arguments_sptnode

    def visit_AugAssign(self, astnode):
        op_str = OPS_MAP[type(astnode.op)]
        label = "#{}=#".format(op_str)
        augassign_sptnode = SptNode(lable=label, lineno=astnode.lineno)

        target_spttkn_node = self.visit(astnode.target)
        target_spttkn_node.set_parent(augassign_sptnode)

        value_spttkn_node = self.visit(astnode.value)
        value_spttkn_node.set_parent(augassign_sptnode)
        return augassign_sptnode

    def visit_UnaryOp(self, astnode):
        op_str = OPS_MAP[type(astnode.op)]
        label = "{}#".format(op_str)
        unaryop_sptnode = SptNode(label=label, lineno=astnode.lineno)
        operand_spttken_node = self.visit(astnode.operand)
        operand_spttken_node.set_parent(unaryop_sptnode)
        return unaryop_sptnode

    def visit_Dict(self, astnode):
        label = "{#}" if astnode.values else "{}"
        dict_sptnode = SptNode(label=label, lineno=astnode.lineno)
        for key_astnode, value_astnode in zip(astnode.keys, astnode.values):
            kvpair_spttknnode = SptNode(label="#=#", lineno=key_astnode.lineno)
            key_spttkn_node = self.visit(key_astnode)
            key_spttkn_node.set_parent(kvpair_spttknnode)
            value_spttkn_node = self.visit(value_astnode)
            value_spttkn_node.set_parent(kvpair_spttknnode)
            kvpair_spttknnode.set_parent(dict_sptnode)
        return dict_sptnode


class SptNode(anytree.NodeMixin):
    def __init__(self, parent=None, label="", **kwargs):
        super(SptNode, self).__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.is_token = False

        self.parent = parent
        self.rank = -1
        self.update_label(label)

    def __str__(self):
        return self.label

    @property
    def label(self):
        return self._label

    def set_parent(self, node):
        self.parent = node
        self.rank = len(node.children)

    def set_children(self, children):
        for rank, child in enumerate(children):
            child.rank = rank + 1
        self.children = children

    def update_label(self, label):
        self._label = label
        lineno = getattr(self, "lineno", "")
        self.name = '{}\nline: {}\n{}'.format(label, lineno, str(id(self))) # used by anytree

    def copy(self):
        node = SptNode(None, label=self.label, name=self.name)
        if hasattr(self, 'copy_from'):
            node.copy_from = self.copy_from
        else:
            node.copy_from = id(self)
        node.name = self.name
        return node


class TokenNode(SptNode):
    def __init__(self, parent=None, label="", **kwargs):
        super(TokenNode, self).__init__(parent=parent, label="", **kwargs)
        self.is_token = True
        self.update_label(label)

    def update_label(self, label):
        self._label = label
        lineno = getattr(self, "lineno", "")
        self.name = '{}\nline: {}\n{}'.format("*|" + label + "|*", lineno, str(id(self))) # used by anytree

    def copy(self):
        node = TokenNode(None, label=self.label, name=self.name, is_token=self.is_token)
        if hasattr(self, 'copy_from'):
            node.copy_from = self.copy_from
        else:
            node.copy_from = id(self)
        node.name = self.name
        return node


class Parser(object):
    @staticmethod
    def parse(code_string):
        '''Use Python AST parse simply.
        Args:
            code_string (String): The code string to be parsed.
        Return:
            root (ast.Module): The AST root.
        '''
        return ast.parse(code_string)

    @staticmethod
    def spt_parse(code_string):
        '''Parse a piece of code.
        Args:
            code_string (String): The code string to be parsed.
        Return:
            root (core.SptNode): The Simplified Parsed Tree root.
        '''
        code_root = ast.parse(code_string)
        return SimplifiedParsedTreeTransformer().visit(code_root)


def simple_example():
    a = '''
a = {
    "b": 1,
    "c": 2,
}
    '''
    path = os.path.dirname(__file__)
    parse_tree = Parser().parse(a)
    root = SimplifiedParsedTreeTransformer().visit(parse_tree)
    from anytree.exporter import DotExporter
    DotExporter(root).to_picture("{}/test_files/test_tree.png".format(path))


def geoipupdate():
    path = os.path.dirname(__file__)
    with open('{}/test_files/geoipupdate.py'.format(path), 'r') as f:
        code = f.read()
        parse_tree = Parser().parse(code)
        root = SimplifiedParsedTreeTransformer().visit(parse_tree)
        from anytree.exporter import DotExporter
        DotExporter(root).to_picture("{}/test_files/geoipupdate.png".format(path))


def ipaddress():
    path = os.path.dirname(__file__)
    with open('{}/test_files/ipaddress.py'.format(path), 'r') as f:
        code = f.read()
        parse_tree = Parser().parse(code)
        root = SimplifiedParsedTreeTransformer().visit(parse_tree)
        from anytree.exporter import DotExporter
        DotExporter(root).to_picture("{}/test_files/ipaddress.png".format(path))


if __name__ == '__main__':
    simple_example()