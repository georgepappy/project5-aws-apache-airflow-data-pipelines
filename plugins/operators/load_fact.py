from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.utils.decorators import apply_defaults

class LoadFactOperator(BaseOperator):

    ui_color = '#F98866'

    @apply_defaults
    def __init__(self,
                 redshift_conn_id='',
                 aws_credentials_id='',
                 table='',
                 sql_string='',
                 append='',
                 *args, **kwargs):

        super(LoadFactOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id
        self.aws_credentials_id=aws_credentials_id
        self.table=table
        self.sql_string=sql_string
        self.append = append

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)
        credentials = aws_hook.get_credentials()
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        sql_insert = '''
            INSERT INTO {}
                {}
        '''.format(self.table, self.sql_string)
        
        if not self.append:
            self.log.info('Clearing data from Redshift fact table')
            redshift.run('DELETE FROM {}'.format(self.table))
            
        self.log.info('Inserting data into Redshift fact table')        
        redshift.run(sql_insert)
