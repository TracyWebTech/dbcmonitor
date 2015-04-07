import datetime

from monitor.models import ReplicationStatus


def update_rep_status(replication, data):
    # Save or Update Replication Status
    all_last_status = ReplicationStatus.objects.filter(replication=replication)
    last_status = all_last_status.last()

    if last_status and \
       last_status.conn_status == data['status'] and \
       last_status.log_file == data['log_file'] and \
       last_status.log_position == int(data['log_position']):
        last_status.status_date = datetime.datetime.now()

    else:
        last_status = ReplicationStatus()
        last_status.replication = replication
        last_status.conn_status = data['status']
        last_status.log_file = data['log_file']
        last_status.log_position = data['log_position']

    last_status.status_date = datetime.datetime.now()
    last_status.save()
