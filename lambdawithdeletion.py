import boto3
import datetime

def lambda_handler(event, context):
    rds = boto3.client('rds')
    db_instance_id = 'your-db-instance-id'  # Replace with your RDS instance ID

    # Create a snapshot identifier with a timestamp
    snapshot_identifier = f"rds-snapshot-{db_instance_id}-{datetime.datetime.now().strftime('%Y%m%d%H%M')}"

    # Create the snapshot
    try:
        rds.create_db_snapshot(
            DBInstanceIdentifier=db_instance_id,
            DBSnapshotIdentifier=snapshot_identifier
        )
        print(f"Snapshot {snapshot_identifier} created successfully.")
    except Exception as e:
        print(f"Error creating snapshot: {str(e)}")
    
    # Calculate the cutoff date for deletion (7 days ago)
    cutoff_date = datetime.datetime.now() - datetime.timedelta(days=7)

    # List all snapshots for the specified DB instance
    try:
        snapshots = rds.describe_db_snapshots(
            DBInstanceIdentifier=db_instance_id,
            SnapshotType='manual'  # Only consider manual snapshots
        )['DBSnapshots']

        # Iterate through snapshots and delete those older than 7 days
        for snapshot in snapshots:
            snapshot_id = snapshot['DBSnapshotIdentifier']
            snapshot_create_time = snapshot['SnapshotCreateTime'].replace(tzinfo=None)

            if snapshot_create_time < cutoff_date:
                rds.delete_db_snapshot(DBSnapshotIdentifier=snapshot_id)
                print(f"Deleted snapshot: {snapshot_id}")

    except Exception as e:
        print(f"Error listing or deleting snapshots: {str(e)}")

    return {
        "statusCode": 200,
        "body": f"Snapshot {snapshot_identifier} created, old snapshots deleted."
    }