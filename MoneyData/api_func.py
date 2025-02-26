from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import os

# Configurações iniciais
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CRED_FILE = r'C:\Users\gabri\OneDrive\Desktop\Projects\Data Science\MoneyData\client_secret_69276656658-pvjsvjotq90maq7m0lj33arg13ij3e9d.apps.googleusercontent.com.json'  # Ajuste conforme necessário
TOKEN_FILE = 'token.json'
SHEET_ID = '1T-f1AYiVQG4yauNsQ5WSuPOhMUipZMD0t3-uvKe3_1M'
SHEET_NAME = 'Compras'  # Nome da aba da planilha

def autenticar_sheets():
    """Autentica e retorna o serviço do Google Sheets."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CRED_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    
    return build('sheets', 'v4', credentials=creds)

def obter_dados_planilha():
    """Obtém todos os dados da planilha e garante que todas as linhas tenham o mesmo número de colunas."""
    try:
        service = autenticar_sheets()
        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID, range=SHEET_NAME
        ).execute()

        valores = result.get('values', [])

        if not valores:
            print("Nenhum dado encontrado na planilha.")
            return None

        # Determina o número máximo de colunas existentes
        max_colunas = max(len(linha) for linha in valores)

        # Ajusta todas as linhas para terem o mesmo número de colunas
        dados_padronizados = [linha + [''] * (max_colunas - len(linha)) for linha in valores]

        return dados_padronizados

    except Exception as e:
        print(f"Erro ao obter dados da planilha: {e}")
        return None

def get_finance_df():
    """Baixa os dados do Google Sheets e converte para um DataFrame do Pandas."""
    dados = obter_dados_planilha()
    
    if dados is None:
        return None

    # Primeira linha será usada como cabeçalho
    headers = dados[0]
    valores = dados[1:] if len(dados) > 1 else []

    # Cria o DataFrame
    df = pd.DataFrame(valores, columns=headers)

    return df