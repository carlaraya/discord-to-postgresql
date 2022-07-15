import json
import numpy as np
import pandas as pd
from sqlalchemy.types import BigInteger, DateTime, Integer, Unicode, UnicodeText

USER_JSON = 'account/user.json'
SERVER_JSON_FNAME = 'guild.json'
CHANNEL_JSON_FNAME = 'channel.json'
MESSAGE_CSV_FNAME = 'messages.csv'


# DataFrameInfo (dfi) class with dataframe and extra information
class DataFrameInfo:
    def __init__(self, df, name, datatypes):
        self.df = df
        self.name = name
        self.datatypes = datatypes

    def __repr__(self):
        return '"%s" dataframe with %s rows''' % (self.name, len(self.df))

def package_to_dfs(package):
    transform_funcs = [
        transform_user,
        transform_server,
        transform_channel,
        transform_recipient,
        transform_message
    ]
    dfis = []
    for func in transform_funcs:
        dfis.append(func(package, dfis)) # pass in previous dfis
    return dfis

def transform_user(package, _=None):
    with package.open(USER_JSON) as user_fo:
        user_json = json.loads(user_fo.read())
        own_user_df = pd.json_normalize(user_json)
        friends_df = pd.json_normalize(user_json['relationships'])
    friends_df = friends_df.rename(columns={'user.username': 'username', 'user.discriminator': 'discriminator'})
    df = pd.concat([own_user_df, friends_df], ignore_index=True) # it is important that own_user_df comes first. it will be referenced by transform_message
    return DataFrameInfo(
        df,
        'user',
        {
            'id': BigInteger(),
            'username': Unicode(),
            'discriminator': Unicode()
        })

def transform_server(package, _=None):
    dfs = []
    for file in package.namelist():
        if file.endswith(SERVER_JSON_FNAME):
            with package.open(file) as fo:
                json_obj = json.loads(fo.read())
                d = pd.json_normalize(json_obj)
                dfs.append(d)
    df = pd.concat(dfs, ignore_index=True)
    return DataFrameInfo(
        df,
        'server',
        {
            'id': BigInteger(),
            'name': Unicode()
        })

def transform_channel(package, _=None):
    dfs = []
    for file in package.namelist():
        if file.endswith(CHANNEL_JSON_FNAME):
            with package.open(file) as fo:
                json_obj = json.loads(fo.read())
                d = pd.json_normalize(json_obj)
                dfs.append(d)
    df = pd.concat(dfs, ignore_index=True)
    df = df.rename(columns={'guild.id': 'server_id'})
    return DataFrameInfo(
        df,
        'channel',
        {
            'id': BigInteger(),
            'type': Integer(),
            'name': Unicode(),
            'server_id': BigInteger()
        })

def transform_recipient(package, prev_dfis):
    channel_df = [dfi for dfi in prev_dfis if dfi.name == 'channel'][0].df
    df = channel_df.loc[:, ['id', 'recipients']].dropna()
    df = df.explode('recipients')
    df = df.set_axis(['channel_id', 'user_id'], axis=1)
    return DataFrameInfo(
        df,
        'recipient',
        {
            'channel_id': BigInteger(),
            'user_id': BigInteger()
        })

def transform_message(package, prev_dfis):
    user_df = [dfi for dfi in prev_dfis if dfi.name == 'user'][0].df
    own_user_id = user_df.at[0, 'id'] # first row of user_df is own user
    dfs = []
    for file in package.namelist():
        if file.endswith(MESSAGE_CSV_FNAME):
            with package.open(file) as fo:
                d = pd.read_csv(fo)
                d.columns = d.columns.str.lower()
                d['channel_id'] = file.split('/')[-2].replace('c', '')
                d['user_id'] = own_user_id
                dfs.append(d)
    df = pd.concat(dfs, ignore_index=True)
    return DataFrameInfo(
        df,
        'message',
        {
            'id': BigInteger(),
            'timestamp': DateTime(),
            'contents': UnicodeText(),
            'attachments': Unicode(),
            'channel_id': BigInteger(),
            'user_id': BigInteger()
        })
    