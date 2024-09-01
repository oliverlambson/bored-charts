"""forked from fastapi_cli.discover because i needed to get rid of the print statements"""

import importlib
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Union

from fastapi import FastAPI


def get_default_path() -> Path:
    potential_paths = (
        "main.py",
        "app.py",
        "api.py",
        "app/main.py",
        "app/app.py",
        "app/api.py",
    )

    for full_path in potential_paths:
        path = Path(full_path)
        if path.is_file():
            return path

    raise Exception(
        "Could not find a default file to run, please provide an explicit path"
    )


@dataclass
class ModuleData:
    module_import_str: str
    extra_sys_path: Path


def get_module_data_from_path(path: Path) -> ModuleData:
    use_path = path.resolve()
    module_path = use_path
    if use_path.is_file() and use_path.stem == "__init__":
        module_path = use_path.parent
    module_paths = [module_path]
    extra_sys_path = module_path.parent
    for parent in module_path.parents:
        init_path = parent / "__init__.py"
        if init_path.is_file():
            module_paths.insert(0, parent)
            extra_sys_path = parent.parent
        else:
            break
    module_str = ".".join(p.stem for p in module_paths)
    return ModuleData(
        module_import_str=module_str, extra_sys_path=extra_sys_path.resolve()
    )


def get_app_name(*, mod_data: ModuleData, app_name: Union[str, None] = None) -> str:
    try:
        mod = importlib.import_module(mod_data.module_import_str)
    except (ImportError, ValueError):
        raise  # missing __init__.py?
    object_names = dir(mod)
    object_names_set = set(object_names)
    if app_name:
        if app_name not in object_names_set:
            raise Exception(
                f"Could not find app name {app_name} in {mod_data.module_import_str}"
            )
        app = getattr(mod, app_name)
        if not isinstance(app, FastAPI):
            raise Exception(
                f"The app name {app_name} in {mod_data.module_import_str} doesn't seem to be a FastAPI app"
            )
        return app_name
    for preferred_name in ["app", "api"]:
        if preferred_name in object_names_set:
            obj = getattr(mod, preferred_name)
            if isinstance(obj, FastAPI):
                return preferred_name
    for name in object_names:
        obj = getattr(mod, name)
        if isinstance(obj, FastAPI):
            return name
    raise Exception("Could not find FastAPI app in module, try using --app")


def get_import_string(*, path: Path | None = None, app_name: str | None = None) -> str:
    if not path:
        path = get_default_path()
    if not path.exists():
        raise Exception(f"Path does not exist {path}")
    mod_data = get_module_data_from_path(path)
    sys.path.insert(0, str(mod_data.extra_sys_path))
    use_app_name = get_app_name(mod_data=mod_data, app_name=app_name)
    import_string = f"{mod_data.module_import_str}:{use_app_name}"
    return import_string
