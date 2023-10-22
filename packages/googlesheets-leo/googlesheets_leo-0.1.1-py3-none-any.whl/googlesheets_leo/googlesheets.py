# from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# import os
# from importacoes import  Request, Credentials, InstalledAppFlow, build, HttpError



# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1d5jhdbwwuPdrYjbFtDsdfgtxwdXDYnlStpHiHqI1zL4'
SAMPLE_RANGE_NAME = 'pagina1!A:z'


def DeletarArquivo(caminho_arquivo):
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)
def Pasta_do_Arquivo(caminho_arquivo):
    return  os.path.dirname(caminho_arquivo)        
def Juntar(a, b):
        return os.path.join(a, b)
                  
def main(nome_da_credencial = r'.\client_secret.json'):
    creds = None
    try: 
        caminhotoken = Juntar(Pasta_do_Arquivo(nome_da_credencial),'token.json') 
        if os.path.exists(caminhotoken):
            creds = Credentials.from_authorized_user_file(caminhotoken, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(nome_da_credencial, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(caminhotoken, 'w') as token:
                token.write(creds.to_json())

        return creds
    except:
        DeletarArquivo(caminhotoken)
        main()



          
def AtualizarCelulas(planilha = SAMPLE_SPREADSHEET_ID, celulas = 'pagina1!A:z',valores=[[]],nome_da_credencial = r'.\client_secret.json' ):
    creds = main(nome_da_credencial) 

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        # result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
        #                             range=SAMPLE_RANGE_NAME).execute()
        # values = result.get('values', [])
        # print(values)


                            

        result = sheet.values().update(spreadsheetId=planilha,
        range=celulas, valueInputOption = "USER_ENTERED", 
                                    body = {'values':valores}).execute()


    except HttpError as err:
        print(err)

def LerCelulas(planilha = SAMPLE_SPREADSHEET_ID, celulas = 'pagina1!A:z', nome_da_credencial = r'.\client_secret.json'):
    creds = main(nome_da_credencial) 

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=planilha, range=celulas,).execute()
        values = result.get('values', [])
        values = [row for row in values if any(cell.strip() for cell in row)]
    except HttpError as err:
        print(err)

    return values


# quando der erro no token, delete-o e rode o programa novamente






if __name__ == '__main__':

    main()