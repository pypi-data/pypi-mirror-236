from hhat_lang.hhat_parsing import parse_code
from hhat_lang.hhat_semantics import Analysis
from hhat_lang.hhat_eval import Eval
from hhat_lang.hhat_new_ast import AST
from hhat_lang.hhat_memory import R
from hhat_lang import __version__
import click


def execute_parsing_code(c: str, verbose: bool = False) -> AST:
    pc_ = parse_code(c)
    if verbose:
        print(f"- code:\n{c}\n")
        print(f"- parsed code:\n{pc_}\n")
    return pc_


def execute_analysis(pc: AST, verbose: bool = False) -> R:
    if verbose:
        print(f"- analysis (pre-evaluation):")
    analysis = Analysis(pc)
    res_ = analysis.run()
    print("\n")
    return res_


def execute_eval(c: R) -> None:
    ev_ = Eval(c)
    print("- executing code:\n")
    ev_.run()


def run_codes(c: str, verbose: bool = False) -> None:
    pc_ = execute_parsing_code(c, verbose)
    pev_ = execute_analysis(pc_, verbose)
    print("-" * 80)
    execute_eval(pev_)


@click.group(invoke_without_command=True, context_settings=dict(ignore_unknown_options=True))
@click.argument("file", type=click.Path(exists=True), required=False)
@click.option("-v", "--version", "version", is_flag=True)
@click.option("--verbose", "verbose", is_flag=True)
def main(file, version, verbose):
    if version:
        click.echo(f"H-hat version {__version__}")
    else:
        if file:
            run_codes(file, verbose=verbose)
        else:
            # TODO: make a REPL?
            pass
