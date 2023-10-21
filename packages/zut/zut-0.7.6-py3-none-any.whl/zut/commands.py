"""
Add and execute commands easily, based on argparse.
Usefull for non-Django applications.
For Django applications, use including command management instead.
"""
from __future__ import annotations
from contextlib import nullcontext
import inspect

import logging
from argparse import Action, ArgumentParser, Namespace, RawTextHelpFormatter, _SubParsersAction
from configparser import _UNSET
from importlib import import_module
from importlib.util import find_spec
from pathlib import Path
import sys
from types import FunctionType, GeneratorType, ModuleType
from typing import Any, Callable, Sequence

from .logging import configure_logging
from .process import get_exit_code

logger = logging.getLogger(__name__)


def add_func_command(parser: ArgumentParser|_SubParsersAction[ArgumentParser], func: FunctionType, add_arguments: FunctionType = None, *, name: str = None, doc: str = None, defaults: dict[str,Any] = {}):
    """
    Add the given function as a subcommand of the parser.
    """
    if name is None:
        name = func.__name__
    if doc is None:
        doc = func.__doc__

    subparsers = _get_subparsers(parser)
    cmdparser = subparsers.add_parser(name, help=get_help_text(doc), description=get_description_text(doc), formatter_class=RawTextHelpFormatter)
    cmdparser.set_defaults(func=func, **defaults)

    if add_arguments:
        add_arguments(cmdparser)

    return cmdparser


def add_module_command(parser: ArgumentParser|_SubParsersAction[ArgumentParser], module: str|ModuleType, *, name: str = None, doc: str = None, defaults: dict[str,Any] = {}):
    """
    Add the given module as a subcommand of the parser.
    
    The command function must be named `handler` and the arguments definition function, if any, must be named `add_arguments`.
    """
    if not isinstance(module, ModuleType):
        module = import_module(module)

    if name is None:
        module_basename = module.__name__.split('.')[-1]
        name = module_basename.split('.')[-1]
        if name.endswith('cmd') and len(name) > len('cmd'):
            name = name[0:-len('cmd')]

    try:
        func = getattr(module, 'handle')
    except AttributeError:
        func = getattr(module, name)

    add_arguments = getattr(module, 'add_arguments', None)
    
    if doc is None and hasattr(module, '__description__'):
        doc = getattr(module, '__description__')
    
    add_func_command(parser, func, add_arguments=add_arguments, name=name, doc=doc, defaults=defaults)


def add_package_commands(parser: ArgumentParser|_SubParsersAction[ArgumentParser], package: str):
    """
    Add all modules in the given package as subcommands of the parser.
    """
    package_spec = find_spec(package)
    if not package_spec:
        raise KeyError(f"package not found: {package}")
    if not package_spec.origin:
        raise KeyError(f"not a package: {package} (did you forget __init__.py ?)")
    package_path = Path(package_spec.origin).parent
    
    for module_path in sorted(package_path.iterdir()):
        if module_path.is_dir() or module_path.name.startswith("_") or not module_path.name.endswith(".py"):
            continue

        module = module_path.stem
        add_module_command(parser, f"{package}.{module}")


def _get_subparsers(parser: ArgumentParser) -> _SubParsersAction[ArgumentParser]:
    """
    Get or create the subparsers object associated with the given parser.
    """
    if isinstance(parser, _SubParsersAction):
        return parser
    elif parser._subparsers is not None:
        return next(filter(lambda action: isinstance(action, _SubParsersAction), parser._subparsers._actions))
    else:
        return parser.add_subparsers(title='commands')


def get_help_text(docstring: str):
    if docstring is None:
        return None
    
    docstring = docstring.strip()
    try:
        return docstring[0:docstring.index('\n')].strip()
    except:
        return docstring


