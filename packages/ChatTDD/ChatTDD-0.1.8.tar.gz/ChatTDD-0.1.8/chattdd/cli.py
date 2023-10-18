import click
import os
import pytest
from chattdd.core import initialize_model, generate_test_code, review_test_code
from chattdd.file_handler import write_to_file
from chattdd.tools import update_config

@click.group()
def cli():
    pass


@cli.command()
@click.argument('outputfolder')
def outputfolder(outputfolder):
    """Set output folder."""
    update_config('OUTPUTFOLDER', outputfolder)
    click.echo(f'Output folder set to {outputfolder}')


@cli.command()
@click.argument('model_name', type=click.Choice(['text-davinci-003', 'gpt-3.5-turbo', 'gpt-4'], case_sensitive=False))
def model(model_name):
    """Select a model."""
    update_config('CHATTDD_MODEL', model_name)
    click.echo(f'Model set to {model_name}')


def generate_and_save(description_str, save_function_code=True):
    model_name = os.getenv('CHATTDD_MODEL', 'text-davinci-003') 
    model = initialize_model(model_name)

    while True:
        click.echo(f"\nUsing {model_name} to create test code for function: {description_str}\n")
        generated_test_code_output = generate_test_code(model, description_str)
        review_output = review_test_code(
            model=model,
            original_request=generated_test_code_output['original_request'],
            function_name=generated_test_code_output['function_name'],
            test_code=generated_test_code_output['test_code']
        )

        review_result = review_output.get('result')
        if review_result == 'GO' or review_result is None:
            click.echo(f"\nComments on the test generated: {review_output.get('comment')}")
            break

    test_file_path = generated_test_code_output['test_file_path']
    write_to_file(generated_test_code_output['test_code'], f'{test_file_path}')

    if save_function_code:
        function_filepath = generated_test_code_output['function_file_path']
        write_to_file(generated_test_code_output['function_code'], f'{function_filepath}')

    click.echo(f"\nGenerated test for function: {generated_test_code_output['function_name']}")
    pytest.main(['-v'])

@cli.command()
@click.argument('description', nargs=-1)
def test_and_code(description):
    """Generate function and Pytest"""
    description_str = ' '.join(description)
    generate_and_save(description_str)


@cli.command()
@click.argument('description', nargs=-1)
def test(description):
    """Generate Pytest"""
    description_str = ' '.join(description)
    generate_and_save(description_str, save_function_code=False)


if __name__ == "__main__":
    cli()