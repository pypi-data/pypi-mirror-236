import os
import shutil


# did one notebook get uploaded
def one_notebook(path):
    return path.endswith(".ipynb")


# main handler for uploads
def handle_upload(path):
    if one_notebook(path):
        notebook_name = path.split(".")[0]
        os.mkdir(notebook_name)
        shutil.move(path, notebook_name)
        return notebook_name
