import ast

from .writer import error
from .utils import get_dot_relpath


class PyFile(ast.NodeVisitor):

    def __init__(self, basedir, path):
        self.basedir = basedir
        self.path = path
        self.dot_path = get_dot_relpath(basedir, path)
        self.class_child_names = set()
        self.ast_used = set()
        self.ast_defined = set()
        self.ast_imported = dict()

    def get_ast_node(self):
        module_string = open(self.path).read()
        try:
            ast_node = ast.parse(module_string, filename=self.path)
        except SyntaxError as e:
            error(1, [self.path, e])
        return ast_node

    def get_relpath_from_import(self, ast_node):
        if ast_node.level != 0:
            pathlist = self.dot_path.split('.')[:ast_node.level]
            if ast_node.module:
                pathlist.append(ast_node.module)
            return '.'.join(pathlist)
        return ast_node.module

    def process_nodes(self):
        self.used, self.used_here = set(), set()
        for node in self.ast_used:
            if node.module is not None and node.module in self.ast_imported:
                self.used.add('{0}.{1}'.format(self.ast_imported[node.module], node.name))
            elif node.name in self.ast_imported:
                self.used.add(self.ast_imported[node.name])
            else:
                self.used_here.add(node)

        for node in self.used_here.copy():
            if '{}_{}'.format(node.name, node.line) in self.class_child_names:
                self.used_here.remove(node)
        self.defined = self.ast_defined - self.used_here

    def parse(self):
        ast_node = self.get_ast_node()
        self.visit(ast_node)
        self.process_nodes()

    def visit(self, ast_node):
        method = 'visit_' + ast_node.__class__.__name__.lower()
        visitor = getattr(self, method, None)
        if visitor is not None:
            visitor(ast_node)
        return self.generic_visit(ast_node)

    def visit_attribute(self, ast_node):
        if isinstance(ast_node.ctx, ast.Load) and isinstance(ast_node.value, ast.Name):
            if ast_node.value.id != 'self':
                node = Node(self.dot_path, ast_node, 'attribute')
                self.ast_used.add(node)

    def visit_classdef(self, ast_node):
        if ast_node.col_offset == 0:
            node = Node(self.dot_path, ast_node, 'class')
            self.ast_defined.add(node)
            for child in ast.walk(ast_node):
                if isinstance(child, ast.Name) and child.id == ast_node.name:
                    self.class_child_names.add('{}_{}'.format(child.id, child.lineno))

    def visit_functiondef(self, ast_node):
        if ast_node.col_offset == 0:
            node = Node(self.dot_path, ast_node, 'function')
            self.ast_defined.add(node)

    def visit_import(self, ast_node):
        for item in ast_node.names:
            name = item.asname or item.name
            self.ast_imported[name] = name

    def visit_importfrom(self, ast_node):
        module_path = self.get_relpath_from_import(ast_node)
        for item in ast_node.names:
            name = item.asname or item.name
            if name == '*':
                error(2, [ast_node.module, self.dot_path])
            self.ast_imported[name] = '{0}.{1}'.format(module_path, item.name)

    def visit_name(self, ast_node):
        node = Node(self.dot_path, ast_node, 'name')
        self.ast_used.add(node)


class Node(object):

    def __init__(self, filepath, ast_node, ast_node_name):
        self.name = self.get_name_value(ast_node)
        self.path = '{0}.{1}'.format(filepath, self.name)
        self.filepath = filepath
        self.node_name = ast_node_name
        self.line = ast_node.lineno
        self.module = self.get_module(ast_node, ast_node_name)

    def __str__(self):
        return self.path

    def __repr__(self):
        return '<Node(path={0}, node_name={1}, line={2})>'.format(
            self.path, self.node_name, self.line)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.path == other.path
        if isinstance(other, str):
            return self.path == other
        return False

    def __hash__(self):
        return hash(self.path)

    @staticmethod
    def get_name_value(ast_node):
        name = getattr(ast_node, 'name', None)
        node_id = getattr(ast_node, 'id', None)
        attr = getattr(ast_node, 'attr', None)
        return name or node_id or attr

    def get_module(self, ast_node, ast_node_name):
        if ast_node_name == 'attribute':
            return ast_node.value.id
        return None
