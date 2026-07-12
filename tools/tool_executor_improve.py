"""Tool executor for calling available tool functions in the tools package.

This executor discovers tool modules in the tools package, registers functions
that are declared in tools/tool_definitions.py, and exposes a single execute()
method that validates and runs the tool with the provided arguments.

Improvements over the original:
- Auto-discovery of tool modules (no hard-coded if/else)
- Typed signatures and clearer errors
- Logging for easier debugging
- Utilities to inspect available tools
"""
from typing import Any, Callable, Dict, Iterable, List, Set, Optional
import importlib
import inspect
import logging
import pkgutil

import tools as tools_pkg
from tools import tool_definitions

logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig()


class ToolNotFoundError(ValueError):
    pass


class ToolExecutionError(RuntimeError):
    pass


class ToolExecutor:
    """Discover and execute tools from the tools package.

    On initialization the executor scans the `tools` package for modules and
    registers functions whose names match tools defined in
    `tools.tool_definitions`.
    """

    def __init__(self) -> None:
        self._registry: Dict[str, Callable[..., Any]] = {}
        self._defined_tool_names: Set[str] = self._load_defined_tool_names()
        self._discover_and_register()

    def _load_defined_tool_names(self) -> Set[str]:
        """Read tool names from tools.tool_definitions module.

        Returns:
            A set of tool function names declared in tool_definitions.
        """
        names: Set[str] = set()
        for value in vars(tool_definitions).values():
            if isinstance(value, dict) and "name" in value:
                names.add(value["name"])
        logger.debug("Defined tool names: %s", names)
        return names

    def _discover_and_register(self) -> None:
        """Import modules in the tools package and register matching functions."""
        for module_info in pkgutil.iter_modules(tools_pkg.__path__):
            module_name = module_info.name
            full_name = f"{tools_pkg.__name__}.{module_name}"
            try:
                module = importlib.import_module(full_name)
            except Exception:
                logger.exception("Failed to import module %s", full_name)
                continue

            for attr_name, func in inspect.getmembers(module, inspect.isfunction):
                if attr_name in self._defined_tool_names:
                    try:
                        self.register(attr_name, func)
                    except Exception:
                        logger.exception("Failed to register tool %s from %s", attr_name, full_name)

    def register(self, name: str, func: Callable[..., Any]) -> None:
        """Register a callable under the given tool name.

        Raises:
            ValueError: if a tool with the same name is already registered.
        """
        if name in self._registry:
            raise ValueError(f"Tool '{name}' is already registered")
        self._registry[name] = func
        logger.info("Registered tool: %s -> %s", name, func)

    def get_registered_tools(self) -> List[str]:
        """Return a sorted list of registered tool names."""
        return sorted(self._registry.keys())

    def execute(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a registered tool with the provided keyword arguments.

        Args:
            tool_name: Name of the tool to execute (must be registered).
            arguments: Mapping of argument name to value to pass as kwargs.

        Returns:
            The tool's return value.

        Raises:
            ToolNotFoundError: If the tool is not registered.
            ToolExecutionError: If the underlying tool raised an exception.
        """
        if tool_name not in self._registry:
            message = f"Tool '{tool_name}' is not supported. Available: {self.get_registered_tools()}"
            logger.error(message)
            raise ToolNotFoundError(message)

        func = self._registry[tool_name]

        # Optional: quick validation of arguments vs signature
        sig = inspect.signature(func)
        try:
            # Bind arguments to get clearer error messages for missing/extra args
            sig.bind_partial(**arguments)
        except TypeError as e:
            message = f"Invalid arguments for tool '{tool_name}': {e}"
            logger.error(message)
            raise ToolExecutionError(message)

        try:
            result = func(**arguments)
            logger.debug("Tool '%s' executed successfully", tool_name)
            return result
        except Exception as exc:
            logger.exception("Error executing tool '%s'", tool_name)
            raise ToolExecutionError(str(exc)) from exc


# Convenience singleton for callers who do not need to manage executor lifecycle
_default_executor: Optional[ToolExecutor] = None


def get_default_executor() -> ToolExecutor:
    global _default_executor
    if _default_executor is None:
        _default_executor = ToolExecutor()
    return _default_executor


if __name__ == "__main__":
    # Simple demo when running module directly
    exe = get_default_executor()
    print("Available tools:", exe.get_registered_tools())