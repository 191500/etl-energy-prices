CREATE TABLE IF NOT EXISTS energy_prices(
	id SERIAL primary key,
	year_period varchar(4),
	month_period varchar(2),
	stateId varchar(5),
	stateDescription varchar(50),
	sectorid varchar(3),
	sectorName varchar(50),
	customers int,
	price float,
	revenue float,
	sales float
);