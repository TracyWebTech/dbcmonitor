
from django.db import models


class ReplicationManager(models.Manager):

    def masters(self):
        return self.distinct().values_list('master', flat=True)

    def slaves(self):
        return self.distinct().values_list('slave', flat=True)

    def current_status(self, database_pk):
        status_dict = {}

        for replication in self.filter(database__pk=database_pk):
            master_row = status_dict.get(replication.master)
            if not master_row:
                master_row = dict.fromkeys(self.slaves())
                status_dict[replication.master] = master_row

            master_row[replication.slave] = replication.status.latest()

        return status_dict

    def status_table(self, database_pk):
        current_status = self.current_status(database_pk)

        table_header = current_status.values()[0].keys()
        table_header.insert(0, None)

        table = [table_header]
        for master, slave_dict in current_status.items():
            row = [master]
            for slave in slave_dict.values():
                if slave:
                    row.append(slave)
                else:
                    row.append(None)
            table.append(row)

        return table
