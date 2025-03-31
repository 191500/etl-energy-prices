from airflow.decorators import dag, task
from dataclasses import asdict
from datetime import datetime
import pandas as pd
import logging

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable

from energy_prices.utils.api_request import getEndpoint
from energy_prices.utils.class_model import ApiParameters, EnergySchema

USA_API_KEY = Variable.get("USA_API_KEY")

@dag(
    dag_id="extract_energy_prices",
    schedule="*/5 * * * *",
    start_date=datetime(2025, 3, 23),
    catchup=False
)
def main():

    @task(task_id="verify_offset")
    def verify_pg_offset() -> int:
        """Return the count registers in db; offset for api call"""

        pg_hook = PostgresHook(postgres_conn_id="DB_ETL")

        # conn = pg_hook.get_conn()
        # cursor = conn.cursor()
        # cursor.execute("""
        #     CREATE TABLE IF NOT EXISTS energy_prices (
        #         id SERIAL primary key,
        #         year_period varchar(4),
        #         month_period varchar(2),
        #         stateId varchar(5),
        #         stateDescription varchar(50),
        #         sectorid varchar(3),
        #         sectorName varchar(50),
        #         customers int,
        #         price float,
        #         revenue float,
        #         sales float
        #     );
        # """)
        # cursor.close()
        # conn.commit()

        res = pg_hook.get_records("select count(ep.id) from energy_prices ep")        
        offset = res[0][0]

        logging.info("OFFSET ", offset)

        if (offset==0):
            return offset
        return offset+1

    @task(task_id="extract")
    def extract_prices(offset: int) -> list:
        results = []
        params = ApiParameters()

        params.api_key = USA_API_KEY
        params.length = 5000
        params.offset = offset
        
        response = getEndpoint("electricity/retail-sales/data/", params)

        results.extend(response.data)

        return [asdict(x) for x in results]

    @task(task_id="transform")
    def transform_prices(list_prices: list) -> list:
        formatedPrices = []
        for price in list_prices:
            if price["sectorid"]=="ALL":
                continue

            newDict = {
                    "year_period": price["period"].split("-")[0],
                    "month_period": price["period"].split("-")[1],
                    "stateid": price["stateid"],
                    "stateDescription": price["stateDescription"],
                    "sectorid": price["sectorid"],
                    "sectorName": price["sectorName"],
                    "customers": int(price["customers"]) if price["customers"] else 0,
                    "price": float(price["price"]) if price["price"] else 0,
                    "revenue": float(price["revenue"]) if price["revenue"] else 0,
                    "sales": float(price["sales"]) if price["sales"] else 0,
                }
            
            formatedPrices.append(newDict)

        return formatedPrices

    @task(task_id="load")
    def load_prices(list_prices_formated: list):

        pg_hook = PostgresHook(postgres_conn_id="DB_ETL")

        pg_hook.insert_rows(
            table="energy_prices",
            rows=[(data["year_period"], data["month_period"], data["stateid"], data["stateDescription"], data["sectorid"], data["sectorName"], data["customers"], data["price"], data["revenue"], data["sales"]) for data in list_prices_formated],
            target_fields=["year_period", "month_period", "stateid", "stateDescription", "sectorid", "sectorName", "customers", "price", "revenue", "sales"]
        )

    load_prices(transform_prices(extract_prices(verify_pg_offset())))

main()