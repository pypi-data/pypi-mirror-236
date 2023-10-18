import jupytext as jt
import sys
import glob
from pathlib import Path
import re
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert.exporters import MarkdownExporter, RSTExporter

TUTORIALS_PATH = "tutorials"
TARGET_DIRECTORY = "docs/getting-started/tutorials"

def main():
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    else:
        base_dir = "."

    parse_markdown_from_tutorials(base_directory=base_dir)

def parse_markdown_from_tutorials(base_directory):
    md_exporter = MarkdownExporter()
    image_exporter = RSTExporter()
    tutorial_base = Path(base_directory).joinpath(TUTORIALS_PATH)
    tutorial_directories = glob.glob(f"{tutorial_base.as_posix()}/tutorial_[1-2][0-9][0-9]")
    tutorial_directories.sort(key=lambda x: int(re.search("_(\d\d\d)", x)[1]))
    output_path = Path(base_directory).joinpath(TARGET_DIRECTORY)
    output_path.mkdir(exist_ok=True, parents=True)
    for tutorial_directory in tutorial_directories:
        tutorial_number = re.search(r"\_(\d\d\d)", tutorial_directory)[1]
        tutorial_parts = glob.glob(f"{Path(tutorial_directory).as_posix()}/tutorial*.py")
        # sorting in case it is accessed randomly
        tutorial_parts.sort(key=lambda x: re.search("_\d\d\d(\w)_", x)[1])
        current_tutorial = ""
        image_folder = output_path.joinpath("images")
        image_folder.mkdir(exist_ok=True, parents=True)
        for part in tutorial_parts:
            print(f"Running Tutorial: {part}")
            run_path = tutorial_directory
            resources = {"metadata": {"path": run_path}}
            exec_proc = ExecutePreprocessor(timeout=None)
            py_file = jt.read(part)
            notebook = jt.writes(py_file, fmt="ipynb")
            notebook = jt.reads(notebook, fmt="ipynb")
            executed_notebook = exec_proc.preprocess(notebook, resources=resources)
            body, resources = md_exporter.from_notebook_node(executed_notebook[0])
            _, image_resources = image_exporter.from_notebook_node(executed_notebook[0])
            if len(image_resources["outputs"].keys()) > 0:
                for imagename, binary in image_resources["outputs"].items():
                    new_name = f"{Path(part).stem}_{imagename}"
                    new_path = image_folder.joinpath(new_name).as_posix()
                    body = body.replace(imagename, f"images/{new_name}")
                    with open(new_path, "wb") as image_file:
                        image_file.write(binary)
            current_tutorial += body

        if tutorial_number is not None:
            name = f"tutorial-{tutorial_number}.md"
            with open(output_path.joinpath(name), "w") as output_file:
                output_file.write(current_tutorial)


if __name__ == "__main__":
    main()
