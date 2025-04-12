from datetime import datetime, timedelta

from collections import defaultdict

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from app.models import Feedback, Classification
from app.extensions import db

def feedbacks_week():

    today = datetime.utcnow()
    init_week = today - timedelta(days=7)

    records = (
        db.session.query(Classification.sentiment, Classification.code, Classification.reason)
        .join(Feedback, Classification.feedbacks_id == Feedback.id)
        .filter(Feedback.created_at >= init_week)
        .all()
    )

    total = len(records)
    positives = sum(1 for r in records if r.sentiment == "POSITIVO")
    negatives = sum(1 for r in records if r.sentiment == "NEGATIVO")

    functions = defaultdict(list)

    for r in records:
        functions[r.code].append(r.reason)

    return {
        "porcentagem_positivos": round((positives / total) * 100, 2) if total else 0,
        "porcentagem_negativos": round((negatives / total) * 100, 2) if total else 0,
        "funcionalidades": functions,
        "total_feedbacks": total
    }


def generate_summary(data):

    prompt = PromptTemplate.from_template("""
        Gere um resumo de feedbacks da semana com as seguintes informações:
                                          
        - {porcentagem_positivos}% de feedbacks foram positivos.
        - {porcentagem_negativos}% foram negativos.

        Principais funcionalidades sugeridas e o motivo de serem importantes:
        {funcionalidades_formatadas}

        Escreva de forma clara e profissional. Lembre-se que esse resumo é enviado para colaboradores da empresa.
        """)

    def format_functions(funcs):
        text = ""
        for k, v in funcs.items():
            text += f"- {k}:\n"
            for reason in v[:3]:  # limita pra não ficar enorme
                text += f"  - {reason}\n"
        return text

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    chain = LLMChain(llm=llm, prompt=prompt)

    return chain.run({
        "porcentagem_positivos": data["porcentagem_positivos"],
        "porcentagem_negativos": data["porcentagem_negativos"],
        "funcionalidades_formatadas": format_functions(data["funcionalidades"])
    })

