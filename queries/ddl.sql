create if not exists table invoice (
	invoice_id int4 not null,
	customer_id int4 not null,
	invoice_date timestamp not null,
	billing_address varchar(70) null,
	billing_city varchar(40) null,
	billing_state varchar(40) null,
	billing_country varchar(40) null,
	billing_postal_code varchar(10) null,
	total numeric(10, 2) not null,
	constraint invoice_pkey primary key (invoice_id)
);

create if not exists table invoice_line (
	invoice_line_id int4 not null,
	invoice_id int4 not null,
	track_id int4 not null,
	unit_price numeric(10, 2) not null,
	quantity int4 not null,
	constraint invoice_line_pkey primary key (invoice_line_id),
);
