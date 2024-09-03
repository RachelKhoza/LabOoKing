import boto3
import requests

def lambda_handler(event, context):
    try:
        # Test connectivity to RDS endpoint
        response = requests.get("https://rds.us-east-1.amazonaws.com/")
        print(f"RDS endpoint connectivity status: {response.status_code}")
        
        rds = boto3.client('rds')
        db_instance_id = 'your-db-instance-id'  # Replace with your RDS instance ID

        snapshot_identifier = f"rds-snapshot-{db_instance_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"

        response = rds.create_db_snapshot(
            DBInstanceIdentifier=db_instance_id,
            DBSnapshotIdentifier=snapshot_identifier
        )
        print(f"Snapshot {snapshot_identifier} created successfully.")
    except Exception as e:
        print(f"Error creating snapshot: {str(e)}")

    return {
        "statusCode": 200,
        "body": f"Snapshot {snapshot_identifier} created."
    }