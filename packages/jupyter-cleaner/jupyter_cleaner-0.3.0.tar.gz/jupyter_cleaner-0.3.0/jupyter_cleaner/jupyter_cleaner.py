import argparse
import json
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import TYPE_CHECKING
from typing import Union

import black  # type: ignore
from reorder_python_imports import _validate_replace_import  # type: ignore
from reorder_python_imports import fix_file_contents  # type: ignore
from reorder_python_imports import import_obj_from_str  # type: ignore
from reorder_python_imports import REMOVALS  # type: ignore
from reorder_python_imports import Replacements  # type: ignore
from reorder_python_imports import REPLACES  # type: ignore

if sys.version_info >= (3, 11):
    try:
        import tomllib
    except ImportError:
        # Help users on older alphas
        if not TYPE_CHECKING:
            import tomli as tomllib
else:
    import tomli as tomllib


def run(
    files: Sequence[Path],
    execution_count: int = 0,
    remove_outputs: bool = True,
    format: bool = True,
    reorder_imports: bool = True,
    indent_level: int = 4,
    exclude_files: Sequence[Path] = [],
    remove_empty_cells: bool = True,
    clear_cell_metadata: bool = True,
    preserve_cell_metadata: Sequence[str] = [],
    ignore_fails: bool = False,
    black_config: Optional[Dict[str, str]] = None,
) -> None:
    """Format Jupyter lab files.

    :param Sequence[Path] files: file(s) to be formatted
    :param Sequence[Path] exclude_files: file(s) to be excluded from formatting
    :param int execution_count: sets execution count. If the integer is greater than zero the count will be printed, else `null` will be printed. Defaults to 0.
    :param bool remove_outputs: remove output from code cells, defaults to True
    :param bool format: format cells using black, defaults to True
    :param bool reorder_imports: reorder imports using reoder-python-imports, defaults to True
    :param int indent_level: integer greater than zero will pretty-print the JSON array with that indent level. An indent level of 0 or negative will only insert newlines.
    :param bool remove_empty_cells: remove empty cells from notebook.
    :param bool clear_cell_metadata: remove metadata from cells from notebook.
    :param Optional[Dict[str, str]] black_config: configuration from black formatting, defaults to None
    :raises TypeError: when file input is unrecognised
    """
    if black_config is None:
        black_config = {}

    for file in files:
        try:
            if (
                not file.is_file()
                or not file.exists()
                or file.suffix != ".ipynb"
                or file in exclude_files
            ):
                continue

            with open(file) as f:
                data = json.load(f)
                python_version = data["metadata"]["language_info"]["version"]
                min_python_version = tuple(
                    map(int, re.findall(r"(\d+)", python_version))
                )
                if len(min_python_version) > 2:
                    min_python_version = min_python_version[:2]

                for cell in data["cells"]:
                    is_code = cell["cell_type"] == "code"
                    is_source = "source" in cell.keys()
                    is_source_empty = len(cell["source"]) == 0
                    is_shell_command = (
                        is_code
                        and is_source
                        and not is_source_empty
                        and cell["source"][0].strip() == "!"
                    )
                    is_metadata = "metadata" in cell.keys()

                    if remove_empty_cells and is_source and is_source_empty:
                        data["cells"].remove(cell)
                        continue

                    if execution_count >= 0 and "execution_count" in cell.keys():
                        cell["execution_count"] = (
                            execution_count if execution_count > 0 else "null"
                        )

                    if remove_outputs and "outputs" in cell.keys():
                        cell["outputs"] = []

                    if (
                        format
                        and is_source
                        and not is_source_empty
                        and is_code
                        and not is_shell_command
                    ):
                        try:
                            mode = black.Mode(is_ipynb=True, **black_config)  # type: ignore
                            str_cell_content = black.format_cell(
                                "".join(cell["source"]), mode=mode, fast=False
                            )
                            cell_content = [
                                f"{c}\n" for c in str_cell_content.split("\n")
                            ]
                            cell_content[-1] = cell_content[-1][
                                :-1
                            ]  # remove last newline
                            cell["source"] = cell_content
                        except black.NothingChanged:
                            pass

                    if (
                        reorder_imports
                        and is_source
                        and not is_source_empty
                        and is_code
                        and not is_shell_command
                    ):
                        to_remove = {
                            import_obj_from_str(s).key
                            for k, v in REMOVALS.items()
                            if min_python_version >= k
                            for s in v
                        }
                        replace_import: List[str] = []
                        for k, v in REPLACES.items():
                            if min_python_version >= k:
                                replace_import.extend(
                                    _validate_replace_import(replace_s)
                                    for replace_s in v
                                )
                        to_replace = Replacements.make(replace_import)
                        str_cell_content = fix_file_contents(
                            "".join(cell["source"]),
                            to_replace=to_replace,
                            to_remove=to_remove,
                        )[:-1]
                        cell_content = [f"{c}\n" for c in str_cell_content.split("\n")]
                        cell_content[-1] = cell_content[-1][:-1]
                        cell["source"] = cell_content

                    if clear_cell_metadata and is_code and is_metadata:
                        cell["metadata"] = {}

                    if len(preserve_cell_metadata) > 0 and is_metadata and is_code:
                        cell["metadata"] = {
                            k: v
                            for k, v in cell["metadata"].items()
                            if k in preserve_cell_metadata
                        }

            with open(file) as f:
                original_data = json.load(f)
                if data == original_data:
                    continue

            with open(file, "w") as f:
                f.write(json.dumps(data, indent=indent_level) + "\n")
            print(f"Reformatted {str(file)}")
        except Exception as e:
            print(f"Reformatting failed: {str(file)}")
            if not ignore_fails:
                raise e
            else:
                continue


