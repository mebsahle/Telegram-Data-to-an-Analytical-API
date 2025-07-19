select
    id,
    message_date,
    text,
    views,
    has_media,
    channel as channel_name
from {{ ref('stg_telegram_messages') }}
