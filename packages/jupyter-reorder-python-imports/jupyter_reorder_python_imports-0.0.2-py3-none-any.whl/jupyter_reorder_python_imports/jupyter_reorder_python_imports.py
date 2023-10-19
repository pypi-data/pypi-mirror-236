import json
import sys
import typing as t

from IPython.core import getipython
from IPython.core.display import HTML
from IPython.core.display import Javascript
from IPython.core.interactiveshell import ExecutionInfo
from IPython.display import display
from IPython.terminal.interactiveshell import TerminalInteractiveShell as Ipt
from reorder_python_imports import _validate_replace_import
from reorder_python_imports import fix_file_contents
from reorder_python_imports import import_obj_from_str
from reorder_python_imports import REMOVALS
from reorder_python_imports import Replacements
from reorder_python_imports import REPLACES

formatter = None


class ReorderPythonImports:
    def __init__(
        self,
        ip: Ipt,
        is_lab: bool = True,
        min_python_version: t.Optional[t.Union[t.Tuple[int], t.Tuple[int, int]]] = None,
    ) -> None:
        """Initialize the class with the passed in config.
        Notes on the JavaScript stuff for notebook:
            - Requires:
                - update=False for the `html` part
            - Other:
                - Can use `jb_cells.find` instead of the for loop if you set the main function to `text/html` and set `raw=True`
            def display:
                https://github.com/ipython/ipython/blob/77e188547e5705a0e960551519a851ac45db8bfc/IPython/core/display_functions.py#L88  # noqa
        :param t.Optional[Ipt] ip: iPython interpreter, defaults to None
        :param bool lab: is session jupyterlab, defaults to True
        :param t.Optional[t.Tuple[int]] min_python_version: minimum python version for reorder-python-imports, defaults to None
        """

        self.shell = ip
        self.min_python_version = min_python_version
        if self.min_python_version is None:
            versions = sorted(REMOVALS.keys() | REPLACES.keys())
            self.min_python_version = (sys.version_info.major, sys.version_info.minor)
            if self.min_python_version not in versions:
                raise ValueError(
                    f"Python version {self.min_python_version} is unsupported. Supported versions are {versions}"
                )

        self.is_lab = is_lab
        if is_lab:
            js_func = """
                <script type="application/javascript" id="jupyter_reorder_python_imports">
                (function() {
                    if (window.IPython === undefined) {
                        return
                    }
                    var msg = "WARNING: it looks like you might have loaded " +
                        "jupyter_reorder_python_imports in a non-lab notebook with " +
                        "`is_lab=True`. Please double check, and if " +
                        "loading with `%load_ext` please review the README!"
                    console.log(msg)
                    alert(msg)
                })()
                </script>
                """
        else:
            js_func = """
                <script type="application/javascript" id="jupyter_reorder_python_imports">
                function jb_set_cell(
                        jb_formatted_code
                        ) {
                    for (var cell of Jupyter.notebook.get_cells()) {
                        if (cell.input_prompt_number == "*") {
                            cell.set_text(jb_formatted_code)
                            return
                        }
                    }
                }
                </script>
                """
        display(  # type: ignore[no-untyped-call, unused-ignore]
            HTML(js_func),  # type: ignore[no-untyped-call, unused-ignore]
            display_id="jupyter_reorder_python_imports",
            update=False,
        )

    def _set_cell(self, cell_content: str) -> None:
        if self.is_lab:
            self.shell.set_next_input(cell_content, replace=True)
        else:
            js_code = f"""
            (function() {{
                jb_set_cell({json.dumps(cell_content)})
            }})();
            """
            display(  # type: ignore[no-untyped-call, unused-ignore]
                Javascript(js_code),  # type: ignore[no-untyped-call, unused-ignore]
                display_id="jupyter_reorder_python_imports",
                update=True,
            )

    def _format_cell(self, cell_info: ExecutionInfo) -> None:
        cell_content = str(cell_info.raw_cell)

        try:
            to_remove = {
                import_obj_from_str(s).key
                for k, v in REMOVALS.items()
                if self.min_python_version >= k
                for s in v
            }
            replace_import: t.List[str] = []
            for k, v in REPLACES.items():
                if self.min_python_version >= k:
                    replace_import.extend(
                        _validate_replace_import(replace_s) for replace_s in v
                    )
            to_replace = Replacements.make(replace_import)
            formatted_code = fix_file_contents(
                cell_content,
                to_replace=to_replace,
                to_remove=to_remove,
            )[:-1]
        except Exception:
            return

        if formatted_code != cell_content:
            self._set_cell(formatted_code)


def load_ipython_extension(
    ip: Ipt,
) -> None:
    """Load the extension via `%load_ext jupyter_reorder_python_imports`.

    :param Ipt ip: iPython interpreter
    """
    load(ip=ip)


def load(
    ip: t.Optional[Ipt] = None,
    lab: bool = True,
    min_python_version: t.Optional[t.Tuple[int]] = None,
) -> None:
    """Load the extension using `jupyter_reorder_python_imports.load()`.
    This allows passing in custom configuration using input arguments.

    :param t.Optional[Ipt] ip: iPython interpreter, defaults to None
    :param bool lab: is session jupyterlab, defaults to True
    :param t.Optional[t.Tuple[int]] min_python_version: minimum python version for reorder-python-imports, defaults to None
    """
    global formatter

    if not ip:
        ip = getipython.get_ipython()  # type: ignore[no-untyped-call, unused-ignore]
    if not ip:
        return

    if formatter is None:
        formatter = ReorderPythonImports(
            ip, is_lab=lab, min_python_version=min_python_version
        )
    ip.events.register("pre_run_cell", formatter._format_cell)  # type: ignore[no-untyped-call, unused-ignore]


def unload_ipython_extension(ip: Ipt) -> None:
    """Unload the extension

    :param Ipt ip: iPython interpreter
    """
    global formatter

    if formatter:
        ip.events.unregister("pre_run_cell", formatter._format_cell)  # type: ignore[no-untyped-call, unused-ignore]
        formatter = None
