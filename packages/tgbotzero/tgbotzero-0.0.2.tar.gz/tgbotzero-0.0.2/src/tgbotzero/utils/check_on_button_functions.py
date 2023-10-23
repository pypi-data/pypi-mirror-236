import ast
import sys


class AddButtonVisitor(ast.NodeVisitor):
    def __init__(self):
        self.buttons = set()
        super().__init__()

    def visit_Call(self, node):
        # Check if the function being called is named "add_button"
        if isinstance(node.func, ast.Name) and node.func.id == "Button":
            # Check if the function has at least 2 arguments
            if len(node.args) >= 2:
                # The second argument is node.args[1]
                if isinstance(node.args[1], ast.Str):
                    self.buttons.add(node.args[1].s)
        self.generic_visit(node)  # Continue visiting other nodes


def check_on_button_functions(main_module):
    try:
        with open(main_module.__file__, 'r', encoding='utf-8') as f:
            main_source = f.read()
    except Exception as e:
        return
    visitor = AddButtonVisitor()
    visitor.visit(ast.parse(main_source))

    for name in visitor.buttons:
        callback_function_name = f'on_button_{name}'
        callback_function = getattr(main_module, callback_function_name, None)
        if not callback_function:
            sys.stderr.write(f"Необходимо определить функцию {callback_function_name}. Например:\n"
                             f"def {callback_function_name}(data):\n"
                             f"    return 'Нажата кнопка {name}, данные: ' + repr(data)\n")
