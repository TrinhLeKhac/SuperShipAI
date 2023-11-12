from sqlalchemy import create_engine
from scripts.api.out_data_final import *
from scripts.database.dtypes import *


def ingest_data_to_db():
    port = 'postgresql://postgres:123456@localhost:5432/db_supership_ai'
    engine = create_engine(port)

    print('>>> Ingest data đã qua xử lý...')
    processed_data_path = './processed_data'
    for f, schema in TABLE_SCHEMA.items():
        if f not in ['data_api', 'data_api_full', 'data_check_output']:
            tmp_df = pd.read_parquet('./processed_data/{}.parquet'.format(f))
            tmp_df.to_sql(name=f, con=engine, schema="db_schema", if_exists="replace", index=False, dtype=schema)

    print('-' * 100)

    print('>>> Ingest output API')
    data_api_df = pd.read_parquet('./output/data_api.parquet')
    data_api_df.to_sql(name='data_api', con=engine, schema="db_schema", if_exists="replace", index=False,
                       dtype=TABLE_SCHEMA['data_api'])
    print('-' * 100)

    print('>>> Ingest output API full')
    data_api_full_df = out_data_api(return_full_cols_df=True)
    data_api_full_df.to_sql(name='data_api_full', con=engine, schema="db_schema", if_exists="replace", index=False,
                            dtype=TABLE_SCHEMA['data_api_full'])
    print('-' * 100)

    print('>>> Ingest data check output')
    if os.path.exists('./output/data_check_output.parquet'):
        check_df = pd.read_parquet('./output/data_check_output.parquet')
    else:
        check_df = out_data_final()

    check_df.to_sql(name='data_check_output', con=engine, schema="db_schema", if_exists="replace", index=False,
                    dtype=TABLE_SCHEMA['data_check_output'])
    print('-' * 100)


if __name__ == '__main__':
    ingest_data_to_db()