@lru_cache
def find_project_root(
    srcs: Sequence[str], stdin_filename: Optional[str] = None
) -> Path:
    """Modified version of black's find_project_root():

    Return a directory containing .git, .hg, or pyproject.toml.

    That directory will be a common parent of all files and directories
    passed in `srcs`.

    If no directory in the tree contains a marker that would specify it's the
    project root, the root of the file system is returned.

    Returns a two-tuple with the first element as the project root path and
    the second element as a string describing the method by which the
    project root was discovered.
    """
    if stdin_filename is not None:
        srcs = tuple(stdin_filename if s == "-" else s for s in srcs)
    if not srcs:
        srcs = [str(Path.cwd().resolve())]

    path_srcs = [Path(Path.cwd(), src).resolve() for src in srcs]

    # A list of lists of parents for each 'src'. 'src' is included as a
    # "parent" of itself if it is a directory
    src_parents = [
        list(path.parents) + ([path] if path.is_dir() else []) for path in path_srcs
    ]

    common_base = max(
        set.intersection(*(set(parents) for parents in src_parents)),
        key=lambda path: path.parts,
    )

    for directory in (common_base, *common_base.parents):
        if (
            (directory / "pyproject.toml").is_file()
            or (directory / ".hg").is_dir()
            or (directory / ".git").exists()
        ):
            return directory

    return directory


def parse_pyproject(
    ignore_pyproject: bool,
) -> Tuple[
    Union[List[str], str, None],
    Union[int, None],
    Union[bool, None],
    Union[bool, None],
    Union[bool, None],
    Union[int, None],
    Union[List[str], str, None],
    Union[bool, None],
    Union[bool, None],
    Union[List[str], str, None],
    Union[bool, None],
]:
    """Parse inputs from pyproject.toml

    :return _type_: Parse inputs from pyproject.toml
    """
    project_root = find_project_root((str(Path.cwd().resolve()),))
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists() or ignore_pyproject:
        return (
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        )

    with open(pyproject_path, "rb") as f:
        pyproject_toml = tomllib.load(f)

    config: Dict[str, Any] = pyproject_toml.get("tool", {}).get("jupyter-cleaner", {})

    files_or_dirs = config["files_or_dirs"] if "files_or_dirs" in config else None
    if isinstance(files_or_dirs, str):
        files_or_dirs = [files_or_dirs]
    exclude_files_or_dirs = (
        config["exclude_files_or_dirs"] if "exclude_files_or_dirs" in config else None
    )
    if isinstance(exclude_files_or_dirs, str):
        exclude_files_or_dirs = [exclude_files_or_dirs]
    execution_count = config["execution_count"] if "execution_count" in config else None
    remove_outputs = config["remove_outputs"] if "remove_outputs" in config else None
    format = config["format"] if "format" in config else None
    reorder_imports = config["reorder_imports"] if "reorder_imports" in config else None
    indent_level = config["indent_level"] if "indent_level" in config else None
    remove_empty_cells = (
        config["remove_empty_cells"] if "remove_empty_cells" in config else None
    )
    clear_cell_metadata = (
        config["clear_cell_metadata"] if "clear_cell_metadata" in config else None
    )
    preserve_cell_metadata = (
        config["preserve_cell_metadata"] if "preserve_cell_metadata" in config else None
    )
    ignore_fails = config["ignore_fails"] if "ignore_fails" in config else None
    return (
        files_or_dirs,
        execution_count,
        remove_outputs,
        format,
        reorder_imports,
        indent_level,
        exclude_files_or_dirs,
        remove_empty_cells,
        clear_cell_metadata,
        preserve_cell_metadata,
        ignore_fails,
    )


