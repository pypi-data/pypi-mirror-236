"""
Модуль для работы с Google Sheets.

Этот модуль предоставляет функции для установки соединения с Google Sheets API и загрузки данных в Google Sheets.

Примеры использования:
- setup_google_sheets(credentials_folder="path/to/credentials", credentials_file="credentials.json"):
  Устанавливает соединение с Google Sheets API, используя учетные данные из указанного файла в указанной папке.
  По умолчанию используется папка "credentials" и файл "credentials.json".
- read_gs_table(worksheet_id="your_worksheet_id", worksheet_name="your_worksheet_name", google_credentials=None):
  Читает данные из указанного листа Google Sheets и возвращает их в виде DataFrame.
- upload_table_to_google_sheet(dataframe, worksheet_id="your_worksheet_id", worksheet_name="your_worksheet_name",
  google_credentials=None, max_attempts=1, retry_delay=0):
  Загружает DataFrame в указанный лист Google Sheets с поддержкой повторных попыток.
"""

import os
import time
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials


def setup_google_sheets(
    credentials_folder="credentials", credentials_file="credentials.json"
):
    """
    Устанавливает соединение с Google Sheets API, используя учетные данные из файла credentials.json.

    :param credentials_file: Название фала (.JSON) с учетными данными (по умолчанию: "credentials.json").
    :param credentials_folder: Путь к папке с учетными данными (по умолчанию: "credentials").
    :return: Объект для работы с Google Sheets.
    """
    credentials_path = os.path.join(credentials_folder, credentials_file)

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found in {credentials_folder}")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(credentials_path, scopes=scope)
    google_credentials = gspread.authorize(credentials)

    return google_credentials


def read_gs_table(worksheet_id=None, worksheet_name=None, google_credentials=None, max_attempts=1, retry_delay=0):

    """
    Читает данные из указанного листа Google Sheets и возвращает их в виде DataFrame.

    :param worksheet_id: Идентификатор листа.
    :param worksheet_name: Название листа.
    :param google_credentials: Объект для работы с Google Sheets (по умолчанию: None, будет использован setup_google_sheets()).
    :param max_attempts: Максимальное количество попыток чтения данных (по умолчанию: 1).
    :param retry_delay: Задержка между попытками чтения в секундах (по умолчанию: 0).
    :return: DataFrame с данными из листа.
    """
    if google_credentials is None:
        google_credentials = setup_google_sheets()

    gc = google_credentials
    for attempt in range(max_attempts):
        try:
            gs = gc.open_by_key(worksheet_id)
            worksheet = gs.worksheet(worksheet_name)
            rows = worksheet.get_all_records(numericise_ignore=["all"])
            return pd.DataFrame(rows)
        except Exception as e:
            print(f"Error reading data from Google Sheets (attempt {attempt + 1}/{max_attempts}):")
            print(e)
            if attempt < max_attempts - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max attempts reached. Read failed.")


def upload_table_to_google_sheet(
    dataframe,
    worksheet_id,
    worksheet_name,
    google_credentials=None,
    max_attempts=1,
    retry_delay=0,
):
    """
    Загружает DataFrame в указанный лист Google Sheets.

    :param dataframe: DataFrame с данными для загрузки.
    :param worksheet_id: Идентификатор листа.
    :param worksheet_name: Название листа.
    :param google_credentials: Объект для работы с Google Sheets (по умолчанию: None, будет использован setup_google_sheets()).
    :param max_attempts: Максимальное количество попыток загрузки данных (по умолчанию: 1).
    :param retry_delay: Задержка между попытками загрузки в секундах (по умолчанию: 0).
    """
    if google_credentials is None:
        google_credentials = setup_google_sheets()

    gc = google_credentials
    gs = gc.open_by_key(worksheet_id)
    worksheet1 = gs.worksheet(worksheet_name)
    for attempt in range(max_attempts):
        try:
            set_with_dataframe(
                worksheet=worksheet1,
                dataframe=dataframe,
                include_index=False,
                include_column_header=True,
                resize=True,
            )
            print("Data uploaded successfully!")
            break  # Выход из цикла, если загрузка данных прошла успешно
        except Exception as e:
            print(
                f"Error uploading data to Google Sheets (attempt {attempt + 1}/{max_attempts}):"
            )
            print(e)
            if attempt < max_attempts - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max attempts reached. Upload failed.")
