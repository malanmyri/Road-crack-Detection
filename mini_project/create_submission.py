import os
import zipfile
import pathlib

zipfile_path = "assignment_code.zip"


# If you create other files, edit this list to include them in the .zip file.
directories_to_include = [
    "data",
    "hyperparameters",
    "scripts",
]

extensions_to_include = [
    ".py",
    ".yaml",
    ".ipynb"
]

files_to_include = {
    "Mini_project": [".ipynb"],
    "baseline": [".yaml"],
}

def select_file(filename, extension):
    if len(extensions) == 1:
        return filename + extensions[0]
    options = {str(i): filename + extensions[i]
               for i in range(len(extensions))}
    filename = query("Which file would you like to add?", options)
    return filename


files_added = []

with zipfile.ZipFile(zipfile_path, "w") as fp:
    for dirpath in directories_to_include:
        for directory, subdirectories, filenames in os.walk(dirpath):
            for filename in filenames:
                filepath = os.path.join(directory, filename)
                if pathlib.Path(filepath).suffix in extensions_to_include:
                    fp.write(filepath)
                    print("Adding file:", filepath)

    for filename, extensions in files_to_include.items():
        filepath = select_file(filename, extensions)
        assert os.path.isfile(filepath),\
            f"Did not find path: {filepath}"
        fp.write(filepath)
        files_added.append(filepath)

def query(question, options):
    print(question)
    to_write = ["\n\t{}: {}".format(key, val) for key, val in options.items()]
    to_write = "".join(to_write)
    print("Options to select:" + to_write)
    answer = None
    while answer not in ("yes", "no"):
        answer_alternatives = ", ".join([str(key) for key in options.keys()])
        answer = input("Select an option [{}]:".format(answer_alternatives))
        answer = answer.strip()
        if answer not in options.keys():
            print("Answer is not in: {}".format(list(options.keys())))
            continue
        return options[answer]


# If you create other files, edit this list to include them in the .zip file.
