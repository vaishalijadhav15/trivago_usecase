import click
import great_expectations as ge
import pyarrow.parquet as pq
import s3fs
import boto3
@click.command()
@click.option("--date", "-d", help='Date formated as %Y-%m-%d')
@click.option("--bucket", "-b", help='S3 bucket where output is stored')
def sanity_check(date, bucket):
    s3 = s3fs.S3FileSystem()

    output = ge.from_pandas(
        pq.ParquetDataset(f's3://{bucket}/usp/output/date={date}', filesystem=s3).read_pandas().to_pandas()
    )

    output.expect_column_values_to_be_in_set('accommodation_ns', [100])

    status = output.validate()
    print(status)

    if not status['success']:
        error_notify(status)
        raise ValueError






def error_notify(message):
    sns_topic_arn = 'arn:aws:sns:us-east-1:534860077983:tvg_poc_topic'
    sns = boto3.client('sns', region_name='us-east-1')
    SUBJECT = "Datalake-Check-Failed"
    BODY = """Datalake Monitoring Alert \n Data Source Name: trivago \n Notification Type: Alert \n Message: {0} """.format(message)
    sns.publish(TargetArn=sns_topic_arn,
                Message=BODY, Subject=SUBJECT,
                MessageStructure='text')
    return



if __name__ == '__main__':
        sanity_check()
