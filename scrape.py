from settings import load_settings
from langchain_community.document_loaders.web_base import WebBaseLoader
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from langchain_mistralai import ChatMistralAI
import pandas as pd



settings = load_settings()

def load_website_content(website: str)-> str:
    """ function to load the content of web page without HTML tags

    Args:
        website (str): web page url

    Returns:
        str: the content of the web page
    """
    
    web_loader = WebBaseLoader(website)
    docs: list[Document] = web_loader.load()
    text = "\n".join([doc.page_content for doc in docs])
    return text


class DayTemperature(BaseModel):
    """ Define your desired data structure.
    """
    date: str = Field("date of measurements")
    day: float = Field("day temperature ")
    night: float = Field("night temperature")
    weather_conditions: str = Field("weather conditions for day and night")
    chance_of_rain: str = Field("chance of rain (day and night)")
    wind: float = Field("wind speed and direction (day and night)")
    humidity: float = Field("humidity (day and night)")
    UV: str = Field(" UV index in format example 0 of 11 or 1 of 11")
    sunrise_sunset: str = Field("sunrise and sunset times")



def scrape_page(page_url: str)-> pd.DataFrame:
    """function used to scrape the next 10 days temperatures for specific city from a url

    Args:
        page_url (str): the city next 10 days url

    Returns:
        pd.DataFrame: dataframe with DayTemperature structure
    """    
    parser = JsonOutputParser(pydantic_object=DayTemperature)
    parser.get_format_instructions()
    prompt = PromptTemplate(
                        template=
                            """
                            Please provide the 10-day weather forecast for Paris, France, in a structured table format. Include both day and night details for each day. 
                            Response should include the following fields:
                                {format_instructions}
                            Please ensure the data is well-organized and easy to read.
                            <content>
                            {content}
                            </conetnt>
                            Respond only with valid JSON. Do not write an introduction or summary.

                            """,
                            input_variables=["content"],
                            partial_variables={"format_instructions": parser.get_format_instructions()}
                        )
    model = ChatMistralAI(api_key=settings.mistral_api_key, model_name="mistral-large-latest")
    chain = prompt | model | parser
    text = load_website_content(page_url)
    output = chain.invoke({
        "content": text
    })
    return pd.DataFrame(output)


