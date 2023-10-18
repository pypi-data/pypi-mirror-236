from remix.framework.api.run import run_remix
import sys
import os
import subprocess as sp
from pathlib import Path
from remix.framework import __gamscode__
import shutil
# remix run --datadir=testing/instances/minimal_lp/data docfile=docs/scripts/remix --roundts=1
SOURCE_PATH = "remix/framework/model/source"
DOCFILE_PATH = "docs/scripts/remix"
TESTCASE_PATH = "testing/instances/minimal_lp/data"

def main():
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]       
    else:
        base_dir = "."
    doc_file = Path(base_dir).joinpath(DOCFILE_PATH)
    if Path(base_dir).exists():
        source_directory = Path(base_dir).joinpath(SOURCE_PATH).resolve()
        if not source_directory.exists():
            raise ValueError(f"The source directory: {source_directory} does not exist.")

        run_remix(datadir=Path(base_dir).joinpath(TESTCASE_PATH).as_posix(), 
                    sourcedir=source_directory.as_posix(),
                    docfile=doc_file, roundts=1)
                
        if os.name == "posix":
            m2t_call = "model2tex.sh"
            doc_file = doc_file.as_posix()
        else:
            from pathlib import WindowsPath
            m2t_call = "model2tex"
            doc_file =str(WindowsPath(doc_file))
        # FIXME: Apparently absolute directories are a nono for gams ...
        model2tex = Path(shutil.which(m2t_call)).parent.joinpath("model2tex.py").as_posix()
        wd = os.getcwd()
        os.chdir(base_dir)
        return_code = sp.run(["python", model2tex, DOCFILE_PATH, "-m", "remix"]).returncode
        os.chdir(wd)
        if return_code != 0:
            ValueError("Something went wrong with model2tex")
        output_name = Path(base_dir).joinpath(DOCFILE_PATH).as_posix() + ".tex"
        if not Path(output_name).exists():
            ValueError(f"Something went wrong with model2tex {output_name} was not created")
    else:
        raise ValueError(f"The given directory: {base_dir} does not exists.")


if __name__ == "__main__":
    main()