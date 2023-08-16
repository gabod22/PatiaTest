import json
import os.path
import gspread, google.auth.exceptions, requests
from gspread import Worksheet
from .files_managment import *
from .helpers import next_available_row

from .constants import gspread_file, config_file

letters = ['N', 'O', 'P', 'Q', 'R', 'S', 'T','U','V','W', 'X']


def get_worksheet():
    config = read_yaml(config_file)
    sheet = config['SPREAD_CONFIG']['DOCUMENT_NAME']
    worksheet = config['SPREAD_CONFIG']['WORKSHEET_NAME']
    print('Obteniendo worksheet')
    return  get_spreadsheet(gspread_file, sheet, worksheet)

def write_cell(data, note, wks: Worksheet, row, col):
    wks.update_cell(row, col, data)
    if note != "":
        wks.insert_note("{}{}".format(letters[col],row), note)

def write_range(data, notes, wks: Worksheet, row, col:str):
    wks.update("{}{}".format(col,row), data)
    insert_notes(notes, row, wks)
    

def insert_notes(notes, row, wks):
    for i,note in enumerate(notes):
        if note != "":
            wks.insert_note("{}{}".format(letters[i],row), note)


def get_already_tested_row(serial_number, column, wks):
    print(serial_number, column)
    cell = wks.find(serial_number, in_column=column)
    print(cell)
    if cell:
        return cell.row
    return -1




def get_credentials(input_credentials):
    """
    Takes the input param 'credentials' that can accept a JSON token or a path to a file
    and returns a dict.
    """
    test_file = input_credentials.splitlines()[0]
    if os.path.isfile(test_file):
        try:
            with open(test_file, 'r') as f:
                credentials = json.load(f)
                f.close()
        except Exception as e:
            raise ValueError("Unable to read the JSON Service Account from file '%s'.\n%s" % (test_file, e))
    else:
        try:
            credentials = json.loads(input_credentials)
        except Exception as e:
            raise Exception("Unable to read the JSON Service Account.\n%s" % e)

    return credentials



def get_spreadsheet(json_file, doc_id, tab_id):
    """
    Inputs params:
    * credentials
    * doc_id
    * tab_id
    Returns a gspread's worksheet object.
    """
    credentials = get_credentials(json_file)
    gspread_client = gspread.service_account(json_file)
    
    

    try:
        worksheet = gspread_client.open(doc_id).worksheet(tab_id)
        
        return worksheet

    except gspread.exceptions.SpreadsheetNotFound as e:
        raise Exception("Intento de abrir un documento de hoja de cálculo inexistente o inaccesible.")
    except gspread.exceptions.WorksheetNotFound as e:
        raise Exception("Intentando abrir una hoja inexistente. Compruebe que el nombre de la hoja existe (%s)." % tab_id)
    except google.auth.exceptions.RefreshError as e:
        raise Exception("La hora del servidor y del equipo no es la misma, ajuste la hora")
    except requests.exceptions.ConnectionError as e:
        raise Exception("La conección se cerró sin respuesta, vuelva a intentarlo")
    except gspread.exceptions.APIError as e:
        if hasattr(e, 'response'):
            error_json = e.response.json()
            print(error_json)
            error_status = error_json.get("error", {}).get("status")
            email = credentials.get("client_email", "(email missing)")
            if error_status == 'PERMISSION_DENIED':
                error_message = error_json.get("error", {}).get("message", "")
                raise Exception("El acceso ha sido denegado con el siguiente error: %s. ¿Has activado la API de Sheets? ¿Ha compartido la hoja de cálculo con %s?" % (error_message, email))
            if error_status == 'NOT_FOUND':
                raise Exception("Intentando abrir un documento de hoja de cálculo inexistente. Compruebe que el identificador del documento existe (%s)." % doc_id)
        raise Exception("La API de Google devuelve un error: %s" % e)
