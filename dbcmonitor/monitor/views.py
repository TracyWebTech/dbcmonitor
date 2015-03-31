from django.shortcuts import HttpResponse
from django.http import HttpResponse
import json

from monitor.models import Replication, SlaveReplication, DatabaseStatus, \
    TableStatus


def home(request):
    html = "<html><body>Monitor Home Page</body></html>" 
    return HttpResponse(html)


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
            master.log_file = json_data['log_file']

        master.log_position = json_data['log_position']
        master.save()

        slaves = json_data['slaves']
        for s in slaves:
            #FIXME: Others filters to identify object
            s_query = SlaveReplication.objects.filter(host_name=s['host'])
            if s_query.exists():
                slave = s_query.first()
            else:
                print("_"*100)
                print("Nao existe. Vou criar o slave")
                slave = SlaveReplication()
                slave.master_rep = master
                slave.host_name = s['host']
                slave.log_file = s['log_file']

            slave.log_position = s['log_position']
            slave.save()

            databases = s['databases']
            for db in databases:
                #FIXME: Others filters to identify object
                db_query = DatabaseStatus.objects.filter(name=db['name'])
                if db_query.exists():
                    comp_db = db_query.first()
                else:
                    comp_db = DatabaseStatus()
                    comp_db.replication = slave
                    comp_db.name = db['name']
                    comp_db.save()

                for name,status in db['tables'].items():
                    t_query = TableStatus.objects.filter(name=name)
                    if t_query.exists():
                        table = t_query.first()
                    else:
                        table = TableStatus()
                        table.name = name
                        table.database = comp_db

                    table.status = status
                    table.save()

    return HttpResponse()
