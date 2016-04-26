import importnp
import imp
import inspect

function_path = "importnp.py"
module_name = inspect.getmodulename(function_path)
print module_name
module_file, module_pathname, module_description = imp.find_module(module_name)
module = imp.load_module(module_name, module_file, module_pathname, module_description)
print module
function = getattr(module, "print_env")
print inspect.getsource(function)
