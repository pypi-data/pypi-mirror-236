#!/bin/env python
import typer
from rich import print

from .project import app as project

app = typer.Typer()
app.add_typer(project, name= "project")

def main():
    app()


if __name__ == "__main__":
    main()
