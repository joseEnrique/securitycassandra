#!/usr/bin/env python
import logging
import os
from cassandra.cluster import Cluster, AuthenticationFailed
from cassandra.auth import PlainTextAuthProvider
from time import sleep

log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)
newpass = os.getenv('CASSANDRA_PASSWORD')
ip = os.getenv('CASSANDRA_IP')
changed = False
while changed is False:
    try:
        auth_provider = PlainTextAuthProvider(
                username='cassandra', password='cassandra')
        cluster = Cluster(contact_points=[ip] , auth_provider=auth_provider)
        session = cluster.connect()
        rows = session.execute("ALTER ROLE cassandra WITH PASSWORD='"+newpass+"';")
        changed = True
        log.warning("Changed")
    except Exception as ex:
        if isinstance(ex.errors[ip],AuthenticationFailed):
            changed = True
            log.error("Password already changed")
        else:
            log.warning("Waiting ..")
            sleep(3)
