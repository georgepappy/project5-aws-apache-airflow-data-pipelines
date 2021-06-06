from airflow.hooks.postgres_hook import PostgresHook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    copy_sql = """
        COPY {} 
        FROM '{}'
        ACCESS_KEY_ID '{}'
        SECRET_ACCESS_KEY '{}'
        COMPUPDATE OFF 
        REGION 'us-west-2'
        TIMEFORMAT AS 'epochmillisecs'
        TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
        FORMAT AS JSON 'auto ignorecase'
    """

    @apply_defaults
    def __init__(self,
                 # Define your operators params (with defaults) here
                 redshift_conn_id='',
                 aws_credentials_id='',
                 table='',
                 s3_bucket='',
                 s3_key='',
                 # Do we need to specify json format here?
                 *args, **kwargs):

        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        # Map params here
        self.redshift_conn_id = redshift_conn_id,
        self.aws_credentials_id=aws_credentials_id,
        self.table=table,
        self.s3_bucket=s3_bucket,
        self.s3_key=s3_key

    def execute(self, context):
        aws_hook = AwsHook(self.aws_credentials_id)

        self.log.info('StageToRedshiftOperator not implemented yet')





