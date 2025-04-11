from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

opeain_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    temperature=0.2,
    model="gpt-3.5-turbo",
    openai_api_key= opeain_key
)

prompt = ChatPromptTemplate.from_template("""
Você é um classificador de sentimentos e intenções. Dada um feedback de um usuário para uma empresa, retorne *apenas* um JSON válido com as chaves: sentiment, requested_features.:

{{
  "sentiment": "POSITIVO" | "NEGATIVO" | "INCONCLUSIVO",
  "requested_features": [
    {{
      "code": "UM_CODIGO_RESUMIDO_DA_INTENCAO",
      "reason": "A razão principal baseada no feedback do usuário"
    }}
  ]
}}

Feedback: "{feedback}"
""")

def sentiment_classifier(feedback):
    chain = prompt | llm
    response = chain.invoke({"feedback": feedback})
    return response.content