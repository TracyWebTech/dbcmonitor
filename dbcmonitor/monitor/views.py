import json
from django.shortcuts import HttpResponse, render_to_response

from monitor.models import Organization, Replication, ReplicationStatus, \
    Database, Table, TableStatus

from monitor.utils.update import update_rep_status


def home(request):
    template = 'monitor.html'
    table_list = []
    for t in TableStatus.objects.all().order_by('-status_date'):
        database = t.table.database
        slave = database.replication
        master = slave.master_rep
        table_status = {}

        table_status['name'] = t.table.name
        table_status['status'] = t.status
        table_status['date'] = t.status_date
        table_status['database'] = database.name
        table_status['slave'] = slave
        table_status['master'] = master

        table_status['fail'] = False
        if t.status == "FAIL":
            table_status['fail'] = True

        table_list.append(table_status)

    rep_list = []

    for rep in ReplicationStatus.objects.all():
        rep_status = {}
        rep_status['name'] = rep.replication.host_name
        rep_status['status'] = rep.conn_status

        rep_list.append(rep_status)

    context = {
        'tables': table_list,
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
            master.organization = Organization.objects.all().first()

        if json_data['token'] != master.organization.token:
            return HttpResponse('Unauthorized', status=401)

        master.save()

        # Save or Update Master Status
        update_rep_status(master, json_data)

        # Save or Update Each Slave
        slaves = json_data['slaves']
        for data in slaves:
            s_query = Replication.objects.filter(host_name=data['host'],
                                                 master_rep=master)

            if s_query.exists():
                slave = s_query.first()
            else:
                slave = Replication()
                slave.master_rep = master
                slave.host_name = data['host']
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
                    database.save()

                for name, status in db['tables'].items():
                    t_query = Table.objects.filter(name=name,
                                                   database=database)
                    table = t_query.last()
                    if not table:
                        table = Table()
                        table.database = database
                        table.name = name
                        table.save()

                    t_status = TableStatus.objects.filter(table=table)
                    last_status = t_status.last()

                    if last_status and last_status.status == status:
                        table_status = last_status
                    else:
                        table_status = TableStatus()
                        table_status.table = table
                        table_status.status = status

                    table_status.status_date = db['date']
                    table_status.save()

    return HttpResponse()
