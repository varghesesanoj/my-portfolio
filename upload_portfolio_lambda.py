import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:972788463809:deployPortfolioTopic')
    try:
        s3 = boto3.resource('s3')
        portfolio_bucket = s3.Bucket('portfolio.sanoj.info')
        build_bucket = s3.Bucket('portfoliobuild.sanoj.info')
        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip',portfolio_zip)


        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
             obj = myzip.open(nm)
             portfolio_bucket.upload_fileobj(obj, nm,
                ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
             portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

        print "Done"
        topic.publish(Subject="Portfolio Deployment", Message="Portfolio deployed successfully")

        print "Topic Published"
    except:
        topic.publish(Subject="Portfolio Deployment Failed", Message="Portfolio deployement failed")
        print "Topic Publish Failed"
        raised

    return 'Hello from Lambda'
