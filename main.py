#!/usr/bin/env python
import logging
import os
from cassandra.cluster import Cluster, AuthenticationFailed
from cassandra.auth import PlainTextAuthProvider
from cassandra import ConsistencyLevel
from time import sleep

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)
cluster = os.getenv('CASSANDRA_CLUSTER')
newpass = os.getenv('CASSANDRA_PASSWORD')
ip = os.getenv('CASSANDRA_IP')
changed = False
sleep(10)
while changed is False:
    try:
        auth_provider = PlainTextAuthProvider(
                username='cassandra', password='cassandra')
        cluster = Cluster(contact_points=[ip] , auth_provider=auth_provider)
        session = cluster.connect()
        rows = session.execute("ALTER ROLE cassandra WITH PASSWORD='"+newpass+"';")
        if cluster is "yes":
            query = SimpleStatement("ALTER KEYSPACE system_auth WITH replication = { 'class' : 'NetworkTopologyStrategy','dc1': 2};", consistency_level=ConsistencyLevel.ONE)
            session.execute(query)
        changed = True
        log.warning("Changed")
    except Exception as ex:
        if isinstance(ex.errors[ip],AuthenticationFailed):
            changed = True
            log.error("Password already changed")
        else:
            log.warning("Waiting ..")
            sleep(3)
