import html
import re
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
import tiktoken

MODEL = "gpt-3.5-turbo-16k"

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def summarise(text):
    '''Summarise text using GPT-3.5'''
    text = clean_text(text)
    
    if num_tokens_from_string(text, MODEL) > 1000:
        return "Text too long. Not allowed for the time being."

    llm = ChatOpenAI(temperature=0, model_name=MODEL)

    prompt_template = \
    """Write a concise summary of the following in bullet point form:
    "{text}"
    CONCISE SUMMARY:"""
    
    prompt = PromptTemplate.from_template(prompt_template)

    chain = LLMChain(llm=llm, prompt=prompt)

    with get_openai_callback() as cb:
        summary = chain.run(text)
        print(cb)

        return summary


def clean_text(text):
    '''Remove HTML tags and revert HTML escaped special characters to shorten token length'''

    # remove HTML tags
    text = re.sub("<[^<]*>", "", text)  # This is faster than Beautiful Soup

    # revert HTML escaped special characters
    text = html.unescape(text)

    text = text.replace(u'\xa0', u' ') \
        .replace("\\n", "\n") \
        .replace("\\t", "\t") \
        .replace("\\r", "\r") \
        .replace("\\", "")

    return text
