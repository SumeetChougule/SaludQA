from langchain.llms import Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-pro")

result = llm.invoke("what is gravity?")

print(result)
print(result.content)


mm = ChatGoogleGenerativeAI(model="gemini-pro-vision")

message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "what do you see in this image? Make a scientific assessment based on what you see",
        },
        {
            "type": "image_url",
            "image_url": "https://picsum.photos/seed/picsum/200/300",
        },
    ]
)

mm.invoke([message])
