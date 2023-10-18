import json
import os
import keyring
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from chattdd.tools import extract_json


def initialize_model(model_name=None):
    if not model_name:
        model_name = os.getenv('CHATTDD_MODEL', 'text-davinci-003')  # Default model

    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        openai_api_key = keyring.get_password('openai', 'api_key')
        if not openai_api_key:
            openai_api_key = input("Please enter your OpenAI API key: ")
            keyring.set_password('openai', 'api_key', openai_api_key)
    
    os.environ['OPENAI_API_KEY'] = openai_api_key
    set_llm_cache(InMemoryCache())

    if model_name == 'text-davinci-003':
        model = OpenAI(model_name="text-davinci-003", max_tokens=3000, temperature=0, openai_api_key=openai_api_key)
    elif model_name == 'gpt-3.5-turbo':
        model = ChatOpenAI(model_name="gpt-3.5-turbo", max_tokens=30000, temperature=0, openai_api_key=openai_api_key)
    elif model_name == 'gpt-4':
        model = ChatOpenAI(model_name="gpt-4", max_tokens=30000, temperature=0, openai_api_key=openai_api_key)
    else:
        raise ValueError(f'Unsupported model: {model_name}')
    
    return model


def generate_test_code(model, user_input):
    template = """
    You are a code generator that follows all principles of Test Driven Development. 
    You adhere to PEP 8.
    Your task is to generate function code AND pytest test code, and place it in a JSON return without any explanations or comments. 
    When writing the pytest file please include required setup or teardown code and use a descriptive test function name.
    The user will prompt you with a required task. Imagine that the user already has a python function that solves this requirement. DO NOT write the function. Your job is just to write the pytest for such a function.
    Your reply will be JSON with 7 elements only, absolutely no comments.:
     1. original_request: the original request from the user. No changes.
     2. function_name: a short function name that reflects the users request.
     3. test_code: python code file that includes a single function, namely the pytest for a function that would test a function that soleves the users requirements. The function to test will be found in the src folder with a filename you suggest. No comments. 
     4. test_file_name: a file name for the pytest test code.
     5. pytest_result: an empty string (we will fill this later)
     6. function_code: python code file that includes a single function, namely the function that the pytest is testing. The function solves the users requirements. No comments.
     7. function_file_path:  path and file name used in the test file.

     
    You will return this in a JSON format. Keys are: 
    "original_request, "function_name", "test_code", "test_file_name", "pytest_result", "function_code", "function_file_path"

    Return only the JSON object with no additional text or formatting.

    """
    generated_test_code_prompt = ChatPromptTemplate.from_messages(
        [("system", template), ("human", f"{user_input}")]
    )
    chain = generated_test_code_prompt | model | StrOutputParser()

    generated_test_code = chain.invoke({'user_input': user_input})
    test_code_json = extract_json(generated_test_code)
    return json.loads(test_code_json)

def review_test_code(model, original_request, function_name, test_code):
    template = """
    Your task as an Pytest and TDD expert is to evaluate a pytest file. The file should contain a pytest to test a function to solve the following requirement: {original_request}

    You don't have the function code, only the pytest code. In other words, the test code is missing the implementation of {function_name}. This is correct and should not reject the test code.
    Here's the pytest file contents represented in a string, it contains escape sequences that you should ignore: 

    "
    {test_code}
    "

    Reject the test if one or more of the following occur: 
    - There are syntax errors in the test code
    - The test isn't following best practice for TDD with Pytest. 
    - The test fails to test a function that solves what the user asked for, {original_request}

    You will return complete JSON containing the following two elements "result" and "comment":
    1. result: "GO" if the test can be accepted. "REJECTED" if the test isn't up your standards.
    2. comment: an evaluation of the test code and the test's overall performance for testing a function to "{original_request}

    """
    generated_test_review_prompt = ChatPromptTemplate.from_messages(
        [("system", template)]
    )
    chain = generated_test_review_prompt | model | StrOutputParser()
    chain_test_review = chain.invoke({'original_request': original_request,'function_name': function_name, 'test_code': test_code})
    return_json = extract_json(chain_test_review)
    return json.loads(return_json)


if __name__ == "__main__":
    model = initialize_model()
    #user_input = "sort a list alphabetically descending order"
    user_input = "sort a list of objects alphabetically"
    test_code_json = generate_test_code(model, user_input)
    original_request = test_code_json['original_request']
    function_name = test_code_json['function_name']
    test_code = test_code_json['test_code']
    test_review_json = review_test_code(model, original_request, function_name, test_code)

    print("Generated Test Code JSON:")
    print(json.dumps(test_code_json, indent=4))
    print("\nTest Review JSON:")
    print(json.dumps(test_review_json, indent=4))
