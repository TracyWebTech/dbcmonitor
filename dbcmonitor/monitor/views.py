import json
from django.shortcuts import HttpResponse, render_to_response

from monitor.models import Organization, Replication, SlaveReplication, \
    DatabaseStatus, TableStatus


def home(request):
    template = 'monitor.html'
    table_list = []
    for t in TableStatus.objects.all():
        database = t.database
        slave = database.replication
        master = slave.master_rep
        table_status = {}

        table_status['name'] = t.name
        table_status['status'] = t.status
        table_status['date'] = t.status_date
        table_status['database'] = database.name
        table_status['slave'] = slave
        table_status['master'] = master

        table_list.append(table_status)

    context = {
        'tables': table_list,
    }
    return render_to_response(template, context)


def check_replication(request):
    html = "<html><body>Monitor Replication Request Page</body></html>"

    return HttpResponse(html)


def save_replication_status(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)

        if json_data['token'] != 'bananabananabanana':
            return HttpResponse('Unauthorized', status=401)

        m_query = Replication.objects.filter(host_name=json_data['host'])
        if m_query.exists():
            master = m_query.first()
        else:
            master = Replication()
            master.host_name = json_data['host']
            master.conn_status = json_data['status']
            master.log_file = json_data['log_file']

        master.log_position = json_data['log_position']
        master.save()

        slaves = json_data['slaves']
        for s in slaves:
            # FIXME: Others filters to identify object
            s_query = SlaveReplication.objects.filter(host_name=s['host'])
            if s_query.exists():
                slave = s_query.first()
            else:
                slave = SlaveReplication()
                slave.master_rep = master
                slave.host_name = s['host']
                slave.log_file = s['log_file']

            slave.conn_status = s['status']
            slave.log_position = s['log_position']
            slave.save()

            databases = s['databases']
            for db in databases:
                # FIXME: Others filters to identify object
                db_query = DatabaseStatus.objects.filter(name=db['name'])
                if db_query.exists():
                    comp_db = db_query.first()
                else:
                    comp_db = DatabaseStatus()
                    comp_db.replication = slave
                    comp_db.name = db['name']
                    comp_db.save()

                for name, status in db['tables'].items():
                    t_query = TableStatus.objects.filter(name=name)
                    if t_query.exists():
                        table = t_query.first()
                    else:
                        table = TableStatus()
                        table.name = name
                        table.database = comp_db

                    table.status = status
                    table.status_date = db['date']
                    table.save()

    return HttpResponse()
