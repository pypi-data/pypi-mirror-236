if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
    
from google.oauth2 import service_account
from google.cloud import bigquery

@data_loader
def load_data(*args, **kwargs):
    credentials = service_account.Credentials.from_service_account_file(
        "athena_credentials_sa.json", scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    client = bigquery.Client(credentials=credentials)

    query = """
    WITH t1 AS (
        SELECT cd_bi_operadora, id_conta AS conta_medica, 
        max(CAST(data_faturamento_guia AS date)) AS data_ingestao,
        count(DISTINCT CAST(data_faturamento_guia AS date)) AS datas_distintas
        FROM arvo.conta_medica_guias
        GROUP BY 1, 2
        HAVING datas_distintas = 1
    )
        
    SELECT s.*,
        p.razao_social,
        p.tipo_rede as id_rede,
        p.estado as uf_prestador,
        p.cidade as cidade_prestador,
        p.especialidade_principal as cbo,
        b.data_nascimento as dt_nascimento,
        b.sexo,
        cast(coalesce(e.codigo_tuss, e.codigo, e.codigo_cbhpm) as string) as codigo,
        e.descricao as evento,
        e.tipo as categoria
    FROM arvo.conta_medica_procedimentos s
    JOIN t1 USING(cd_bi_operadora, conta_medica)
    LEFT JOIN arvo.prestadores p ON s.operadora  = p.operadora AND s.id_prestador = p.id
    LEFT JOIN arvo.beneficiarios b ON s.operadora = b.operadora AND s.id_beneficiario  = b.id
    LEFT JOIN arvo.procedimentos e ON s.operadora = e.operadora AND s.id_procedimento  = e.id
    WHERE CAST(data_ingestao AS date) > DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)
    """

    df = client.query(query).to_dataframe()

    df = 

    # df.to_parquet('gs://arvo-data-prod/athena/raw/sinistro_athena_raw_20231019.parquet')

    return df
