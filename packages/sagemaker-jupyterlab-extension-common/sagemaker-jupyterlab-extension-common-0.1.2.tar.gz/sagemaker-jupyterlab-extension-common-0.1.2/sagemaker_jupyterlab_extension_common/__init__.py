import json
from os import path
from pathlib import Path

from ._version import __version__

HERE = Path(__file__).parent.resolve()
with (HERE / "labextension" / "package.json").open(encoding="utf-8") as fid:
    data = json.load(fid)


# Path to the frontend JupyterLab extension assets
def _jupyter_labextension_paths():
    return [{"src": "labextension", "dest": data["name"]}]


def _jupyter_server_extension_points():
    return [{"module": "sagemaker_jupyterlab_extension_common"}]


# Entrypoint of the server extension
def _load_jupyter_server_extension(nb_app):
    nb_app.log.info(f"Loading SageMaker Studio Lab server extension {__version__}")
    web_app = nb_app.web_app
    base_url = web_app.settings["base_url"]


load_jupyter_server_extension = _load_jupyter_server_extension
