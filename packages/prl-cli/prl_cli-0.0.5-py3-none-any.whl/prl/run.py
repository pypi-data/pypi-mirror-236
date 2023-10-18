import click
from .auth import get_auth_token
from .util import BE_HOST, FE_HOST, list_test_suites
import requests


@click.group()
def run():
    """
    Commands relating to starting or viewing runs
    """
    pass


@click.command()
@click.option(
    "--use-sample-output",
    "-u",
    is_flag=True,
    help="Use a fixed set of outputs to test the evaluator itself",
)
def start(use_sample_output: bool):
    """
    Start a new run of a test suite.

    Optionally, if the test suite was defined with "sample_output" fields
    and if the --use-sample-output flag is passed, then it will
    use a fixed set of outputs instead of querying the model under test.
    This is useful to evaluate the performance of the evaluator itself.
    """
    suites = list_test_suites()
    click.echo("Test Suites:")
    click.echo("\n".join([f"{i}: {s['title']}" for i, s in enumerate(suites)]))

    idx = click.prompt("Enter the number of the test suite to run", type=int)
    while not 0 <= idx <= len(suites):
        idx = click.prompt("Invalid choice. Retry", type=int)
    suiteid = suites[idx]["id"]

    response = requests.post(
        url=f"{BE_HOST}/start_run/",
        headers={"Authorization": get_auth_token()},
        json={"test_suite_id": suiteid, "use_sample_output": use_sample_output},
    )

    if response.status_code == 200:
        run_id = response.json()["run_id"]
        click.secho("Successfully started run.", fg="green")
        click.secho(f"{FE_HOST}/results?run_id={run_id}", bold=True)
    else:
        click.secho("Could not start run", fg="red")


run.add_command(start)
