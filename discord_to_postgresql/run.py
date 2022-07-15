from pathlib import Path
import fire
import zipfile

from discord_to_postgresql import transform, load


def run(package='./package.zip',
        if_exists='fail',
        username='',
        password='',
        host='',
        port='',
        db_name='',
        text_file_with_url=''):
    '''Imports Discord messages archive to PostgreSQL database.
    
    Args:
      package: package.zip file path.
      if_exists: How to behave if the tables already exist. This argument will be directly passed to the DataFrame.to_sql() function. Possible values: `fail`: Raise a ValueError. `replace`: Drop the table before inserting new values. `append`: Insert new values to the existing table.
       username: PostgreSQL server username. Optional if text_file_with_url already specified.
       password: PostgreSQL server password. Optional if text_file_with_url already specified.
       host: PostgreSQL server host URL (e.g. localhost or xxx.xxx.xxx.xxx). Optional if text_file_with_url already specified.
       port: PostgreSQL server port. Optional if text_file_with_url already specified.
       db_name: PostgreSQL server database name. Optional if text_file_with_url already specified.
       text_file_with_url: Text file containing PostgreSQL DB connection URL. Optional if username, password, host, port, db_name are all specified.
URL is of the format: postgresql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME> 
    '''
    if (not text_file_with_url and (
        not username or not password or not host or not port or not db_name)):
        raise ValueError('Please specify either complete DB credentials or a text file containing DB connection URL')
    with zipfile.ZipFile(package) as pf:
        print('Transforming json & csv files to dataframes...')
        dfis = transform.package_to_dfs(pf)
        print('\n'.join(str(dfi) for dfi in dfis))
        print('Loading dataframes to postgresql database...')
        load.dfis_to_postgre(dfis, if_exists, username, password, host, port, db_name, text_file_with_url)
        print('Done')
    

if __name__ == '__main__':
    fire.Fire(run)