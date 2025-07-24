# Python: Rewriting query within TCP payload using nfqueue/scapy
[Link to question](https://stackoverflow.com/questions/49371026/python-rewriting-query-within-tcp-payload-using-nfqueue-scapy)
**Creation Date:** 1521488094
**Score:** 0
**Tags:** python, tcp, scapy, payload
## Question Body
<p>I'm in no way a networking expert so there is possibly something obvious I am missing here. I'm attempting to rewrite a database query within a TCP payload. I have been able to get this to work for a single scenario but for others it is not working and I don't know why.</p>

<p><strong>Got to Work</strong>:</p>

<p>Changing - 'select * from test1' TO 'select * from test2'</p>

<p><strong>Doesn't Work</strong>: </p>

<p>Changing - 'Select * from test1' TO 'select * from test50'</p>

<ul>
<li>Is this not working due to a change in the size of the payload?</li>
</ul>

<p>Here is an example of my code:</p>

<pre><code>import nfqueue
from scapy.all import *
import os
import sys

iptable_change = "iptables -A OUTPUT -p tcp --dport 8008 -j NFQUEUE"
os.system(iptable_change)


def callback(payload):
    data = payload.get_data()
    pkt = IP(data)
    if pkt.src == '127.0.0.1':
        if 'test1' in pkt[Raw].load:
            pkt[TCP].payload = str(pkt[TCP].payload).replace("test1", "test50")
            del pkt[IP].chksum
            del pkt[TCP].chksum
            payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(pkt), len(pkt))


def main():
    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)
    q.set_callback(callback)
    q.create_queue(0)
    try:
        q.try_run()
    except KeyboardInterrupt:
        q.unbind(socket.AF_INET)
        q.close()


if __name__ == "__main__":
    main()
</code></pre>

<p>Is there something I am missing here? Because I am changing a db query do packets need to be handled differently?</p>

## Answers
### Answer ID: 49470237
<p>If you change the length of a TCP packet, then you have to fix the following sequence and acknowledgment numbers... which is hard.</p>

<p>If you need to tamper with the content of a TCP connection, I'd suggest you just DNAT the connection to a TCP proxy you write (a simple TCP server that establishes a connection to the original server and forwards the data between the two endpoints). This way, you let your host's network stack deal with TCP sequence and acknowledgment numbers.</p>

