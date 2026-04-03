import os
import importlib
from Utils.utils_py import add_module_to_config, init_config

def init_mod_config(config, shared_context, func):
    global_config = init_config()
    shared_context["logger"].debug(f"Module config load")
    if config["name"] in global_config["modules"].keys():
        shared_context["logger"].info(f"Module already exists in config")
    else:
        global_config = add_module_to_config(config['name'], global_config, config)
    shared_context["logger"].info(f"[{config['name']}] Module config loaded")
    shared_context["logger"].info(f"Init Scheduler...")
    scheduler_ut = shared_context["sheduler_util"]
    scheduler_ut.schedule_from_config(global_config["modules"][config["name"]], func)

async def init_modules(shared_context):
    # Dynamically load all modules from the modules directory
    modules_dir = "modules"
    
    for filename in os.listdir(modules_dir):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]  # Remove .py extension
            
            try:
                # Import the module
                module = importlib.import_module(f"modules.{module_name}")
                
                # Get module configuration
                if hasattr(module, 'get_module_config'):
                    module_config = module.get_module_config()
                    shared_context["logger"].info(f"Loading module: {module_config['name']}")
                    
                    # Create async wrapper for the module's init function
                    async def module_wrapper(mod=module, ctx=shared_context):
                        if hasattr(mod, 'init_module'):
                            await mod.init_module(ctx)
                        else:
                            ctx["logger"].warning(f"Module {module_name} missing init_module function")
                    
                    # Initialize and schedule the module
                    init_mod_config(module_config, shared_context, module_wrapper)
                else:
                    shared_context["logger"].warning(f"Module {module_name} missing get_module_config function")
                    
            except Exception as e:
                shared_context["logger"].error(f"Failed to load module {module_name}: {e}")
