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
        self.constants = set()


    def enter_scope(self):
        """Push a new scope onto the stack (e.g., entering a function or block)."""
        self.scopes.append({})

    def exit_scope(self):
        """Pop the current scope off the stack (e.g., leaving a function or block)."""
        if len(self.scopes) > 1:  # Don’t remove global scope
            self.scopes.pop()

    def set(self, variable_name, value, data_type, is_constant=False):
        """Set the varibale at topmost scope"""
        self.scopes[-1][variable_name] = (value, data_type)
        if is_constant:
            self.constants.add(variable_name)

    def get(self, variable_name):
        for scope in reversed(self.scopes):
            if variable_name in scope:
                entry = scope[variable_name]
                if isinstance(entry, tuple) and isinstance(entry[0], dict):
                    # Resolve variable reference (pass-by-reference)
                    ref_scope, ref_type = entry
                    for var in ref_scope:
                        if ref_scope[var][1] == ref_type:
                            return ref_scope[var][0]
                return entry[0]  # Normal variable or constant
        raise ValueError(f"Undefined variable: {variable_name}")

    def update(self, variable_name, value, data_type):
        if variable_name in self.constants:
            raise ValueError(f"Cannot assign to constant '{variable_name}'")
        for scope in reversed(self.scopes):
            if variable_name in scope:
                entry = scope[variable_name]
                if isinstance(entry, tuple) and isinstance(entry[0], dict):
                    # Update referenced scope (pass-by-reference)
                    ref_scope, ref_type = entry
                    for var in ref_scope:
                        if ref_scope[var][1] == ref_type:
                            ref_scope[var] = (value, ref_type)
                            return
                else:
                    # Update normal variable
                    scope[variable_name] = (value, data_type)
                    return
        raise ValueError(f"Variable '{variable_name}' not declared")

    def is_declared(self, variable_name):
        for scope in reversed(self.scopes):
            if variable_name in scope:
                return True
        return False
    
    def is_declared_in_current_scope(self, variable_name):
        return variable_name in self.scopes[-1]

    def set_function(self, name, body, params=None):
        self.functions[name] = (body, params or [])
        print(f"Stored function {name}: body={body}, params={params}")  # Debug

    def get_function(self, name):
        return self.functions.get(name)
    
    def get_variable_ref(self, variable_name):
        """Return (scope, type) for variable to allow reference updates."""
        for scope in reversed(self.scopes):
            if variable_name in scope:
                return (scope, scope[variable_name][1])
        raise ValueError(f"Undefined variable: {variable_name}")

    def __contains__(self, variable_name):
        return variable_name in self.memory

    def reset_memory(self):
        self.memory = {}
        self.functions = {}
        self.scopes = [{}]
        self.constants = set()


if __name__ == "__main__":
    memory = Memory()
    memory.set(variable_name='a', value=10, data_type=int)
    memory.set(variable_name='b', value="20", data_type=str)
    print(memory)
    print(memory.get(variable_name='b'))