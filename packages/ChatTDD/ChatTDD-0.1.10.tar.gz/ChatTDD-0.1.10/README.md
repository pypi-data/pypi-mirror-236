
# ChatTDD

ChatTDD is a utility designed to help developers create Test-Driven Python code using Langchain and OpenAI. By entering a description of the functionality you need, ChatTDD will generate pytest code for that function. Additionally, it allows you to review and validate the generated test code using different models from OpenAI.

## Installation

To install ChatTDD, ensure you have Python 3.9 installed, then run the following command:

```markdown
pip install ChatTDD
```

## Configuration

Before using ChatTDD, you'll need to have an OpenAI API key. If you don't have one, you can obtain it from [OpenAI](https://beta.openai.com/signup/).

On the first run, ChatTDD will prompt you to enter your OpenAI API key, which will be saved for future use.

## Usage

Once installed, you can use the chattdd command to interact with the tool. Here's how to use ChatTDD:

### Select a Model
You can choose between three models: text-davinci-003, gpt-3.5-turbo, and gpt-4. 
To select a model, use the following command:

```markdown
chattdd model text-davinci-003
```

Your model selection will be remembered for future sessions.

### Output Folder

```markdown
chattdd outputfolder [folder_path]
```
Sets the root folder for generated files. If this is left blank, files will be saved in the specified relative paths without a leading folder.

### Generate Function and Test Code

```markdown
chattdd test-and-code "sort a list of objects alphabetically"
```

ChatTDD will create the necessary Python files under the `src` and `tests` directories respectively.

### Generate Only Test Code

```markdown
chattdd test "sort a list of objects alphabetically"
```

ChatTDD will create the necessary Python files under the `tests` directory.

## Contributing

If you'd like to contribute to the development of ChatTDD, please feel free to fork the repository and submit a pull request.

## License

ChatTDD is licensed under the MIT License. See the `LICENSE` file for more details.


