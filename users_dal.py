from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class users_DAL:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    def create_user(self, username, hashed_password):
        """Insere um novo usuário no banco de dados."""
        data = {"username": username, "password": hashed_password}
        response = self.supabase.table("users").insert(data).execute()
        return response

    def get_user(self, username):
        """Busca o usuário no banco de dados."""
        response = self.supabase.table("users").select("*").eq("username", username).execute()
        if response.data:
            return response.data[0]
        return None
    
    
