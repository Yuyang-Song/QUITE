# How to convert this dynamodb_client.query() method written code to batch_get_item()
[Link to question](https://stackoverflow.com/questions/69358194/how-to-convert-this-dynamodb-client-query-method-written-code-to-batch-get-ite)
**Creation Date:** 1632817444
**Score:** 0
**Tags:** python, amazon-web-services, aws-lambda, amazon-dynamodb, boto3
## Question Body
<p>I'm building an API. Now I am building GET lambda function to retrieve multiple items from DynamoDB database. I wrote this function with boto3.query() method and I was told that it is much faster and better to use batch_get_item() method. For now my code looks like this.</p>
<pre><code>  import json
    import boto3
    from boto3.dynamodb.conditions import Key
    
    
    def lambda_handler(event, context):
    
        
        id = 0
        if 'cat_id' in event:
            id = event['cat_id']
            cat_list = id.split(',') 
            
        dynamodb_client = boto3.client('dynamodb', region_name=&quot;us-east-2&quot;)
        try:
            resp = []
            for i in cat_list:
                response = dynamodb_client.query(
                TableName='CATS',
                KeyConditionExpression='cat_id = :a',
                ExpressionAttributeValues={
                        ':a': {'S': i}
                        }
                )
                resp.append(response['Items'])
            
            return {    
                'statusCode': 200,    
                'body': resp
            }
            
        except:
            return {    
                'statusCode': 400,    
                'body': json.dumps(f&quot;We could not retrieve these cats.&quot;)  
            }
</code></pre>
<p>How should I rewrite this function with a batch_get_item() method? The most important thing for me is to be able to retrieve items with query string for example /list?id=1,2,3</p>
<p>Thank you in advance</p>

