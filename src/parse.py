import ast

from .writer import error
from .utils import get_dot_relpath


class PyFile(object):

    def __init__(self, basedir, path):
        self.path = path
        self.dot_path = get_dot_relpath(basedir, path)
        self.used = set()
        self.ast_used = []
        self.ast_imported = {}
        self.defined = {
            'class': [],
            'function': [],
            'name': []
        }

    def generic_visit(self, node, inner=False):
        for _, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item, inner)
            elif isinstance(value, ast.AST):
                self.visit(value, inner)

    def get_node(self):
        module_string = open(self.path).read()
        try:
            node = ast.parse(module_string, filename=self.path)
        except SyntaxError as e:
            error(1, [self.path, e])
        return node

    def get_relpath_from_import(self, node):
        if node.level != 0:
            splitted_dot_path = self.dot_path.split('.')
            if node.level > len(splitted_dot_path):
                error(4, [self.path, node.lineno])
            pathlist = splitted_dot_path[:-node.level]
            if node.module:
                pathlist.append(node.module)
            return '.'.join(pathlist)
        return node.module

    def parse(self):
        node = self.get_node()
        self.generic_visit(node)
        self.process_items()

    def process_items(self):
        used_here = set()
        for item in self.ast_used:
            if isinstance(item, list):
                import_path, key, key_list = None, None, []
                while item:
                    if import_path is not None:
                        import_path = '.'.join((import_path, item.pop()))
                        self.used.add(import_path)
                    else:
                        key = '.'.join(filter(None, (key, item.pop())))
                        key_list.append('.'.join((self.dot_path, key)))
                        if key in self.ast_imported:
                            import_path = self.ast_imported[key]
                            self.used.add(import_path)
                if import_path is None:
                    used_here.update(key_list)
            else:
                if item in self.ast_imported:
                    self.used.add(self.ast_imported[item])
                else:
                    used_here.add('.'.join((self.dot_path, item)))

        for name, items in self.defined.items():
            self.defined[name] = [i for i in items if i['path'] not in used_here]

    def visit(self, node, inner=False):
        method = 'visit_{}'.format(node.__class__.__name__.lower())
        visitor = getattr(self, method, None)
        if visitor is not None:
            visitor(node, inner)
        if not isinstance(node, ast.Attribute):
            inner = isinstance(node, (ast.ClassDef, ast.FunctionDef)) or inner
            return self.generic_visit(node, inner)

    def visit_attribute(self, node, *args):
        if isinstance(node.ctx, ast.Load):
            value = []
            while isinstance(node, ast.Attribute):
                value.append(node.attr)
                node = node.value
            if isinstance(node, ast.Name) and node.id != 'self':
                value.append(node.id)
                self.ast_used.append(value)

    def visit_classdef(self, node, *args):
        if node.col_offset == 0:
            path = '.'.join((self.dot_path, node.name))
            self.defined['class'].append({'path': path, 'node': node})

    def visit_functiondef(self, node, *args):
        if node.col_offset == 0:
            path = '.'.join((self.dot_path, node.name))
            self.defined['function'].append({'path': path, 'node': node})

    def visit_import(self, node, *args):
        for item in node.names:
            name = item.asname or item.name
            self.ast_imported[name] = item.name

    def visit_importfrom(self, node, *args):
        module_path = self.get_relpath_from_import(node)
        for item in node.names:
            name = item.asname or item.name
            if name == '*':
                error(2, [node.module, self.dot_path])
            if module_path:
                self.ast_imported[name] = '.'.join((module_path, item.name))
            else:
                self.ast_imported[name] = item.name

    def visit_name(self, node, inner=False):
        if isinstance(node.ctx, ast.Load):
            self.ast_used.append(node.id)
        elif not inner:
            path = '.'.join((self.dot_path, node.id))
            self.defined['name'].append({'path': path, 'node': node})
