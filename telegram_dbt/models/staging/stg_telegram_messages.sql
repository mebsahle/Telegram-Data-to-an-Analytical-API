with source as (
    select * from raw.telegram_messages
),

renamed as (
    select
        id,
        date::timestamp as message_date,
        text,
        views,
        has_media,
        channel
    from source
)

select * from renamed
