"""
This is from the janzu project.  Sample code only - not expected to work here.

The science modules take ~20s to import, and aren't needed in the django web app.
This file contains a list of modules that are lazy loaded.
"""

import sys
from importlib.util import LazyLoader, find_spec
from importlib import import_module
from types import ModuleType

# List all modules you want to lazy load
LAZY_MODULES = [
    "google.cloud.aiplatform",
    "imblearn",
    "imblearn.over_sampling",
    "imblearn.under_sampling",
    "predictors.auto_prompt_engineer.auto_prompt_engineer",
    "predictors.contrib",
    "predictors.contrib.blip",
    "predictors.contrib.claude.claude_aws",
    "predictors.contrib.google.gemini",
    "predictors.contrib.google.gemini",
    "predictors.contrib.openai",
    "predictors.contrib.openai.openai",
    "predictors.contrib.openai.utils",
    "predictors.contrib.owlvit",
    "predictors.datasets",
    "predictors.datasets.class_balance",
    "predictors.datasets.dataset",
    "predictors.finetuning",
    "predictors.finetuning.fine_tuner_nearest_neighbor",
    "predictors.finetuning.predictions",
    "predictors.object_detection",
    "predictors.pipeline",
    "predictors.pipeline.exceptions",
    "predictors.pipeline.generic",
    "predictors.visual_reasoning",
    "predictors",
    "sklearn",
    #"torch",  # used in base_settings to turn off autograd
    "vertexai",
]

def setup_lazy_modules():
    # First, collect all modules including parents that need lazy loading
    all_modules = set()
    for module_name in LAZY_MODULES:
        parts = module_name.split('.')
        # Add all parent modules
        for i in range(len(parts)):
            all_modules.add('.'.join(parts[:i+1]))
    
    # Process modules in order from shallowest to deepest
    for module_name in sorted(all_modules, key=lambda x: x.count('.')):
        if module_name not in sys.modules:
            try:
                # Try to import the parent module normally first
                if '.' in module_name:
                    parent_name = module_name.rsplit('.', 1)[0]
                    if parent_name not in sys.modules:
                        import_module(parent_name)
                
                spec = find_spec(module_name)
                if spec is None:
                    if '.' in module_name:
                        parent = module_name.rsplit('.', 1)[0]
                        if parent in sys.modules:
                            # Just create a module object, don't try to load it yet
                            sys.modules[module_name] = ModuleType(module_name)
                            continue
                    print(f"Lazy module {module_name} not found")
                    continue
                
                # This should create a lazy loader that will load the module when accessed
                loader = LazyLoader(spec.loader)
                spec.loader = loader
                module = loader.create_module(spec)
                if module is None:
                    module = ModuleType(module_name)
                sys.modules[module_name] = module
                print(f"Set up lazy loading for {module_name}")
            except (ImportError, AttributeError) as e:
                print(f"Error setting up {module_name}: {e}")
                sys.modules[module_name] = ModuleType(module_name)