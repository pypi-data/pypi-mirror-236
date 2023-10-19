"""Main script to run others as subcommands."""
import fire

from bitfount import __version__
from bitfount.scripts.generate_schema import gen_schema
from bitfount.scripts.generate_yaml_specs import generate_yaml_specs
from bitfount.scripts.run_modeller import run as modeller_run
from bitfount.scripts.run_pod import run as pod_run
from bitfount.scripts.run_testing import evaluate_model


def run(*, version: bool = False) -> None:
    """Bitfount CLI.

    Run `bitfount` standalone in the CLI to see the available commands.

    Args:
        version: Prints bitfount version.
    """
    if version:
        print(__version__)
        return

    fire.Fire(
        {
            "generate_schema": gen_schema,
            "run_modeller": modeller_run,
            "run_pod": pod_run,
            "run_testing": evaluate_model,
            "generate_yaml_specs": generate_yaml_specs,
        }
    )


def main() -> None:
    """Main script entry point.

    This is required because `setup.py` must point to a function and it can't point to
    `run` directly because it hasn't been wrapped by `fire.Fire` yet.

    """
    fire.Fire(run, name="bitfount")


if __name__ == "__main__":
    main()
