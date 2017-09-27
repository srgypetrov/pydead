import ast

from .writer import error
from .utils import get_dot_relpath


class PyFile(ast.NodeVisitor):

    def __init__(self, basedir, path):
        self.basedir = basedir
        self.path = path
        self.dot_path = get_dot_relpath(basedir, path)
        self.used = set()
        self.ast_used = set()
        self.ast_imported = {}
        self.defined = {
            'class': [],
            'function': [],
            'name': []
        }

    def get_node(self):
        module_string = open(self.path).read()
        try:
            node = ast.parse(module_string, filename=self.path)
        except SyntaxError as e:
            error(1, [self.path, e])
        return node

    def get_relpath_from_import(self, node):
        if node.level != 0:
            pathlist = self.dot_path.split('.')[:node.level]
            if node.level > 1 and not pathlist:
                error(4, [self.path, node.lineno])
            if node.module:
                pathlist.append(node.module)
            return '.'.join(pathlist)
        return node.module

    def process_items(self):
        used_here = set()
        for item in self.ast_used:
            # item_list = item.split('.')
            # key = item_list.pop()
            if item in self.ast_imported:
                # value = '.'.join([self.ast_imported[key]] + item_list)
                self.used.add(self.ast_imported[item])
            else:
                used_here.add('{0}.{1}'.format(self.dot_path, item))

        for name, items in self.defined.items():
            self.defined[name] = [i for i in items if i['path'] not in used_here]

    def parse(self):
        node = self.get_node()
        self.generic_visit(node)
        self.process_items()

    def visit(self, node):
        method = 'visit_{}'.format(node.__class__.__name__.lower())
        visitor = getattr(self, method, None)
        if visitor is not None:
            visitor(node)
        if not isinstance(node, ast.Attribute):
            inner = isinstance(node, (ast.ClassDef, ast.FunctionDef))
            return self.generic_visit(node, inner)

    def generic_visit(self, node, inner=False):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.Name) and inner:
                        self.visit_name(item, inner)
                    elif isinstance(item, ast.AST):
                        self.generic_visit(item, inner) if inner else self.visit(item)
            elif isinstance(value, ast.Name) and inner:
                self.visit_name(value, inner)
            elif isinstance(value, ast.AST):
                self.generic_visit(value, inner) if inner else self.visit(value)

    def visit_attribute(self, node):
        if isinstance(node.ctx, ast.Load):
            value = []
            while isinstance(node, ast.Attribute):
                value.append(node.attr)
                node = node.value
            if isinstance(node, ast.Name) and node.id != 'self':
                value.append(node.id)
                value.reverse()
                # print('\n' + '-' * 30)
                # print('.'.join(value))
                self.ast_used.add('.'.join(value))

    def visit_classdef(self, node):
        if node.col_offset == 0:
            path = '{0}.{1}'.format(self.dot_path, node.name)
            self.defined['class'].append({'path': path, 'node': node})

    def visit_functiondef(self, node):
        if node.col_offset == 0:
            path = '{0}.{1}'.format(self.dot_path, node.name)
            self.defined['function'].append({'path': path, 'node': node})

    def visit_import(self, node):
        for item in node.names:
            name = item.asname or item.name
            self.ast_imported[name] = item.name

    def visit_importfrom(self, node):
        module_path = self.get_relpath_from_import(node)
        for item in node.names:
            name = item.asname or item.name
            if name == '*':
                error(2, [node.module, self.dot_path])
            if module_path:
                self.ast_imported[name] = '{0}.{1}'.format(module_path, item.name)
            else:
                self.ast_imported[name] = item.name

    def visit_name(self, node, inner=False):
        if isinstance(node.ctx, ast.Load):
            self.ast_used.add(node.id)
        elif not inner:
            path = '{0}.{1}'.format(self.dot_path, node.id)
            self.defined['name'].append({'path': path, 'node': node})
