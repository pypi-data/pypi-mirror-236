import yaml
import click
from pandas import DataFrame
from subprocess import run as prun
from pathlib import Path
from rich.console import Console
from abml_cli.abml_yamler import generate_abml_file, generate_input_file, generate_subroutine_file
from abml_cli.abml_grids import get_parameters_list, generate_param_grid,flatten_dict
import glob
from os import remove, rename
from os.path import isfile
from yaml import safe_load
import logging
import sys
import time

c = Console()

parser_path = (Path(__file__).parents[0] / "abml_parser.py").resolve()

logger = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s]  %(message)s")
streamhandler = logging.StreamHandler(logging.StreamHandler())
streamhandler.setFormatter(logFormatter)
logger.addHandler(streamhandler)


@click.command()
@click.option("--file", "-f", help="abml-files", required=False, multiple=False)
@click.option("--debug", "-d", is_flag=True, show_default=True, default=False, help="debug mode")
def run(file, debug):

    if debug is True:
        logger.setLevel(logging.DEBUG)
        debug_flag = "--debug"
    else:
        logger.setLevel(logging.INFO)
        debug_flag = ""
    
    if file is None:
        files = glob.glob("*.abml")
    else:
        files = [file]

    params={}
    if Path("_env.abml").is_file():
        with open("_env.abml", mode="r", encoding="utf-8") as f:
            env = safe_load(f)
    
        params = env.get("parameters", {})
        
    for f in files:
        if not f.startswith("_"):
            generate_abml_file(f, **params)
            rendered = f'_{f.replace(".abml", "")}.render.abml'
            with open(rendered, mode="r", encoding="utf-8") as stream:
                data = yaml.safe_load(stream)
            
            if "subroutines" in data:
                subs = data["subroutines"]
                if isinstance(subs, str):
                    subs = [subs]
                
                for sub in subs:
                    name, ext = sub.split(".")
                    generate_subroutine_file(sub, filename=f'{name}_{f.replace(".abml", "")}.{ext}', **params)

            cwd = Path().cwd()
            cmd = f'abaqus cae nogui="{parser_path}" -- --yml "{cwd / rendered}" {debug_flag}'
            prun(cmd, shell=True, check=True)

        

    rpys = glob.glob("*.rpy*")
    recs = glob.glob("*.rec*")

    for file in rpys+recs:
        try:
            remove(file)
        except PermissionError:
            pass
            

@click.command()
@click.option("--file", "-f", help="abml-files", required=True, multiple=False)
def run_grid(file):
    params={}
    grids = {}
    if Path("_env.abml").is_file():
        with open("_env.abml", mode="r", encoding="utf-8") as f:
            env = safe_load(f)
    
        params = env.get("parameters", {})
        grids = env.get("grids", {})

    input_folder = grids.pop("input_folder", None)
    sub_folder = grids.pop("subroutine_folder", None)
    
    
    root = Path("grids")
    root.mkdir(exist_ok=True)

    for grid_name in grids:
        grid_path = root / Path(grid_name)
        grid_path.mkdir(exist_ok=True)
        
        params_list = get_parameters_list(params, grids[grid_name])
        df = DataFrame(map(flatten_dict, params_list))
        names = []
        for i, params_grid in enumerate(params_list):
            timestr = time.strftime("%Y%m%d-%H%M%S")
            names.append(timestr)
            path = grid_path / Path(f"{timestr}")
            path.mkdir(exist_ok=True)
            cwd = Path().cwd()
            
            if file.endswith(".abml"):
                filename = f'{file.split(".abml")[0]}.{path.name}'
                generate_abml_file(file, path=path, filename=filename, **params_grid)
                rendered = f"_{filename}.render.abml"
                cmd = f'abaqus cae nogui="{parser_path}" -- --yml "{cwd / path / rendered}" --path "{cwd / path}"'
                prun(cmd, shell=True, check=True)

                cae =  cwd / path / Path(file).with_suffix(".cae")
                cae_new = Path(cwd / path / f"{timestr}.cae")
                if cae_new.is_file():
                    cae_new.unlink()
                cae.rename(cae_new)

                jnl =  cwd / path / Path(file).with_suffix(".jnl")
                jnl_new = Path(cwd / path / f"{timestr}.jnl")
                if jnl_new.is_file():
                    jnl_new.unlink()
                jnl.rename(jnl_new)

                inp =  cwd / path / Path(file).with_suffix(".inp")
                inp_new = Path(cwd / path / f"{timestr}.inp")
                if inp_new.is_file():
                    inp_new.unlink()
                inp.rename(inp_new)

                with open(rendered, mode="r", encoding="utf-8") as stream:
                    data = yaml.safe_load(stream)

                if "subroutines" in data:
                    subs = data["subroutines"]
                    if isinstance(subs, str):
                        subs = [subs]

                    if len(subs) != 1:
                        raise ValueError(f"list length of subroutines in grid mode must be 1")
                    
                    for sub in subs:
                        name, ext = sub.split(".")
                        sub_name = f'{name}_{file.replace(".abml", "")}.{ext}'
                        generate_subroutine_file(sub, filename=sub_name, path=path,  **params)
                    
                    sub =  cwd / path / Path(sub_name)
                    sub_new = Path(cwd / path / f"{timestr}.for")
                    if sub_new.is_file():
                        sub_new.unlink()
                    sub.rename(sub_new)

            elif file.endswith(".inp"):
                filename = f'{path.name}'
                generate_input_file(file, path=path, filename=filename, **params_grid)

                inp_new = Path(cwd / path / f"{timestr}.inp")

            if input_folder is not None:
                Path(cwd / grid_path / input_folder).mkdir(exist_ok=True)
                Path(cwd / grid_path / input_folder / f"{timestr}.inp").write_bytes(inp_new.read_bytes())
            if sub_folder is not None:
                Path(cwd / grid_path / sub_folder).mkdir(exist_ok=True)
                Path(cwd / grid_path / sub_folder / f"{timestr}.for").write_bytes(sub_new.read_bytes())

        df["name"] = names
        df.set_index("name", inplace=True)
        df.to_csv(grid_path / "env.csv", sep=",")

    rpys = glob.glob("*.rpy*")
    recs = glob.glob("*.rec*")

    for file in rpys+recs:
        try:
            remove(file)
        except PermissionError:
            pass

