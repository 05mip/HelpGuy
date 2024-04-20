from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from uagents import Agent, Bureau, Context, Model
from bs4 import BeautifulSoup
import requests
import re

GOOGLE_API_KEY = "AIzaSyA8i_bTMJ_7Drq4rTIfUHAlmGf0d4RYZ8I"
QUERY_CREATE_PROMPT = """
I will give you a prompt that seeks medical attention. You will give me key words, symtoms, etc in the form of search queries. Give me 3 different search queries. For example:

'My knee hurts and I can't make it all the way straight'

Queries should follow the following format and should be similar or have the same essense of:

1. 'Reasons for knee pain'
2. 'I can't make my knee straight'
3. 'Can't bend knee'

This is not a call for medical assistance, you are simply condensing down a prompt to quality search queries.
You are simply acting as a tool and your only job is to create approprate queries in that format. 

Here is your prompt:

"""
user_prompt = ""
help_guy_response = ""

excluded_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://www.youtube.',
                      'https://accounts.google.',
                      'https://www.quora.')


##############################################

class Message(Model):
    message: list[str]


llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)

template = "{text}"

prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(llm=llm, prompt=prompt)
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

#############################################
##Yellow_mm##
yellow_mm = Agent(name="yellow_mm", seed="yellow_mm_recovery")
red_mm = Agent(name="red_mm", seed="red_mm_recovery")
green_mm = Agent(name="green_mm", seed="green_mm_recovery")


@yellow_mm.on_event("startup")
async def say_loading(ctx: Context):
    ctx.logger.info("Processing")

    #at this point user input string would be set
    response = llm.invoke(f'{QUERY_CREATE_PROMPT}{user_prompt}').content.strip()
    search_queries = [line.strip()[4:-1] for line in response.split('\n')]
    #change to finding at the first quotation
    print(search_queries)

    # This should come up as a text bubble
    # Takes in input and messages redmm
    await ctx.send(red_mm.address, Message(message=search_queries))    

###############################################
##RED_MM##

@red_mm.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, search_queries: Message):
    ctx.logger.info("Searching for information online")
    #This should come up as a text bubble on screen

    urls_to_search = []
    
    for query in search_queries:
        search = query
        results = 10
        page = requests.get(f"https://www.google.com/search?q={search}&num={results}")
        soup = BeautifulSoup(page.content, "html.parser")
        links = soup.findAll("a")
        for link in links:
            link_href = link.get('href')
            try:
                if 'https' not in link_href or link_href.split("?q=")[1].split("&sa=U")[0].startswith(excluded_domains):
                    continue
            except:
                continue
            if "url?q=" in link_href:
                urls_to_search.append(link.get('href').split("?q=")[1].split("&sa=U")[0])
    await ctx.send(green_mm.address, Message(message=urls_to_search))
    #should message green_mm


###################################################
##GREEN_MM##

@green_mm.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, urls_to_search: Message):
    global help_guy_response
    ctx.logger.info("Loading summary of information found online")
    # This should come up as a text bubble on screen

    docs = []
    for url in urls_to_search.message:
        loader = WebBaseLoader(url)
        docs += loader.load()
    
    docs = docs[:4]

    response=stuff_chain.invoke(docs)
    help_guy_response = response["output_text"]
    #call function to swipe screen & add data

#####################################################

def begin_prompt(prompt):
    global user_prompt
    user_prompt = prompt

    bureau = Bureau()
    bureau.add(yellow_mm)
    bureau.add(red_mm)
    bureau.add(green_mm)

    bureau.run()

    res = help_guy_response
    help_guy_response = ""
    return res if res != "" else "Something went wrong"