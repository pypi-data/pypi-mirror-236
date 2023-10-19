# jupyter-cleaner

jupyter-cleaner makes tracking Jupyter lab files in git easy.

This is done by:
- Removing the output of cells
- Formatting the source of cells (using black)
- Reordering imports in the source of cells (using reorder-python-imports)
- Setting the execution count of cells
- pretty printing the JSON array

It is recommended to run jupyter-cleaner before adding the Jupyter lab files to the stage in git. This allows for easier tracking of differences between commits.

## CLI
running `jupyter-cleaner -h` displays:
```
usage: jupyter-cleaner [-h] [--exclude_files_or_dirs EXCLUDE_FILES_OR_DIRS [EXCLUDE_FILES_OR_DIRS ...]] [--execution_count EXECUTION_COUNT]
                       [--indent_level INDENT_LEVEL] [--remove_outputs] [--format] [--reorder_imports] [--ignore_pyproject]
                       files_or_dirs [files_or_dirs ...]

jupyter_cleaner

positional arguments:
  files_or_dirs         Jupyter lab files to format or directories to search for lab files

options:
  -h, --help            show this help message and exit
  --exclude_files_or_dirs EXCLUDE_FILES_OR_DIRS [EXCLUDE_FILES_OR_DIRS ...]
                        Jupyter lab files or directories to exclude from formatting and search
  --execution_count EXECUTION_COUNT
                        Number to set for the execution count of every cell. Defaults to 0.
  --indent_level INDENT_LEVEL
                        Integer greater than zero will pretty-print the JSON array with that indent level. An indent level of 0 or negative
                        will only insert newlines.. Defaults to 4.
  --remove_outputs      Remove output of cell. Defaults to false.
  --format              Format code of every cell (uses black). Defaults to false.
  --reorder_imports     Reorder imports of every cell (uses reorder-python-imports). Defaults to false.
  --ignore_pyproject    Argparse will over-ride pyproject. Defaults to false.
```

## pyproject.toml
Inputs to jupyter-cleaner can be supplied via pyproject.toml:
```
[tool.jupyter_cleaner]
execution_count=0
remove_outputs=true
format=true
reorder_imports=true
indent_level=4
```
