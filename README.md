# Discord to PostgreSQL

Imports Discord messages archive to PostgreSQL database.

Tested in Python 3.7, 3.8, and 3.9 on Linux and Windows.

## Installation
```
pip3 install discord-to-postgresql
```

## Usage

### Run with postgresql credentials as arguments
```
discord_to_postgresql path/to/package.zip replace myusername mypassword 0.0.0.0 5432 postgres
```

### Run with textfile containing PostgreSQL connection URL specified as argument
```
discord_to_postgresql path/to/package.zip replace -t path/to/conn_url.txt
```
#### Sample contents of textfile
```
postgresql://myusername:mypassword@0.0.0.0:5432/postgres
```

## PostgreSQL output tables
### `discord_user`
|    Column     |       Type        |
|---------------|-------------------|
| id            | bigint            |
| username      | character varying |
| discriminator | character varying |

### `discord_server`
| Column |       Type        |
|--------|-------------------|
| id     | bigint            |
| name   | character varying |

### `discord_channel`
`type` is the "type" of the discord channel. Known possible values of `type` are:
- 0 = normal server channel
- 1 = direct message (between 2 people only)
- 3 = group chat (may be more than 2 people)
- 5 = announcement channel
- 11 = thread

|  Column   |       Type        |
|-----------|-------------------|
| id        | bigint            |
| type      | integer           |
| name      | character varying |
| server_id | bigint            |

### `discord_recipient`
A private chat will have 2 "recipients" (members), or 1-8 for group chats.

|   Column   |  Type  |
|------------|--------|
| channel_id | bigint |
| user_id    | bigint |

### `discord_message`
|   Column    |            Type             |
|-------------|-----------------------------|
| id          | bigint                      |
| timestamp   | timestamp without time zone |
| contents    | text                        |
| attachments | character varying           |
| channel_id  | bigint                      |
| user_id     | bigint                      |


## Command-line arguments
- `--package`: package.zip file path.
- `--if_exists`: How to behave if the tables already exist. This argument will be directly passed to the DataFrame.to_sql() function.
Possible values:
    - `fail`: Raise a ValueError.
    - `replace`: Drop the table before inserting new values.
    - `append`: Insert new values to the existing table.
- `--username`: PostgreSQL server username. Optional if text_file_with_url already specified.
- `--password`: PostgreSQL server password. Optional if text_file_with_url already specified.
- `--host`: PostgreSQL server host URL (e.g. localhost or xxx.xxx.xxx.xxx). Optional if text_file_with_url already specified.
- `--port`: PostgreSQL server port. Optional if text_file_with_url already specified.
- `--db_name`: PostgreSQL server database name. Optional if text_file_with_url already specified.
- `--text_file_with_url`: Text file containing PostgreSQL DB connection URL. Optional if username, password, host, port, db_name are all specified.
URL is of the format: `postgresql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DB_NAME>`


## Addendum: Easiest way to start up a test PostgreSQL server

Install Docker: https://docs.docker.com/engine/install/

Then type this command to install a Docker PostgreSQL image and run as a container:
```
docker run -p 5432:5432 --name test-postgres -e POSTGRES_USER=myusername -e POSTGRES_PASSWORD=mypassword -e POSTGRES_DB=postgres -d postgres
```
This will run a postgresql server accessible on `localhost:5432` with username `myusername` and password `mypassword`, and create a databased named `postgres`.

To stop the container:
```
docker stop test-postgres
```
To restart the container:
```
docker start test-postgres
```
To delete the container (and erase all db data):
```
docker rm test-postgres
```
after which it is completely fine to run the above-mentioned `docker run` command again.

Heroku Postgres (free cloud server) is another option but has a maximum row number limit.

## TODO
- [ ] Test for other versions of Python
- [ ] Test for Windows
- [ ] Add support for primary keys (no duplicate rows if append)
