from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class apiKeys_DAL:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def create_api_key(self, id_user,
                        gemini_key, 
                        openAI_key,
                        deepseek_key, 
                        copilot_key, 
                        githubmodels_key):   

        data = {"id_user": id_user, 
                "gemini_key": gemini_key, 
                "openai_key": openAI_key, 
                "deepseek_key": deepseek_key, 
                "copilot_key": copilot_key, 
                "githubmodels_key": githubmodels_key}
        
        response = self.supabase.table("api_key").insert(data).execute()
        
        return response

    def get_apikey(self, id_user):                
        response = self.supabase.table("api_key").select("*").eq("id_user", id_user).execute()
        if response.data:
            return response.data[0]
        return None    
    
    def update_api_key(self, id_user, gemini_key, openAI_key, deepseek_key, copilot_key, githubmodels_key):   

        data = {"id_user": id_user, 
                "gemini_key": gemini_key, 
                "openai_key": openAI_key, 
                "deepseek_key": deepseek_key, 
                "copilot_key": copilot_key, 
                "githubmodels_key": githubmodels_key}
        
        response = self.supabase.table("api_key").update(data).eq("id_user", id_user).execute()
        
        return response
    

    def get_githubmodels_key(self, id_user):                
        response = self.supabase.table("api_key").select("githubmodels_key").eq("id_user", id_user).execute()
        if response.data:
            return response.data[0]["githubmodels_key"]
        return None
    

    def get_gemini_key(self, id_user):                
        response = self.supabase.table("api_key").select("gemini_key").eq("id_user", id_user).execute()
        if response.data:
            return response.data[0]["gemini_key"]
        return None