def get_description_text(docstring: str):
    if docstring is None:
        return None
    
    docstring = docstring.replace('\t', ' ')
    lines = docstring.splitlines(keepends=False)

    min_indent = None
    for line in lines:
        lstriped_line = line.lstrip()
        if lstriped_line:
            indent = len(line) - len(lstriped_line)
            if min_indent is None or min_indent > indent:
                min_indent = indent
    
    description = None
    for line in lines:
        description = (description + '\n' if description else '') + line[min_indent:]

    return description


class CommandManager:
    def __init__(self, root_module: ModuleType = None, prog: str = None):
        self._registered_resources: dict[str,CommandResource] = {}
        self._used_resources: list[CommandResource] = []
        self._args: dict[str,Any] = None

        if root_module or prog:
            self._prepare(root_module, prog)


    def _prepare(self, root_module: ModuleType, prog: str):
        """
        Prepare entry points. May be done in `__init__` (simple because applicable whatever the usage)
        or in the usage function, `main` for example (sometimes required to avoid circular dependencies when passing the root module in `__init__`).
        """
        if hasattr(self, 'root_module') or hasattr(self, 'prog'):
            raise ValueError(f"root_module or prog already provided")

        self.root_module = root_module if root_module else inspect.getmodule(inspect.stack()[2][0])
        self.prog = prog

        if self.root_module.__name__ == '__main__':
            self.root_module = import_module(".", package=self.root_module.__package__)
            
        if not self.prog:
            self.prog = self.root_module.__name__
            if self.prog.endswith('.commands'):
                self.prog = self.prog[0:-len('.commands')]
        
        # Determine entry points
        self.add_arguments = getattr(self.root_module, 'add_arguments', None)
        self.handle = getattr(self.root_module, 'handle', None)
        self.runner = getattr(self.root_module, 'runner', None)

        if hasattr(self.root_module, '__description__'):
            self.description = get_description_text(self.root_module.__description__)
        elif self.handle:
            self.description = get_description_text(self.handle.__doc__)
        else:
            self.description = None


    def main(self, root_module: ModuleType = None, prog: str = None):
        """
        A default `main` function for applications.

        Commands are defined in the module's top-level namespace (i.e. __init__.py)
        using `handle` and `add_arguments` functions.

        Compatible with nested subcommands.
        """
        if not hasattr(self, 'root_module') or root_module or prog:
            self._prepare(root_module, prog)

        configure_logging()

        # Build argument parser
        parser = ArgumentParser(prog=self.prog, description=self.description, formatter_class=RawTextHelpFormatter)
        parser.add_argument('--version', action='version', version=self._get_version())

        if self.add_arguments:
            self.add_arguments(parser)

        # Parse command line
        namespace = parser.parse_args()
        args = vars(namespace)
        func = args.pop('func', self.handle)

        # Run command
        r = self.run_command(func, **args)
        exit(r)


    def create_django_command(self, root_module: ModuleType = None, prog: str = None):
        """
        Create a Django management command.
        """
        from django.core.management import BaseCommand

        if not hasattr(self, 'root_module') or root_module or prog:
            self._prepare(root_module, prog)

        class Command(BaseCommand):
            help = self.description

            def add_arguments(self2, parser):
                if self.add_arguments:
                    self.add_arguments(parser)

            def handle(self2, func=None, **args):
                args.pop('verbosity', None)
                args.pop('settings', None)
                args.pop('pythonpath', None)
                args.pop('traceback', None)
                args.pop('no_color', None)
                args.pop('force_color', None)
                args.pop('skip_checks', None)

                if func is None and self.handle:
                    func = self.handle

                return self.run_command(func, **args)

        return Command


    def run_command(self, func: Callable, **args):
        if not func:
            logger.error("no command given")
            return 1
        
        with self.prepare_args(args, func) as args:
            # Run command
            try:
                if self.runner:
                    r = self.runner(func, args)
                else:            
                    r = func(**args)

                r = get_exit_code(r)
            except BaseException as err:
                message = str(err)
                logger.exception(f"exiting on {type(err).__name__}{f': {message}' if message else ''}")
                r = 1
            return r


    def _get_version(self):
        """
        Search the first of the module or module's parents which contains a __version__ attribute.
        """
        def recurse(module: ModuleType):
            try:
                return module.__name__, getattr(module, '__version__')
            except AttributeError:
                module_parts = module.__name__.split('.')
                if len(module_parts) <= 1:
                    return None, None
                parent_module = sys.modules['.'.join(module_parts[:-1])]
                return recurse(parent_module)
            
        version_module, version = recurse(self.root_module)
        if version:
            return f"{version_module} {version}"
        else:
            return None


    def register_resource(self, dest: str, builder: Callable[[str],Any], metavar: str = None, default: str = None, help: str = None):
        """
        Register a resource.
        - `dest`: name of the function parameter.
        """
        if dest in self._registered_resources:
            raise ValueError(f"resource already defined: {dest}")
        
        self._registered_resources[dest] = CommandResource(dest, builder, metavar=metavar, default=default, help=help)


    def get_resource_action(self, dest: str):
        return self._registered_resources[dest].get_action()
    

    def prepare_args(self, args: dict, func: FunctionType):
        if isinstance(args, Namespace):
            self._args = vars(args)
        else:
            self._args = args

        func_parameters = inspect.signature(func).parameters
        
        for dest, resource in self._registered_resources.items():
            used = False
            
            if dest in self._args:
                instance = resource.get(self._args[dest])
                self._args[dest] = instance
                used = True

            elif dest in func_parameters:
                instance = resource.get(_UNSET)
                self._args[dest] = instance
                used = True
            
            if used and resource not in self._used_resources:
                self._used_resources.append(resource)
        
        return self


    def __enter__(self):
        if self._args is None:
            raise ValueError('prepare_args must be called first')
        return self._args


    def __exit__(self, exc_type, exc_value, traceback):
        for instance in self._used_resources:
            instance.close(exc_type, exc_value, traceback)


