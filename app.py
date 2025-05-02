from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
from flask import request, jsonify
from users_dal import users_DAL
from apiKeys_dal import apiKeys_DAL
from IAHandler import GenerateResponseIAs

app = Flask(__name__)
app.secret_key = "secreta-chave"  # Necessário para usar sessões
dal_users = users_DAL()
dal_apiKyes = apiKeys_DAL()
gp = GenerateResponseIAs()


@app.route('/')
def home():
    return redirect(url_for("login"))


#####################################################
##################LOGIN###############################
#####################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = dal_users.get_user(username)
        if user:
            hashed_password = user["password"]
            # Verifica se a senha informada corresponde à senha armazenada
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):

                # Armazena o nome de usuário na sessão
                session['user'] = username  
                session['user_id'] = user["id"]
                return redirect(url_for("chat")) 
             
            else:
                return render_template("login.html", login_erro="Usuário ou senha incorretos.")
        return render_template("login.html", login_erro="Usuário ou senha incorretos.")
    return render_template("login.html")

#####################################################
##################CHAT###############################
#####################################################
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "POST": 
        if request.form.get("action") == "save-settings":

            gemini_key = request.form.get("gemini_key")
            openai_key = request.form.get("openai_key")
            deepseek_key = request.form.get("deepseek_key")
            copilot_key = request.form.get("copilot_key")
            githubmodels_key = request.form.get("githubmodels_key")
            
            if session['user_id']:
                if dal_apiKyes.get_apikey(session['user_id']):                    
                    dal_apiKyes.update_api_key(session['user_id'], gemini_key, openai_key, deepseek_key, copilot_key, githubmodels_key)
                else:
                    dal_apiKyes.create_api_key(session['user_id'], gemini_key, openai_key, deepseek_key, copilot_key, githubmodels_key)
            else:
                return render_template("chat.html") 
            
    # Verifica se o usuário está logado
    if 'user' not in session:
        return redirect(url_for("login"))  
    return render_template("chat.html", user_login= "olá " + session['user'])  


####################################################
##################LOGOUT###############################
####################################################
@app.route("/logout")
def logout():
    session.pop('user', None)  
    return redirect(url_for("login"))  

####################################################
##################REGISTER###############################
####################################################
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]        
        
        if dal_users.get_user(username):
            return render_template("register.html", register_erro="Usuário já existe.")        
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            dal_users.create_user(username, hashed_password.decode('utf-8'))

            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/send-message", methods=["POST"])
def send_message():
    data = request.get_json()
    message = data.get("message")

    chat_history = session.get('chat_history', [])
    chat_history.append({'sender': 'Você', 'message': message})

    response = gp.generate_response(message, session['user_id'])

    chat_history.append({'sender': 'Bot', 'message': response})
    session['chat_history'] = chat_history

    return jsonify({'bot_response': response})



if __name__ == "__main__":
    app.run(debug=True)




