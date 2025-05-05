import google.generativeai as genai
import requests
from apiKeys_dal import apiKeys_DAL
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from util import Util
from datetime import datetime

dal_apiKyes = apiKeys_DAL()    

class GenerateResponseIAs:
    
    def __init__(self):
        pass

    def generate_response(self, message, user_id):
        
        githubmodels_key = dal_apiKyes.get_githubmodels_key(user_id)
        gemini_key = dal_apiKyes.get_gemini_key(user_id)
        msg_final = []
        contador = datetime.now()
        print(f"Chave Gemini: {gemini_key} | Chave GithubModels: {githubmodels_key}")
        
        if githubmodels_key: 
            
            msg_final[0] = self.generate_response_openAi(message, githubmodels_key) #openai/gpt-4.1
            contador = datetime.now() - contador
            print(f"Tempo de resposta OpenAI: {contador.total_seconds()} segundos")
            #msg_final[0] += '\n\n' # Adiciona uma quebra de linha entre as respostas


            contador = datetime.now()
            msg_final[1] = self.generate_response_deepseek(message, githubmodels_key) #DeepSeek-V3-0324
            contador = datetime.now() - contador
            print(f"Tempo de resposta DeepSeek: {contador.total_seconds()} segundos")
            #msg_final[1] += '\n\n' # Adiciona uma quebra de linha entre as respostas

            
            contador = datetime.now()
            msg_final[2] = self.generate_response_llama(message, githubmodels_key) #Meta-Llama-3.1-70B-Instruct" 
            contador = datetime.now() - contador
            print(f"Tempo de resposta Llama: {contador.total_seconds()} segundos")               

        if gemini_key:            
            msg_final = self.generate_response_gemini(msg_final, gemini_key)                

        return msg_final

    def generate_response_gemini(self, message, gemini_key):          
        try:
            # Configurar chave de API
            genai.configure(api_key=gemini_key)

            message_gemini = (
    f"A seguir estão respostas fornecidas por diferentes modelos de linguagem "
    f"(ChatGPT, DeepSeek e LLaMA) para a mesma pergunta, embora a pergunta original não esteja disponível. "
    f"Use essas respostas como base e forneça uma única resposta clara, objetiva e bem estruturada, "
    f"como se você fosse uma IA chamada Auriel respondendo diretamente ao usuário.\n\n"
    f"Respostas das fontes:\n"
    f"- ChatGPT: {message[0]}\n"
    f"- DeepSeek: {message[1]}\n"
    f"- LLaMA: {message[2]}\n\n"
    f"Importante: Não diga que está resumindo ou comparando respostas de outros modelos. "
    f"Fale com naturalidade, como se a resposta fosse inteiramente sua. "
    f"Sempre se refira a si mesmo como Auriel."
)
            
            model = genai.GenerativeModel("gemini-1.5-pro")
            response = model.generate_content(message_gemini)

            return response.text if response else "Erro ao gerar resposta com Gemini."
        
        except Exception as e:
            print(f"Erro ao conectar ao Gemini: {e}")
            return
    
    def generate_response_openAi(self, message, githubmodels_key):
        
        try:
            endpoint = "https://models.github.ai/inference"
            model = "openai/gpt-4.1"

            client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(githubmodels_key),)

            response = client.complete(
                messages=[
                    SystemMessage("You are a helpful assistant."),
                    UserMessage(message)
                ],
                temperature=1.0,
                top_p=1.0,
                model=model
            )

            return response.choices[0].message.content

        
        except Exception as e:
            print(f"Erro OpenAI ao conectar ao GitHub Models: {e}")
            return 
        

    def generate_response_deepseek(self, message, githubmodels_key):

        try:
            endpoint = "https://models.github.ai/inference"
            model = "deepseek/DeepSeek-V3-0324"

            client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(githubmodels_key),)

            response = client.complete(
                messages=[
                    SystemMessage("You are a helpful assistant."),
                    UserMessage(message)
                ],
                temperature=1.0,
                top_p=1.0,
                model=model
            )

            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Erro DeepSeek ao conectar ao GitHub Models: {e}")
            return 
        

    def generate_response_llama(self, message, githubmodels_key):

        try:
            endpoint = "https://models.github.ai/inference"
            model = "meta/Meta-Llama-3.1-70B-Instruct"

            client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(githubmodels_key),)

            response = client.complete(
                messages=[
                    SystemMessage("You are a helpful assistant."),
                    UserMessage(message)
                ],
                temperature=1.0,
                top_p=1.0,
                model=model
            )

            return response.choices[0].message.content
        
        except Exception as e:
            print(f"Erro Llama ao conectar ao GitHub Models: {e}")
            return
        
        
