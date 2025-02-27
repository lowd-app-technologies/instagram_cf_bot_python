import json
import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
from http.server import BaseHTTPRequestHandler

# Configuração de logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Credentials(BaseModel):
    username: str
    password: str

@app.get("/")
async def root():
    return {"message": "Backend está online!"}

@app.post("/api/get_user_info")
async def get_user_info(credentials: Credentials):
    logger.info(f"Tentando recuperar informações para o usuário: {credentials.username}")
    return {
        "message": "Login successful",
        "user_name": credentials.username,
        "profile_picture": "/profile.jpg"
    }

@app.post("/api/run_selenium")
async def run_selenium(credentials: Credentials):
    usuarios_adicionados = 10  # Número simulado de usuários adicionados
    return {
        "success": True,
        "usuarios_adicionados": usuarios_adicionados
    }

def get_user_info_impl(credentials):
    logger.info(f"Tentando recuperar informações para o usuário: {credentials.username}")
    return {
        "message": "Login successful",
        "user_name": credentials.username,
        "profile_picture": "/profile.jpg"
    }

def run_selenium_impl(credentials):
    usuarios_adicionados = 10  # Número simulado de usuários adicionados
    return {
        "success": True,
        "usuarios_adicionados": usuarios_adicionados
    }

def handler(event, context):
    try:
        # Verifica se é um evento HTTP do Vercel
        if 'httpMethod' in event:
            method = event.get('httpMethod', '')
            path = event.get('path', '')
            body = json.loads(event.get('body', '{}') or '{}')
            
            # Rota raiz
            if path == '/' or path == '':
                return {
                    'statusCode': 200,
                    'body': json.dumps({"message": "Backend está online!"}),
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                }
            
            # Rotas de API
            if method == 'POST':
                if path == '/api/get_user_info':
                    credentials = Credentials(**body)
                    result = get_user_info_impl(credentials)
                elif path == '/api/run_selenium':
                    credentials = Credentials(**body)
                    result = run_selenium_impl(credentials)
                else:
                    result = {"error": "Rota não encontrada"}
                    return {
                        'statusCode': 404,
                        'body': json.dumps(result),
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        }
                    }
                
                return {
                    'statusCode': 200,
                    'body': json.dumps(result),
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*'
                    }
                }
            
            # Método não permitido
            return {
                'statusCode': 405,
                'body': json.dumps({"error": "Método não permitido"}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }
        
        # Caso não seja um evento HTTP
        return {
            'statusCode': 200,
            'body': json.dumps("Backend está online!")
        }
    except Exception as e:
        logger.error(f"Erro no handler: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({"error": str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }

# Função para compatibilidade com diferentes plataformas
def main(event, context):
    return handler(event, context)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
