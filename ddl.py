from connector import set_connection
import pandas as pd

with open('queries/ddl.sql') as f:
    query=f.read()

with set_connection('duckdb') as duck:
    duck.execute(query)

    invoice_df=pd.read_csv("source/invoice.csv")
    duck.query("""
        insert into invoice
        select *
        from invoice_df
    """)

    invoice_line_df=pd.read_csv("source/invoice_line.csv")
    duck.query("""
        insert into invoice_line
        select *
        from invoice_line_df
    """)