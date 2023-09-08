import html
import re
import tiktoken
from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.callbacks import get_openai_callback
from langchain.text_splitter import RecursiveCharacterTextSplitter

LARGE_CONTEXT_MODEL = "gpt-3.5-turbo-16k"
DEFAULT_MODEL = "gpt-3.5-turbo"


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(DEFAULT_MODEL)
    num_tokens = len(encoding.encode(string))
    return num_tokens


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


def summarise(text):
    '''Summarise text using GPT-3.5'''

    text = clean_text(text)
    no_tokens = num_tokens_from_string(text)

    if no_tokens > 15900:
        return map_reduce_summarise(text)
    else:
        model = DEFAULT_MODEL if no_tokens < 3900 else LARGE_CONTEXT_MODEL
        return stuff_summarise(text, model)


def log_chain_run(summary_chain, text):
    '''Runs a chain and logs the callback'''

    with get_openai_callback() as cb:
        summary = summary_chain.run(text)
        print(cb)

    return summary


def stuff_summarise(text, model):
    '''Summarise text using stuffing method'''

    llm = ChatOpenAI(temperature=0, model_name=model)

    prompt_template = \
        """Write a concise summary of the following in bullet point form. 
        The following text was taken from a website, so there may be redundant website information that should be avoided. 
        Extract only the most important content information.
        There is no need to state "The article says" or "The article states" or similar before each bullet point.
        TEXT:"{text}"
        CONCISE BULLET POINT SUMMARY:"""

    prompt = PromptTemplate.from_template(prompt_template)

    summary_chain = LLMChain(llm=llm, prompt=prompt)

    return log_chain_run(summary_chain, text)


def map_reduce_summarise(text):
    '''Summarise text using map reduce method'''

    llm = ChatOpenAI(temperature=0, model_name=LARGE_CONTEXT_MODEL)

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        length_function=num_tokens_from_string,
        chunk_size=3500,
        chunk_overlap=10,
        add_start_index=True,
    )

    docs = text_splitter.create_documents([text])
    print(f"Number of docs: {len(docs)}")

    # Map
    map_custom_prompt = \
        """Summarize the following text in a clear and concise way.
        The following text was taken from a website, so there may be redundant website information. 
        Extract only the most important content information.
        TEXT:"{text}"
        CONCISE SUMMARY:"""

    map_prompt_template = PromptTemplate(
        input_variables=['text'],
        template=map_custom_prompt
    )

    # Combine
    combine_custom_prompt = \
        """Write a concise summary of the following in bullet point form. 
        The following text was taken from a website, so there may be redundant website information. 
        Extract only the most important content information.
        There is no need to state "The article says" or "The article states" or similar before each bullet point.
        TEXT:"{text}"
        CONCISE BULLET POINT SUMMARY:"""

    combine_prompt_template = PromptTemplate(
        template=combine_custom_prompt,
        input_variables=['text']
    )

    # MapReduce
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type='map_reduce',
        map_prompt=map_prompt_template,
        combine_prompt=combine_prompt_template,
        verbose=False
    )

    return log_chain_run(summary_chain, docs)
