def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

@singleton
class Memory:
    def __init__(self):
        self.scopes = [{}]  # Global scope
        self.functions = {}
        self.constants = set()

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()

    def set(self, variable_name, value, data_type, is_constant=False):
        self.scopes[-1][variable_name] = (value, data_type)
        if is_constant:
            self.constants.add(variable_name)

    def get(self, variable_name):
        print(f"Getting {variable_name}")  # Debug
        for scope in reversed(self.scopes):
            if variable_name in scope:
                entry = scope[variable_name]
                print(f"Entry: {entry}")  # Debug
                if isinstance(entry, tuple) and isinstance(entry[0], dict):
                    ref_scope, ref_type, ref_var = entry
                    print(f"Resolved to {ref_var}")  # Debug
                    return ref_scope[ref_var][0]
                return entry[0]
    def get_type(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                entry = scope[name]
                if isinstance(entry, tuple) and isinstance(entry[0], dict):
                    return entry[1]
                return entry[1]
        raise ValueError(f"Undefined variable: {name}")

    def is_declared(self, variable_name):
        for scope in reversed(self.scopes):
            if variable_name in scope:
                return True
        return False

    def is_declared_in_current_scope(self, variable_name):
        return variable_name in self.scopes[-1]

    def set_function(self, name, func_info):
        self.functions[name] = func_info
        print(f"Stored function {name}: info={func_info}")

    def get_function(self, name):
        return self.functions.get(name)

    def update(self, variable_name, value, data_type):
        if variable_name in self.constants:
            raise ValueError(f"Cannot assign to constant '{variable_name}'")
        for scope in reversed(self.scopes):
            if variable_name in scope:
                entry = scope[variable_name]
                if isinstance(entry, tuple) and isinstance(entry[0], dict):
                    ref_scope, ref_type, ref_var = entry
                    if ref_var in self.constants:
                        raise ValueError(f"Cannot assign to constant '{ref_var}'")
                    ref_scope[ref_var] = (value, ref_type)
                    return
                else:
                    scope[variable_name] = (value, data_type)
                    return
        raise ValueError(f"Variable '{variable_name}' not declared")

    def get_variable_ref(self, variable_name):
        for scope in reversed(self.scopes):
            if variable_name in scope:
                return (scope, scope[variable_name][1], variable_name)
        raise ValueError(f"Undefined variable: {variable_name}")

    def reset_memory(self):
        self.scopes = [{}]
        self.functions = {}
        self.constants = set()

# Simulate the language program
def simulate_language():
    memory = Memory()

    # Define function 'test'
    func_info = {
        'params': [('y', int), ('x', int)],
        'body': lambda: print(memory.get('y'))  # Simulate print(y)
    }
    memory.set_function('test', func_info)

    # Set global variables
    memory.set('x', 10, int)
    memory.set('y', 19, int)

    # Simulate function call: test(x, y)
    func = memory.get_function('test')
    if func:
        memory.enter_scope()
        param_names = [p[0] for p in func['params']]
        arg_values = [memory.get('x'), memory.get('y')]  # x=10, y=19
        for param_name, arg_value, (_, param_type) in zip(param_names, arg_values, func['params']):
            memory.set(param_name, arg_value, param_type)
        
        func['body']()  # Execute print(y)
        memory.exit_scope()

    # Simulate global print(x)
    print("Global print(x):")
    try:
        value = memory.get('x')  # Should print 10
        print(value)
    except ValueError as e:
        print(f"Error: {e}")

    # Debug: Print global scope
    print("Global scope:", memory.scopes[0])

if __name__ == "__main__":
    simulate_language()