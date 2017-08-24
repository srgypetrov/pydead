import ast

from .writer import error
from .utils import get_dot_relpath


class PyFile(ast.NodeVisitor):

    def __init__(self, basedir, path):
        self.basedir = basedir
        self.path = path
        self.dot_path = get_dot_relpath(basedir, path)
        self.used = set()
        self.used_here = set()
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
            pathlist = self.dot_path.split('.')[:-ast_node.level]
            if ast_node.level > 1 and not pathlist:
                error(4, [self.path, ast_node.lineno])
            if ast_node.module:
                pathlist.append(ast_node.module)
            return '.'.join(pathlist)
        return ast_node.module

    def process_nodes(self):
        for item in self.ast_used:
            item_list = item.split('.')
            key = item_list.pop(0)
            if key in self.ast_imported:
                value = '.'.join([self.ast_imported[key]] + item_list)
                self.used.add(value)
            else:
                self.used_here.add('{0}.{1}'.format(self.dot_path, item))
        self.defined = [i for i in self.ast_defined if i.path not in self.used_here]

    def parse(self):
        ast_node = self.get_ast_node()
        self.visit(ast_node)
        self.process_nodes()

    def visit(self, ast_node):
        method = 'visit_' + ast_node.__class__.__name__.lower()
        visitor = getattr(self, method, None)
        if visitor is not None:
            visitor(ast_node)
        else:
            return self.generic_visit(ast_node)

    def visit_attribute(self, ast_node):
        if isinstance(ast_node.ctx, ast.Load):
            value = [ast_node.attr]
            while isinstance(ast_node.value, ast.Attribute):
                ast_node = ast_node.value
                value.insert(0, ast_node.attr)
            if isinstance(ast_node, ast.Name) and ast_node.value.id != 'self':
                value.insert(0, ast_node.value.id)
                self.ast_used.add('.'.join(value))

    def visit_classdef(self, ast_node):
        if ast_node.col_offset == 0:
            node = Node(self.dot_path, ast_node, 'class')
            self.ast_defined.add(node)

    def visit_functiondef(self, ast_node):
        if ast_node.col_offset == 0:
            node = Node(self.dot_path, ast_node, 'function')
            self.ast_defined.add(node)

    def visit_import(self, ast_node):
        for item in ast_node.names:
            name = item.asname or item.name
            self.ast_imported[name] = item.name

    def visit_importfrom(self, ast_node):
        module_path = self.get_relpath_from_import(ast_node)
        for item in ast_node.names:
            name = item.asname or item.name
            if name == '*':
                error(2, [ast_node.module, self.dot_path])
            if module_path:
                self.ast_imported[name] = '{0}.{1}'.format(module_path, item.name)
            else:
                self.ast_imported[name] = item.name

    def visit_name(self, ast_node):
        if isinstance(ast_node.ctx, ast.Load):
            self.ast_used.add(ast_node.id)
        else:
            node = Node(self.dot_path, ast_node, 'name')
            self.ast_defined.add(node)


class Node(object):

    def __init__(self, filepath, ast_node, ast_node_type):
        self.name = ast_node.id if ast_node_type == 'name' else ast_node.name
        self.node_type = ast_node_type
        self.line = ast_node.lineno
        self.filepath = filepath
        self.path = '{0}.{1}'.format(filepath, self.name)

    def __str__(self):
        return self.path

    def __repr__(self):
        return '<Node(path={0}, node_type={1}, line={2})>'.format(
            self.path, self.node_type, self.line)
