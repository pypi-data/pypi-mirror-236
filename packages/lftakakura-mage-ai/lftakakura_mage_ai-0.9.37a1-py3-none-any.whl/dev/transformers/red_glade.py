if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer

# from arvo.data_dictionary.standard import (
#     EVENT_COLUMNS,
#     PROVIDER_COLUMNS,
#     BENEFICIARY_COLUMNS,
# )

@transformer
def transform(df, *args, **kwargs):
    df = df.loc[df['tipo_conta'] == 'CONTA NORMAL']
    # print(df)
    # df.loc[:, "codigo"] = df["codigo"].str.replace("\D", "", regex=True).replace("", None).fillna("-99").astype(int).astype(str)

    # depara = execute_query("select * from raw_athena_client.depara")
    # depara["codigo"] = depara["codigo"].astype(int).astype(str)
    # depara["depara"] = depara["depara"].astype(int).astype(str)

    # df = df.merge(depara, on="codigo", how="left")
    # df.loc[:, "codigo"] = df["depara"].fillna(df["codigo"])

    return df