class CommandResource:
    def __init__(self, dest: str, builder: Callable[...,Any], metavar: str = None, default: str = None, help: str = None):
        self.dest = dest
        self.builder = builder
        self.metavar = metavar
        self.default = default
        self.help = help
        self._built: dict[Any,Any] = {}


    def get_action(self):
        class ResourceAction(Action):
            def __init__(a_self, option_strings, **kwargs):            
                kwargs['dest'] = self.dest
                if not 'default' in kwargs and self.default is not None:
                    kwargs['default'] = self.default
                if not 'metavar' in kwargs and self.metavar is not None:
                    kwargs['metavar'] = self.metavar
                if not 'help' in kwargs and self.help is not None:
                    kwargs['help'] = self.help
                super().__init__(option_strings, **kwargs)

            def __call__(a_self, parser: ArgumentParser, namespace: Namespace, values: str | Sequence[Any] | None, option_string: str | None = None):
                setattr(namespace, self.dest, values)
        
        return ResourceAction


    def get(self, arg_value = _UNSET):
        if not arg_value in self._built:
            result = self.builder(arg_value) if arg_value is not _UNSET else self.builder()
            if hasattr(result, '__enter__'):
                result.__enter__()
            if isinstance(result, GeneratorType):
                result = [instance for instance in result]
            self._built[arg_value] = result
        
        return self._built[arg_value]
        

    def close(self, exc_type, exc_value, traceback):
        def close_instance(instance):
            # actual closing
            if hasattr(instance, '__exit__'):
                instance.__exit__(exc_type, exc_value, traceback)
            elif hasattr(instance, 'close'):
                instance.close()

        def close_list(instances: list):
            for instance in instances:
                if isinstance(instance, list):
                    close_list(instance)
                else:
                    close_instance(instance)

        def close_dict(instances: dict):
            for instance in instances.values():
                if isinstance(instance, list):
                    close_list(instance)
                else:
                    close_instance(instance)

        close_dict(self._built)
