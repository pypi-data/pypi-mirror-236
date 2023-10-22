import typer
import requests
from sty import fg
import os
import platform
import pyperclip

app = typer.Typer()
api_key = ""


@app.command()
def auth(token: str):
    if platform.system() == "Windows":
        try:
            if not os.path.exists(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker")):
                os.mkdir(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker"))
            if not os.path.exists(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt")):
                open(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt"), "x")
            with open(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt"), "a+") as f:
                f.seek(0)
                f.truncate(0)
                f.write(token)
            typer.echo(f"{fg.li_green}Token successfully configured.{fg.rs}")
        except Exception as e:
            typer.echo(fg.red + str(e) + fg.rs)
            typer.echo(f"{fg.li_red}Failed to configure API key. Try again later.{fg.rs}")
            raise typer.Exit(code=1)
    else:
        typer.echo(f"{fg.li_red}The ServerSeeker CLI currently only supports Windows.{fg.rs}")

@app.command()
def whereis(target: str, uuid: bool = False, copy: bool = False):
    if os.path.exists(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt")):
        with open(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt"), "r") as f:
            try:
                if uuid:
                    response = requests.post("https://api.serverseeker.net/whereis", json={"uuid": target}, headers={"Authorization": f"Bearer {f.read()}"})
                else:
                    response = requests.post("https://api.serverseeker.net/whereis", json={"name": target}, headers={"Authorization": f"Bearer {f.read()}"})
                
                if copy:
                    pyperclip.copy(response.text)
                    typer.echo(f"{fg.li_green}Copied response to clipboard.{fg.rs}")
                else:
                    typer.echo(response.json())
            except Exception as e:
                typer.echo(fg.red + str(e) + fg.rs)
                typer.echo(f"{fg.li_red}Failed to send request. Try again later.{fg.rs}")
                raise typer.Exit(code=1)
    else:
        typer.echo(f"{fg.li_green}Please configure your API key via {fg.li_yellow}'serverseeker auth <api_key>'{fg.li_green} first.{fg.rs}")
        raise typer.Exit(code=1)


@app.command()
def search(online_players: str = "[0, \"inf\"]", max_players: str = "[0, \"inf\"]", cracked: bool = False, protocol: int = 764, online_after: int = 0, software: str = "any", country_code: str = "", description: str = "", copy: bool = False):
    if os.path.exists(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt")):
        with open(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt"), "r") as f:
            try:
                response = requests.post("https://api.serverseeker.net/servers", json={"online_players": eval(online_players),"max_players": eval(max_players), "cracked": cracked, "protocol": protocol, "online_after": online_after, "country_code": country_code, "description": description}, headers={"Authorization": f"Bearer {f.read()}"})
                if copy:
                    pyperclip.copy(response.text)
                    typer.echo(f"{fg.li_green}Copied response to clipboard.{fg.rs}")
                else:
                    typer.echo(response.json())
            except Exception as e:
                typer.echo(fg.red + str(e) + fg.rs)
                typer.echo(f"{fg.li_red}Failed to send request. Try again later.{fg.rs}")
                raise typer.Exit(code=1)
    else:
        typer.echo(f"{fg.li_green}Please configure your API key via {fg.li_yellow}'serverseeker auth <api_key>'{fg.li_green} first.{fg.rs}")
        raise typer.Exit(code=1)


@app.command()
def info(ip: str, port: int = 25565, copy: bool = False):
    if os.path.exists(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt")):
        with open(os.path.join(os.getenv("LOCALAPPDATA"), "ServerSeeker", "api_key.txt"), "r") as f:
            try:
                response = requests.post("https://api.serverseeker.net/server_info", json={"ip": ip, "port": port}, headers={"Authorization": f"Bearer {f.read()}"})
                if copy:
                    pyperclip.copy(response.text)
                    typer.echo(f"{fg.li_green}Copied response to clipboard.{fg.rs}")
                else:
                    typer.echo(response.json())
            except Exception as e:
                typer.echo(fg.red + str(e) + fg.rs)
                typer.echo(f"{fg.li_red}Failed to send request. Try again later.{fg.rs}")
                raise typer.Exit(code=1)
    else:
        typer.echo(f"{fg.li_green}Please configure your API key via {fg.li_yellow}'serverseeker auth <api_key>'{fg.li_green} first.{fg.rs}")
        raise typer.Exit(code=1)


app()