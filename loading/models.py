from sqlalchemy import MetaData, Table, Column, Integer, Text, Boolean, TIMESTAMP

metadata = MetaData()

telegram_messages = Table(
    'telegram_messages', metadata,
    Column('id', Integer, primary_key=True),
    Column('date', TIMESTAMP),
    Column('text', Text),
    Column('views', Integer),
    Column('has_media', Boolean),
    Column('channel', Text),
    schema='raw'
)
