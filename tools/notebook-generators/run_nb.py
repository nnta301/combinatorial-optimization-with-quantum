import sys
import nbformat
from nbclient import NotebookClient

for path in sys.argv[1:]:
    nb = nbformat.read(path, as_version=4)
    NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": "."}}).execute()
    nbformat.write(nb, path)
    print("executed", path)
