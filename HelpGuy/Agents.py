from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from uagents import Agent, Bureau, Context, Model
from bs4 import BeautifulSoup
from agent_config import *
from fake_useragent import UserAgent
import requests
from uagents.context import send_sync_message
from uagents.crypto import Identity



user_prompt = ""
help_guy_response = ""
State = None

##############################################

class Message(Model):
    message: list[str]

ua = UserAgent()
header_template = {
    'User-Agent': ua.random
}

llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=GOOGLE_API_KEY)
prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(llm=llm, prompt=prompt)
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

#############################################
##Yellow_mm##
yellow_mm = Agent(name="yellow_mm", seed="yellow_mm_recovery")
red_mm = Agent(name="red_mm", seed="red_mm_recovery")
green_mm = Agent(name="green_mm", seed="green_mm_recovery")

endpointID = Identity.from_seed("endpoint_recovery", 0)

@yellow_mm.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, user_prompt: Message):
    ctx.logger.info("YELLOW")

    if sender != green_mm.address:
        ctx.logger.info("Processing")

        response = llm.invoke(f'{QUERY_CREATE_PROMPT}{user_prompt}').content.strip()
        search_queries = [line.strip()[4:-1] for line in response.split('\n')]
        #change to finding at the first quotation
        print(search_queries)

        # This should come up as a text bubble
        # Takes in input and messages redmm
        await ctx.send(red_mm.address, Message(message=search_queries))
    else:
        await ctx.send(endpointID.address, user_prompt)


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
    for url in urls_to_search.message[:1]:
        try:
            loader = WebBaseLoader(url, header_template=header_template)
            docs += loader.load()
        except:
            continue
    
    response=stuff_chain.invoke(docs)
    help_guy_response = response["output_text"]
    print(help_guy_response)

    await ctx.send(yellow_mm.address, Message(message=[help_guy_response]))
    #call function to swipe screen & add data

#####################################################
##BLUE_MM##


#####################################################



bureau = Bureau(endpoint='http://127.0.0.1:8000/submit')
bureau.add(yellow_mm)
bureau.add(red_mm)
bureau.add(green_mm)


if __name__ == "__main__":
    bureau.run()


