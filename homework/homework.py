"""
Escriba el codigo que ejecute la accion solicitada.
"""


import os
import zipfile
import pandas as pd
from datetime import datetime

def clean_campaign_data():
    input_folder = "files/input"
    output_folder = "files/output"
    os.makedirs(output_folder, exist_ok=True)

    dataframes = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".zip"):
            zip_path = os.path.join(input_folder, filename)
            with zipfile.ZipFile(zip_path, "r") as z:
                for csv_filename in z.namelist():
                    if csv_filename.endswith(".csv"):
                        with z.open(csv_filename) as f:
                            df = pd.read_csv(f, sep=",")
                            dataframes.append(df)

    if not dataframes:
        raise FileNotFoundError("No se encontraron archivos .csv dentro de los .zip.")

    df = pd.concat(dataframes, ignore_index=True)

    client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    client["job"] = client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)
    client["credit_default"] = client["credit_default"].apply(lambda x: 1 if str(x).lower() == "yes" else 0)
    client["mortgage"] = client["mortgage"].apply(lambda x: 1 if str(x).lower() == "yes" else 0)
    client.to_csv(os.path.join(output_folder, "client.csv"), index=False)

    campaign = df[[
        "client_id", "number_contacts", "contact_duration",
        "previous_campaign_contacts", "previous_outcome",
        "campaign_outcome", "month", "day"
    ]].copy()
    campaign["previous_outcome"] = campaign["previous_outcome"].apply(lambda x: 1 if str(x).lower() == "success" else 0)
    campaign["campaign_outcome"] = campaign["campaign_outcome"].apply(lambda x: 1 if str(x).lower() == "yes" else 0)
    campaign["last_contact_date"] = campaign.apply(
        lambda row: f"2022-{month_to_number(row['month']):02d}-{int(row['day']):02d}", axis=1
    )
    campaign = campaign.drop(columns=["month", "day"])
    campaign.to_csv(os.path.join(output_folder, "campaign.csv"), index=False)

    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics.to_csv(os.path.join(output_folder, "economics.csv"), index=False)

def month_to_number(month_str):
    months = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
    }
    return months.get(str(month_str).lower(), 1)

if __name__ == "__main__":
    clean_campaign_data()


"""
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerles un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """