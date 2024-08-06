select
    i.invoice_date
    , strftime(i.invoice_date, '%Y%m')::integer as monthkey
    , i.billing_country as country
    , i.total
    , count(il.track_id) as tracks_cnt
from invoice i
    left join invoice_line il on i.invoice_id=il.invoice_id
group by
    i.invoice_date
    , strftime(i.invoice_date, '%Y%m')::integer
    , i.billing_country
    , i.total
order by
    i.invoice_date