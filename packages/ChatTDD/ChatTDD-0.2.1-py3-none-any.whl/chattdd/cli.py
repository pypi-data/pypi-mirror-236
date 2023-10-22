import click
import pytest
from chattdd.core import initialize_model, generate_test_code, review_test_code
from chattdd.tools import update_config, load_config, write_to_file

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Main entry point for ChatTDD CLI."""
    if ctx.invoked_subcommand is None:
        # Prompt user for function requirement if 'chattdd' is typed without any subcommands
        user_requirement = click.prompt("Please enter the functional requirement")
        ctx.invoke(test_and_code, user_requirement=user_requirement.split())

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

def generate_and_save(user_requirement, save_function_code=True):
    config = load_config()
    model_name = config['CHATTDD_MODEL']
    model = initialize_model(model_name)

    while True:
        click.echo(f"\nUsing {model_name} to create test code for function: {user_requirement}\n")
        generated_test_code_output = generate_test_code(model, user_requirement)
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

    write_to_file(generated_test_code_output['test_code'], generated_test_code_output['test_file_name'])

    click.echo(f"\nGenerated test for function: {generated_test_code_output['function_name']}")

    if save_function_code:
        write_to_file(generated_test_code_output['function_code'], generated_test_code_output['function_file_name'])
        click.echo(f"..also generated function: {generated_test_code_output['function_name']}")
    
    pytest.main(['-v'])

@cli.command()
@click.argument('user_requirement', nargs=-1)
def test_and_code(user_requirement):
    """Generate function and Pytest"""
    user_requirement_str = ' '.join(user_requirement)
    generate_and_save(user_requirement_str)

@cli.command()
@click.argument('user_requirement', nargs=-1)
def test(user_requirement):
    """Generate Pytest"""
    user_requirement_str = ' '.join(user_requirement)
    generate_and_save(user_requirement_str, save_function_code=False)

if __name__ == "__main__":
    cli()