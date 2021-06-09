from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 aws_credentials_id='',
                 tables='',
                 quality_checks='',
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id=redshift_conn_id
        self.aws_credentials_id=aws_credentials_id
        self.tables=tables
        self.quality_checks=quality_checks

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        for check in self.quality_checks:
            # check[0] is the query string; check[1] is the return value defining failure
            for table in self.tables:
                self.log.info(f'Performing data quality check on table {table}')
                records = redshift.get_records(check[0].format(table))
                if len(records) < 1 or len(records[0]) < 1:
                    raise ValueError(f'Data quality check FAILED: Table {table} returned no results')
                num_records = records[0][0]
                if num_records == check[1]:
                    raise ValueError(f'Data quality check on table {table} FAILED.')
                else:
                    self.log.info(f'Data quality check on table {table} PASSED.')