def parse_args():
    parser = argparse.ArgumentParser(description="jupyter_cleaner")
    parser.add_argument(
        "files_or_dirs",
        type=str,
        nargs="+",
        help="Jupyter lab files to format or directories to search for lab files",
    )
    parser.add_argument(
        "--exclude_files_or_dirs",
        type=str,
        nargs="+",
        help="Jupyter lab files or directories to exclude from formatting and search",
    )
    parser.add_argument(
        "--execution_count",
        type=int,
        default=-1,
        help="Number to set for the execution count of every cell. A negative integer doesn't replace the execution count and 0 is replaced with null. Defaults to 0.",
    )
    parser.add_argument(
        "--indent_level",
        type=int,
        default=4,
        help="Integer greater than zero will pretty-print the JSON array with that indent level. An indent level of 0 or negative will only insert newlines.. Defaults to 4.",
    )
    parser.add_argument(
        "--remove_outputs",
        action="store_true",
        help="Remove output of cell. Defaults to false.",
    )
    parser.add_argument(
        "--format",
        action="store_true",
        help="Format code of every cell (uses black). Defaults to false.",
    )
    parser.add_argument(
        "--reorder_imports",
        action="store_true",
        help="Reorder imports of every cell (uses reorder-python-imports). Defaults to false.",
    )
    parser.add_argument(
        "--ignore_pyproject",
        action="store_true",
        help="Argparse will over-ride pyproject. Defaults to false.",
    )
    parser.add_argument(
        "--remove_empty_cells",
        action="store_true",
        help="Remove cells that are empty. Defaults to false.",
    )
    parser.add_argument(
        "--clear_cell_metadata",
        action="store_true",
        help="Clear cell metadata. Defaults to false.",
    )
    parser.add_argument(
        "--preserve_cell_metadata",
        type=str,
        nargs="+",
        help="List of keys to preserve in cell metadata.",
    )
    parser.add_argument(
        "--ignore_fails",
        action="store_true",
        help="Continue execution despite failures. Defaults to false.",
    )
    args = parser.parse_args()
    return (
        args.files_or_dirs,
        args.execution_count,
        args.remove_outputs,
        args.format,
        args.reorder_imports,
        args.indent_level,
        args.exclude_files_or_dirs,
        args.ignore_pyproject,
        args.remove_empty_cells,
        args.clear_cell_metadata,
        args.preserve_cell_metadata,
        args.ignore_fails,
    )


def get_lab_files(files_or_dirs: List[Path]) -> List[Path]:
    files = []
    for file_or_dir in files_or_dirs:
        if file_or_dir.is_dir():
            files.extend([p for p in file_or_dir.rglob("*.ipynb")])
        elif file_or_dir.is_file() and file_or_dir.suffix == ".ipynb":
            files.append(file_or_dir)
        else:
            raise ValueError("File or directory does not exist or could not be found")
    return list(set(files))


