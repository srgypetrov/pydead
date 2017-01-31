import ast

from .utils import ParsedItem, error, get_dot_relpath


class PyParser(ast.NodeVisitor):

    def reset(self, path):
        self.imported = {}
        self.defined = set()
        self.used = set()
        self.class_child_names = set()
        self.relpath = get_dot_relpath(path)

    def parse(self, path):
        self.reset(path)
        ast_node = self.get_ast_node(path)
        self.visit(ast_node)
        return self.prepare_results()

    @staticmethod
    def get_ast_node(path):
        module_string = open(path).read()
        try:
            node = ast.parse(module_string, filename=path)
        except SyntaxError as e:
            error(1, [path, e])
        return node

    def prepare_results(self):
        imported_and_used, defined_and_used = self.group_used_items()
        defined_and_used = self.remove_class_child_names(defined_and_used)
        return {
            'defined_objects': self.defined - defined_and_used,
            'used_objects': imported_and_used
        }

    def group_used_items(self):
        imported, defined = set(), list()
        for item in self.used:
            if item.node == 'attribute':
                if item.module in self.imported:
                    imported.add('{0}.{1}'.format(self.imported[item.module], item.name))
                    continue
            if item.name in self.imported:
                imported.add(self.imported[item.name])
            else:
                defined.append(item)
        return imported, defined

    def remove_class_child_names(self, names):
        used = set()
        for name in names:
            if '{}_{}'.format(name.name, name.line) not in self.class_child_names:
                used.add(name)
        return used

    def get_relpath_from_import(self, node):
        if node.level != 0:
            pathlist = self.relpath.split('.')[:-node.level]
            if node.module:
                pathlist.append(node.module)
            return '.'.join(pathlist)
        return node.module

    def get_item(self, node, node_type, module=None):
        name = self.get_name_value(node)
        node_path = self.get_node_path(name)
        return ParsedItem(node_path, name, self.relpath, node_type, node.lineno, module)

    def get_node_path(self, name):
        return '{0}.{1}'.format(self.relpath, name)

    @staticmethod
    def get_name_value(node):
        name = getattr(node, 'name', None)
        node_id = getattr(node, 'id', None)
        attr = getattr(node, 'attr', None)
        return name or node_id or attr

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__.lower()
        visitor = getattr(self, method, None)
        if visitor is not None:
            visitor(node)
        return self.generic_visit(node)

    def visit_classdef(self, node):
        if node.col_offset == 0:
            self.defined.add(self.get_item(node, 'class'))
            for child in ast.walk(node):
                if isinstance(child, ast.Name) and child.id == node.name:
                    self.class_child_names.add('{}_{}'.format(child.id, child.lineno))

    def visit_attribute(self, node):
        if isinstance(node.ctx, ast.Load) and isinstance(node.value, ast.Name):
            if node.value.id != 'self':
                self.used.add(self.get_item(node, 'attribute', node.value.id))

    def visit_functiondef(self, node):
        if node.col_offset == 0:
            self.defined.add(self.get_item(node, 'function'))

    def visit_name(self, node):
        self.used.add(self.get_item(node, 'name'))

    def visit_import(self, node):
        for item in node.names:
            name = item.asname or item.name
            self.imported[name] = name

    def visit_importfrom(self, node):
        module_path = self.get_relpath_from_import(node)
        for item in node.names:
            name = item.asname or item.name
            if name == '*':
                error(2, [node.module, self.relpath])
            self.imported[name] = '{0}.{1}'.format(module_path, item.name)

py_parser = PyParser()
