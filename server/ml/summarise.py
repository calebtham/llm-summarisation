import html
import re
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.callbacks import get_openai_callback
import tiktoken

LARGE_CONTEXT_MODEL = "gpt-3.5-turbo-16k"
DEFAULT_MODEL = "gpt-3.5-turbo"


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def summarise(text):
    '''Summarise text using GPT-3.5'''

    text = clean_text(text)
    tokens = num_tokens_from_string(text, DEFAULT_MODEL)

    if tokens > 8000:
        return "Text too long. Not allowed for the time being."

    model = DEFAULT_MODEL if tokens < 4000 else LARGE_CONTEXT_MODEL

    llm = ChatOpenAI(temperature=0, model_name=model)

    prompt_template = \
        """Write a concise summary of the following in bullet point form. The following text was taken from a website, so there may be redundant website information. Extract only the most important content information.:
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