def process_inputs(
    args_files_or_dirs: List[str],
    args_execution_count: int,
    args_remove_outputs: bool,
    args_format: bool,
    args_reorder_imports: bool,
    args_indent_level: int,
    args_exclude_files_or_dirs: Union[List[str], None],
    args_remove_empty_cells: bool,
    args_clear_cell_metadata: bool,
    args_preserve_cell_metadata: Union[List[str], None],
    args_ignore_fails: bool,
    project_files_or_dirs: Union[List[str], str, None],
    project_execution_count: Union[int, None],
    project_remove_outputs: Union[bool, None],
    project_format: Union[bool, None],
    project_reorder_imports: Union[bool, None],
    project_indent_level: Union[int, None],
    project_exclude_files_or_dirs: Union[List[str], str, None],
    project_remove_empty_cells: Union[bool, None],
    project_clear_cell_metadata: Union[bool, None],
    project_preserve_cell_metadata: Union[List[str], str, None],
    project_ignore_fails: Union[bool, None],
) -> Tuple[
    List[Path], int, bool, bool, bool, int, List[Path], bool, bool, List[str], bool
]:
    """Creates inputs of the right format and prioritises pyproject inputs over argparse inputs, outside of files and directories where all inputs are combined.

    :param List[str] args_files_or_dirs: files or directories from argparse
    :param List[str] args_exclude_files_or_dirs: files or directories to exclude from argparse
    :param int args_execution_count: execution count from argparse
    :param bool args_remove_outputs: remove code output from argparse
    :param bool args_format: apply formatting from argparse
    :param bool args_reorder_imports: reorder imports from argparse
    :param Union[List[str], str, None] project_files_or_dirs: files or directories from pyproject
    :param Union[List[str], str, None] project_exclude_files_or_dirs: files or directories to exclude from pyproject
    :param Union[int, None] project_execution_count: execution count from pyproject
    :param Union[bool, None] project_remove_outputs: remove code output from pyproject
    :param Union[bool, None] args_remove_empty_cells: remove empty cells from argparse
    :param Union[bool, None] project_remove_empty_cells: remove empty cells from pyproject
    :param Union[bool, None] project_format: apply formatting from pyproject
    :param Union[bool, None] project_reorder_imports: reorder imports from pyproject
    :return Tuple[ Union[List[str], str, None], Union[int, None], Union[bool, None], Union[bool, None], Union[bool, None], ]: inputs to run()
    """

    if args_files_or_dirs is None:
        args_files_or_dirs = [Path.cwd().resolve()]
    if project_files_or_dirs is None:
        project_files_or_dirs = []
    elif isinstance(project_files_or_dirs, str):
        project_files_or_dirs = [project_files_or_dirs]
    files_or_dirs = [Path(f) for f in project_files_or_dirs + args_files_or_dirs]
    if project_exclude_files_or_dirs is None:
        project_exclude_files_or_dirs = []
    elif isinstance(project_exclude_files_or_dirs, str):
        project_exclude_files_or_dirs = [project_exclude_files_or_dirs]
    if args_exclude_files_or_dirs is None:
        args_exclude_files_or_dirs = []
    exclude_files_or_dirs = [
        Path(f) for f in project_exclude_files_or_dirs + args_exclude_files_or_dirs
    ]
    execution_count = (
        project_execution_count
        if project_execution_count is not None
        else args_execution_count
    )
    remove_outputs = (
        project_remove_outputs
        if project_remove_outputs is not None
        else args_remove_outputs
    )
    format = project_format if project_format is not None else args_format
    reorder_imports = (
        project_reorder_imports
        if project_reorder_imports is not None
        else args_reorder_imports
    )
    indent_level = (
        project_indent_level if project_indent_level is not None else args_indent_level
    )
    remove_empty_cells = (
        project_remove_empty_cells
        if project_remove_empty_cells is not None
        else args_remove_empty_cells
    )
    clear_cell_metadata = (
        project_clear_cell_metadata
        if project_clear_cell_metadata is not None
        else args_clear_cell_metadata
    )
    if project_preserve_cell_metadata is None:
        project_preserve_cell_metadata = []
    elif isinstance(project_preserve_cell_metadata, str):
        project_preserve_cell_metadata = [project_preserve_cell_metadata]
    if args_preserve_cell_metadata is None:
        args_preserve_cell_metadata = []
    preserve_cell_metadata = (
        project_preserve_cell_metadata + args_preserve_cell_metadata
    )
    ignore_fails = (
        project_ignore_fails if project_ignore_fails is not None else args_ignore_fails
    )

    return (
        files_or_dirs,
        execution_count,
        remove_outputs,
        format,
        reorder_imports,
        indent_level,
        exclude_files_or_dirs,
        remove_empty_cells,
        clear_cell_metadata,
        preserve_cell_metadata,
        ignore_fails,
    )


def main():
    (
        args_files_or_dirs,
        args_execution_count,
        args_remove_outputs,
        args_format,
        args_reorder_imports,
        args_indent_level,
        args_exclude_files_or_dirs,
        args_ignore_pyproject,
        args_remove_empty_cells,
        args_clear_cell_metadata,
        args_preserve_cell_metadata,
        args_ignore_fails,
    ) = parse_args()

    (
        project_files_or_dirs,
        project_execution_count,
        project_remove_outputs,
        project_format,
        project_reorder_imports,
        project_indent_level,
        project_exclude_files_or_dirs,
        project_remove_empty_cells,
        project_clear_cell_metadata,
        project_preserve_cell_metadata,
        project_ignore_fails,
    ) = parse_pyproject(args_ignore_pyproject)

    (
        files_or_dirs,
        execution_count,
        remove_outputs,
        format,
        reorder_imports,
        indent_level,
        exclude_files_or_dirs,
        remove_empty_cells,
        clear_cell_metadata,
        preserve_cell_metadata,
        ignore_fails,
    ) = process_inputs(
        args_files_or_dirs,
        args_execution_count,
        args_remove_outputs,
        args_format,
        args_reorder_imports,
        args_indent_level,
        args_exclude_files_or_dirs,
        args_remove_empty_cells,
        args_clear_cell_metadata,
        args_preserve_cell_metadata,
        args_ignore_fails,
        project_files_or_dirs,
        project_execution_count,
        project_remove_outputs,
        project_format,
        project_reorder_imports,
        project_indent_level,
        project_exclude_files_or_dirs,
        project_remove_empty_cells,
        project_clear_cell_metadata,
        project_preserve_cell_metadata,
        project_ignore_fails,
    )

    files = get_lab_files(files_or_dirs)
    exclude_files = get_lab_files(exclude_files_or_dirs)

    run(
        files,
        execution_count,
        remove_outputs,
        format,
        reorder_imports,
        indent_level,
        exclude_files,
        remove_empty_cells,
        clear_cell_metadata,
        preserve_cell_metadata,
        ignore_fails,
    )
