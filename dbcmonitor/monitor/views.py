import json
from django.shortcuts import HttpResponse, render_to_response

from monitor.models import Organization, Replication, ReplicationStatus, \
    Database, Table, TableStatus

from monitor.utils.update import update_rep_status


def home(request):
    template = 'monitor.html'
    db_status_list = []
    for db in Database.objects.all():
        db_status = {}
        db_status['name'] = db.name
        db_status['slave'] = db.replication
        db_status['master'] = db.replication.master_rep
        db_status['date'] = db.status_date

        last_master_status = \
            ReplicationStatus.objects.filter(
                replication=db_status['master']
            ).last()

        last_slave_status = \
            ReplicationStatus.objects.filter(
                replication=db_status['slave']
            ).last()

        master_status = last_master_status.conn_status
        slave_status = last_slave_status.conn_status

        if master_status != 'connected' or slave_status != 'connected':
            continue

        table_list = []
        for t in Table.objects.filter(database=db):
            t_status = TableStatus.objects.filter(table=t).last()

            table = {}
            table['name'] = t.name
            table['status'] = t_status.status
            table['database'] = db
            table['master'] = db_status['master']
            table['slave'] = db_status['slave']

            table_list.append(table)

            if t_status.status != 'pass':
                db_status['status'] = 'FAIL'

        db_status['tables'] = table_list
        db_status_list.append(db_status)

    rep_list = []

    for rep in Replication.objects.all():
        last_status = ReplicationStatus.objects.filter(replication=rep).last()
        rep_status = {}
        rep_status['name'] = rep.host_name
        rep_status['status'] = last_status.conn_status
        rep_status['status_date'] = last_status.status_date

        rep_list.append(rep_status)

    context = {
        'databases': db_status_list,
        'replications': rep_list,
    }
    return render_to_response(template, context)


def check_replication(request):
    html = "<html><body>Monitor Replication Request Page</body></html>"

    return HttpResponse(html)


def save_replication_status(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        m_query = Replication.objects.filter(host_name=json_data['host'])
        if m_query.exists():
            master = m_query.first()
        else:
            master = Replication()
            master.host_name = json_data['host']
            # FIXME: Handle others organizations
            organization_q = Organization.objects.all()

            if not organization_q.exists():
                return HttpResponse("Replication must be of some organization",
                                    status=500)

            master.organization = organization_q.first()

        if json_data['token'] != master.organization.token:
            return HttpResponse('Unauthorized', status=401)

        master.save()

        # Save or Update Master Status
        update_rep_status(master, json_data)

        # Save or Update Each Slave
        slaves = json_data['slaves']
        for data in slaves:
            s_query = Replication.objects.filter(host_name=data['host'])

            if s_query.exists():
                slave = s_query.first()
                slave.master_rep = master
            else:
                slave = Replication()
                slave.host_name = data['host']
                slave.master_rep = master
                slave.organization = slave.master_rep.organization

            slave.save()

            update_rep_status(slave, data)

            databases = data['databases']

            for db in databases:
                db_query = Database.objects.filter(name=db['name'],
                                                   replication=slave)
                if db_query.exists():
                    database = db_query.first()
                else:
                    database = Database()
                    database.replication = slave
                    database.name = db['name']
                    database.status_date = db['date']
                    database.save()

                for name, status in db['tables'].items():
                    t_query = Table.objects.filter(name=name,
                                                   database=database)
                    table = t_query.last()
                    if not table:
                        table = Table()
                        table.database = database
                        table.name = name

                    table.last_status = status
                    table.save()

                    t_status = TableStatus.objects.filter(table=table)
                    last_status = t_status.last()

                    if last_status and last_status.status == status:
                        table_status = last_status
                    else:
                        table_status = TableStatus()
                        table_status.table = table
                        table_status.status = status
                        table_status.save()

    return HttpResponse()
