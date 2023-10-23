import click
import pytest
from chattdd.core import initialize_model, generate_test_code, review_test_code
from chattdd.tools import update_config, load_config, write_to_file

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Main entry point for ChatTDD CLI."""
    if ctx.invoked_subcommand is None:
        try:
            # Prompt user for function requirement if 'chattdd' is typed without any subcommands
            user_requirement = click.prompt("Please enter the functional requirement")
            ctx.invoke(test_and_code, user_requirement=(user_requirement,))
        except Exception as e:
            click.echo(f"An error occurred: {str(e)}")

@cli.command()
@click.argument('outputfolder')
def outputfolder(outputfolder):
    """Set output folder."""
    try:
        update_config('OUTPUTFOLDER', outputfolder)
        click.echo(f'Output folder set to {outputfolder}')
    except Exception as e:
        click.echo(f"Failed to set output folder. Error: {str(e)}")

@cli.command()
@click.argument('model_name', type=click.Choice(['text-davinci-003', 'gpt-3.5-turbo', 'gpt-4'], case_sensitive=False))
def model(model_name):
    """Select a model."""
    try:
        update_config('CHATTDD_MODEL', model_name)
        click.echo(f'Model set to {model_name}')
    except Exception as e:
        click.echo(f"Failed to set model. Error: {str(e)}")

def generate_and_save(user_requirement, save_function_code=True):
    try:
        config = load_config()
        model_name = config['CHATTDD_MODEL']
        model = initialize_model(model_name)

        click.echo(f"\nUsing {model_name} to create test code for function: {user_requirement}\n")
        generated_test_code_output = generate_test_code(model, user_requirement)

        test_code = generated_test_code_output.get('test_code')
        if not test_code:
            click.echo(f"\n{generated_test_code_output.get('comment', 'No comment available')}") 
            return

        review_output = review_test_code(
            model=model,
            original_request=generated_test_code_output['original_request'],
            function_name=generated_test_code_output['function_name'],
            test_code=test_code
        )

        review_result = review_output.get('result')
        click.echo(f"\nComments on the test generated: {review_output.get('comment', 'No comment available')}")
        if review_result == "GO":
            write_to_file(test_code, generated_test_code_output['test_file_name'])

            click.echo(f"\nGenerated test for function: {generated_test_code_output['function_name']}")

            if save_function_code:
                write_to_file(generated_test_code_output['function_code'], generated_test_code_output['function_file_name'])
                click.echo(f"..also generated function: {generated_test_code_output['function_name']}")

            pytest.main(['-v'])
    except Exception as e:
        click.echo(f"An error occurred during generation: {str(e)}")

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
