import json
import sys
from typing import Any, Dict
import click
from .util import BE_HOST, get_client, FE_HOST, list_test_suites
from gql import gql
import boto3
import requests


@click.group()
def suite():
    """
    Start, create, or view tests and test suites
    """
    pass


def parse_suite_interactive():
    title = click.prompt("Test Suite Title")
    while title == "":
        title = click.prompt("Title cannot be empty. Reenter")

    description = click.prompt("Test Suite Description")

    i = 1
    keep_generating_prompts = True
    tests = []
    while keep_generating_prompts:
        click.secho(f"---Test {i}---", bold=True)
        input_under_test = click.prompt("Input under test (e.g. the prompt)")

        keep_generating_criteria = True
        j = 1
        checks = []
        while keep_generating_criteria:
            # TODO: Validation
            operator = click.prompt(f"Operator {j}")
            # TODO: Skip based on operator
            criteria = click.prompt(f"Criteria {j}")
            checks.append({"criteria": criteria, "operator": operator})
            j += 1

            keep_generating_criteria = click.confirm("Keep Generating Checks?")

        i += 1

        tests.append({"input_under_test": input_under_test, "checks": checks})
        keep_generating_prompts = click.confirm("Keep generating tests?")

    return {"title": title, "description": description, "tests": tests}


def parse_suite_file(file):
    # TODO: Validate file format
    return json.load(file)


def upload_files(data: Dict[str, Any]):
    # Map from file path to file id
    files = {}
    for test in data["tests"]:
        if "file_under_test" in test:
            file_path = test["file_under_test"]
            with open(file_path, "rb") as f:
                response = requests.post(f"{BE_HOST}/upload_file/", files={"file": f})
                if response.status_code != 200:
                    raise Exception(f"Failed to upload file {file_path}")
                file_id = response.json()["file_id"]
                files[file_path] = file_id
    return files


def create_test_suite(data: Dict[str, Any]) -> str:
    query = gql(
        f"""
    mutation createTestSuite {{
        updateTestSuite(
            description: "{data['description']}",
            testSuiteId: "0",
            title: "{data['title']}"
        ) {{
            testSuite {{
            description
            id
            org
            title
            }}
        }}
    }}
    """
    )
    result = get_client().execute(query)
    suite_id = result["updateTestSuite"]["testSuite"]["id"]
    return suite_id


def add_tests(data, files, suite_id):
    for test in data["tests"]:
        # TODO: Escape chars better
        if "file_under_test" in test:
            file_path = test["file_under_test"]
            input_under_test = files[file_path]
            input_under_test_type = "file"
        else:
            input_under_test = test["input_under_test"]
            input_under_test_type = "raw"

        # TODO: avoid double json
        checks = json.dumps(json.dumps(test["checks"]))
        # TODO: Do this server side

        sample_output = test["sample_output"] if "sample_output" in test else ""

        query = gql(
            f"""
        mutation addUpdateTest {{
              updateTest(
                  sampleOutput: {json.dumps(sample_output)},
                  checks: {checks}, 
                  inputUnderTest: {json.dumps(input_under_test)}, 
                  inputUnderTestType: "{input_under_test_type}",
                  testId: "0",
                  testSuiteId: "{suite_id}") {{
                  test {{
                    checks
                    inputUnderTest
                    testId
                  }}
                }}
            }}
            """
        )
        get_client().execute(query)
        # TODO: Check response?


@click.command()
@click.option(
    "--interactive",
    "-i",
    is_flag=True,
    help="Enable interactive mode instead of reading from file",
)
@click.argument("file", type=click.File("r"), required=False)
def create(interactive: bool, file: str):
    """
    Creates a new test suite.

    There are two modes. In normal operation, inputs are read from a JSON file:

    \tprl suite create <filename>

    In interactive mode, the user is prompted for values:

    \tprl suite create --interactive

        Requires authentication to use.
    """
    # try:
    if not interactive and file is None:
        click.echo(
            "Either --interactive must be passed, or an input file should be specified"
        )
        sys.exit(1)

    click.echo("Creating test suite...")

    if interactive:
        data = parse_suite_interactive()
    else:
        data = parse_suite_file(file)

    files = upload_files(data)

    suite_id = create_test_suite(data)
    add_tests(data, files, suite_id)
    # Execute the query on the transport
    click.secho("Successfully created test suite.", fg="green")
    click.secho(f"{FE_HOST}/view?test_suite_id={suite_id}", bold=True)

    # except Exception as e:
    #     click.secho("Suite Creation Failed. Error: " + str(e), fg="red")


@click.command()
def list_():
    """
    List test suites associated with this organization
    """
    suites = list_test_suites()

    suite_text = "\n".join([f"{i}: {s['title']}" for i, s in enumerate(suites)])
    click.echo(suite_text)


suite.add_command(create)
suite.add_command(list_, "list")
