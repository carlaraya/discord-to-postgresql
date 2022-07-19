from sqlalchemy import create_engine
import psycopg2

# Only include columns that were specified in the datatypes dict
def slice_columns(dfi):
    dfi.df = dfi.df.loc[:, [*dfi.datatypes]]

def dfis_to_postgre(dfis,
                    if_exists,
                    username=None,
                    password=None,
                    host=None,
                    port=5432,
                    db_name=None,
                    text_file_with_url=None):
    for dfi in dfis:
        dfi.name = 'discord_' + dfi.name
    base_dfis_to_postgre(dfis, if_exists, username, password, host, port, db_name, text_file_with_url)

def base_dfis_to_postgre(dfis,
                    if_exists,
                    username=None,
                    password=None,
                    host=None,
                    port=5432,
                    db_name=None,
                    text_file_with_url=None):
    if text_file_with_url:
        with open(text_file_with_url, 'r') as url_fo:
            engine = create_engine(url_fo.read().strip())
    else:
        engine = create_engine('postgresql://%s:%s@%s:%s/%s' %
                               (username, password, host, port, db_name))
    with engine.connect() as conn:
        for dfi in dfis:
            slice_columns(dfi)
            print('Inserting %s df to db...' % dfi.name)
            dfi.df.to_sql(
                dfi.name,
                engine,
                if_exists=if_exists,
                dtype=dfi.datatypes,
                index=False)
