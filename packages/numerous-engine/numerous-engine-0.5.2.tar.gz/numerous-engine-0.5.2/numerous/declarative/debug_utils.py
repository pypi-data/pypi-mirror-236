from numerous.declarative.specifications.module import Module


def print_var(engine_var, get_val):
    print(f"{engine_var.path.primary_path}: {get_val(engine_var)}")


def print_all_module(module, get_val):
    if isinstance(module, Module):
        scopes = module.scopes
    else:
        scopes = {}

    for scope_name, scope_spec in scopes.items():

        for name, variable in scope_spec.variables.items():
            engine_var = variable.native_ref
            print_var(engine_var, get_val)

    for items_spec_name, items_spec in module.items_specs.items():

        for module_name, sub_module in items_spec.get_modules(ignore_not_assigned=True).items():
            if isinstance(sub_module, Module):
                print_all_module(sub_module, get_val)


def print_all_variables(module, df):
    def get_val(var):
        return df[var.path.primary_path].tail(1).values[0]

    print_all_module(module, get_val)
