#
# server.py - DeGirum Python SDK: Degirum AI Server control
# Copyright DeGirum Corp. 2022
#
# Implements DeGirum AI Server start functionality
#


"""
DeGirum AI server launcher and model downloader.

!!! note

    The functionality of this module is now exposed via PySDK CLI.

The purpose of this module is to start DeGirum AI server:
```
python -m degirum.server --zoo <local zoo path> [--port <server TCP port>]
```

Keyword Args:
    
    --zoo (str): Path to a local model zoo directory, containing AI models you want your AI server to serve.
        
        - One possible way to fill local model zoo directory is to download models from a model zoo repo using 
        `download_models()` function and provide the path to the local zoo directory as `--zoo` parameter.
    
    --port (int): TCP port to bind server to. 
        
        - Default is 8778.

- When AI server is started, it runs indefinitely. 
- If you started the server from a terminal, you may press `Enter` to shut it down. 
- If you started the server headless (for example, as a service), then to shut down the server you need to kill 
the Python process which runs the server.

The module also exposes `download_models()` function which can be used to prepare local model zoo directory to be 
served by AI server:

- You first download models from the model zoo repo of your choice into some local directory of your choice by 
calling [degirum.server.download_models][] function.
- Then you start the AI server providing the path to that local directory as `--zoo` parameter.

"""

import argparse
import pdb
from pathlib import Path

from .CoreClient import Server
from .zoo_manager import ZooManager
from ._zoo_accessor import _CloudServerZooAccessor


def download_models(
    path: str, *, url: str = ZooManager._default_cloud_url, token: str = "", **kwargs
):
    """Download all models from a model zoo repo specified by the URL.

    Args:
        
        path: Local filesystem path to store models downloaded from a model zoo repo.
        
        url: Zoo repo URL. 
            
            - If not specified, then DeGirum public model zoo URL will be used.
        
        token: Zoo repo authorization token.
        
    Keyword Args:

        model_family (str): Model family name filter. 
        
            - When you pass a string, it will be used as search substring in the model name. For example, `"yolo"`, `"mobilenet"`.
            - You may also pass `re.Pattern`. In this case it will do regular expression pattern search.
        
        device (str): Target inference device -- string or list of strings of device names.
        
            - Possible names: `"orca"`, `"orca1"`, `"cpu"`, `"gpu"`, `"edgetpu"`, `"dla"`, `"dla_fallback"`, `"myriad"`.
        
        precision (str): Model calculation precision -- string or list of strings of model precision labels.
        
            - Possible labels: `"quant"`, `"float"`.
        
        pruned (str): Model density -- string or list of strings of model density labels.
        
            - Possible labels: `"dense"`, `"pruned"`.
        
        runtime (str): Runtime agent type -- string or list of strings of runtime agent types.
        
            - Possible types: `"n2x"`, `"tflite"`, `"tensorrt"`, `"openvino"`.
    """
    root_path = Path(path)
    root_path.mkdir(exist_ok=True)
    zoo = _CloudServerZooAccessor(url=url, token=token)
    print(f"Downloading models\n  from '{url}'\n  into '{path}'")
    n = 0
    for m in zoo.list_models(**kwargs):
        zoo.download_model(m, root_path)
        print(m)
        n += 1
    print(f"Downloaded {n} model(s)")


def _download_zoo_run(args):
    """
    Download all models from a model zoo repo

    Args:

        args: argparse command line arguments
    """

    download_models(
        args.path,
        url=args.url,
        token=args.token,
        model_family=args.model_family,
        device=args.device,
        runtime=args.runtime,
        precision=args.precision,
        pruned=args.pruned,
    )


def _download_zoo_args(parser):
    """
    Define download-zoo subcommand arguments

    Args:

        parser: argparse parser object to be stuffed with args
    """
    parser.add_argument(
        "--path",
        default=".",
        help="local filesystem path to store models downloaded from a model zoo repo",
    )
    parser.add_argument(
        "--url",
        default=ZooManager._default_cloud_url,
        help="cloud model zoo URL; if not specified then DeGirum public model zoo URL will be used",
    )
    parser.add_argument(
        "--token",
        help="model zoo repo authorization token",
    )
    parser.add_argument(
        "--model_family",
        help="model family name filter: model name substring or regular expression",
    )
    parser.add_argument(
        "--device",
        help="target inference device filter",
        choices=["ORCA", "ORCA1", "CPU", "EDGETPU", "MYRIAD"],
    )
    parser.add_argument(
        "--runtime",
        help="runtime agent type filter",
        choices=["N2X", "TFLITE", "OPENVINO"],
    )
    parser.add_argument(
        "--precision",
        help="model calculation precision filter",
        choices=["QUANT", "FLOAT"],
    )
    parser.add_argument(
        "--pruned",
        help="model density filter",
        choices=["PRUNED", "DENSE"],
    )
    parser.set_defaults(func=_download_zoo_run)


def _server_run(args):
    """
    Start and run AI server

    Args:

        args: argparse command line arguments
    """

    localhost = lambda: "127.0.0.1" + "" if args.port < 0 else f":{args.port}"

    if args.command == "start":
        import threading

        # start server
        with Server(args.port, args.zoo) as server:
            server.start()

            def keyboard_handler():
                try:
                    input(
                        f"DeGirum AI Server is started at {'default port' if args.port < 0 else 'port ' + str(args.port)}\n"
                        + f"serving model zoo in '{args.zoo}' directory.\n"
                        + "Press Enter to stop the server"
                    )
                    server.stop(False)  # no wait
                    print("Requesting server to stop...")
                except BaseException:
                    pass

            if not args.quiet:
                threading.Thread(
                    target=keyboard_handler,
                    name="dg-server-keyboard_handler",
                    daemon=True,
                ).start()

            try:
                server.wait()
            except BaseException:
                pass

            if not args.quiet:
                print("\nServer stopped")

    elif args.command == "rescan-zoo":
        # send rescan model zoo command to server on localhost
        from .aiclient import zoo_manage

        zoo_manage(localhost(), {"rescan": 1})

    elif args.command == "shutdown":
        # send shutdown command to server on localhost
        from .aiclient import shutdown

        shutdown(localhost())


def _server_args(parser):
    """
    Define server subcommand arguments

    Args:
        parser: argparse parser object to be stuffed with args
    """
    parser.add_argument(
        "command",
        nargs="?",
        choices=["start", "rescan-zoo", "shutdown"],
        default="start",
        help="server command: start server; rescan local server model zoo; shutdown local server",
    )
    parser.add_argument(
        "--port", type=int, default=-1, help="[start] TCP port to bind to"
    )
    parser.add_argument(
        "--quiet", action="store_true", help="[start] do not display any output"
    )
    parser.add_argument(
        "--zoo", default=".", help="[start] model zoo directory to serve models from"
    )
    parser.set_defaults(func=_server_run)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=f"{__file__}", description="DeGirum AI Server starter"
    )
    _server_args(parser)
    _server_run(parser.parse_args())
