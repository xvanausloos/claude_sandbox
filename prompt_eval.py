from dotenv import load_dotenv
from anthropic import Anthropic
import json
from statistics import mean

load_dotenv()

client = Anthropic(max_retries=3)
model = "claude-haiku-4-5"

# Helpers functions 
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, stop_sequences=None):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
        stop_sequences=stop_sequences,
    )
    return "Chat:" + message.content[0].text

def generate_dataset():
    prompt = """
    Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
    that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
    each representing task that requires Python, JSON, or a Regex to complete.

    Example output:
    ```json
    [
        {
            "task": "Description of task",
        },
        ...additional
    ]
    ```

    * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
    * Focus on tasks that do not require writing much code

    Please generate 3 objects.
    """

    messages = []
    add_user_message(messages, prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text.removeprefix("Chat:"))

def run_prompt(test_case):
    """Merge prompt and test case input then return the output from the model."""
    prompt = f"""
    Please solve the following task :
    {test_case["task"]}
    """
    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output


def run_test_case(test_case):
    """Call run_prompt and grades the results."""
    output = run_prompt(test_case)
    # TODO grading
    score = 10
    
    return {
        "output": output,
        "test_case": test_case,
        "score": score,
    }

def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []

    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)

    average_score = mean([result["score"] for result in results])
    print(f"Average score: {average_score}")

    return results

# Function to grade a test case + output using a model
def grade_by_model(test_case, output):
    eval_prompt = f"""
You are an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.

Original Task:
<task>
{test_case["task"]}
</task>

Solution to Evaluate:
<solution>
{output}
</solution>

Output Format
Provide your evaluation as a structured JSON object with the following fields, in this specific order:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement
- "reasoning": A concise explanation of your overall assessment
- "score": A number between 1-10

Respond with JSON. Keep your response concise and direct.
Example response shape:
{{
    "strengths": string[],
    "weaknesses": string[],
    "reasoning": string,
    "score": number
}}
    """

    messages = []
    add_user_message(messages, eval_prompt)
    add_assistant_message(messages, "```json")
    text = chat(messages, stop_sequences=["```"])
    return json.loads(text.removeprefix("Chat:"))


dataset = generate_dataset()

with open("dataset.json", "r") as f:
    dataset = json.load(f)

results = run_eval(dataset)

print(json.dumps(results, indent=2))

graded_results = []
for result in results:
    graded_result = grade_by_model(result["test_case"], result["output"])
    graded_results.append({
        "test_case": result["test_case"],
        "output": result["output"],
        "grade": graded_result,
    })
print(json.dumps(graded_results, indent=2))


