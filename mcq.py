import os
import json
import pandas
import traceback
from langchain.chains import SequentialChain
from langchain_anthropic import ChatAnthropic,Anthropic
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import PyPDF2

from dotenv import load_dotenv
load_dotenv()
key=os.getenv('ANTHROPIC_API_KEY')

os.environ['ANTHROPIC_API_KEY']=key
anthropic_llm = ChatAnthropic(model = "claude-3-haiku-20240307")

with open('mcq_template.txt','r') as f:
    response_json=f.read()

TEMPLATE="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}
"""

quiz_promt=PromptTemplate(
    input_variables=['text','number','subject','tone','response_json'],
    template=TEMPLATE
)
quiz_chain=LLMChain(llm=anthropic_llm, prompt=quiz_promt, output_key="quiz", verbose=True)

TEMPLATE2="""
You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject", "quiz"], template=TEMPLATE)
review_chain=LLMChain(llm=anthropic_llm, prompt=quiz_evaluation_prompt, output_key="review", verbose=True)
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "subject", "tone", "response_json"],
                                        output_variables=["quiz", "review"], verbose=True,)

with open('sub_text.txt', 'r') as file:
    TEXT = file.read()

#response_json=json.dumps(response_json)

NUMBER=3
SUBJECT="biology"
TONE="simple"

from langchain.callbacks import get_openai_callback
#How to setup Token Usage Tracking in LangChain

response=generate_evaluate_chain(
    {
        "text": TEXT,
        "number": NUMBER,
        "subject":SUBJECT,
        "tone": TONE,
        "response_json": json.dumps(response_json)
    }
    )

print(response)
quiz=response.get("quiz")
quiz=json.loads(quiz)
quiz_table_data = []
for key, value in quiz.items():
    mcq = value["mcq"]
    options = " | ".join(
        [
            f"{option}: {option_value}"
            for option, option_value in value["options"].items()
            ]
        )
    correct = value["correct"]
    quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

for item in quiz_table_data:
    values = list(item.values())

    print(f'QS: {values[0]} \n choices:{values[1]} \n answer: {values[2]}')

