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
        # Stack of scopes: each scope is a dict of {var_name: (value, data_type)}
        self.scopes = [{}]  # Start with global scope
        # Separate storage for functions
        self.functions = {}
        self.memory = {}

    def enter_scope(self):
        """Push a new scope onto the stack (e.g., entering a function or block)."""
        self.scopes.append({})

    def exit_scope(self):
        """Pop the current scope off the stack (e.g., leaving a function or block)."""
        if len(self.scopes) > 1:  # Don’t remove global scope
            self.scopes.pop()

    def set(self, variable_name, value, data_type):
        """Set a variable in the current (topmost) scope."""
        self.scopes[-1][variable_name] = (value, data_type)

    def get(self, variable_name):
        """Look up a variable, starting from the current scope and moving outward."""
        for scope in reversed(self.scopes):  # Check local scope first, then global
            if variable_name in scope:
                return scope[variable_name][0]  # Return the value
        raise ValueError(f"Undefined variable: {variable_name}")

    def is_declared(self, variable_name):
        """Check if a variable is declared in the current scope."""
        return variable_name in self.scopes[-1]

    def set_function(self, function_name, body):
        """Store a function in the global scope."""
        self.functions[function_name] = body

    def get_function(self, function_name):
        """Retrieve a function’s body."""
        return self.functions.get(function_name)

    def __contains__(self, variable_name):
        return variable_name in self.memory

    def reset_memory(self):
        self.memory = {}
        self.functions = {}
        self.scopes = [{}]


if __name__ == "__main__":
    memory = Memory()
    memory.set(variable_name='a', value=10, data_type=int)
    memory.set(variable_name='b', value="20", data_type=str)
    print(memory)
    print(memory.get(variable_name='b'))