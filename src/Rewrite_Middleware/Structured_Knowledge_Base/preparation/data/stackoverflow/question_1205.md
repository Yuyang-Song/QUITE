# K8s/Kubernetes CoreDNS - add additional SRV or A records (manually)
[Link to question](https://stackoverflow.com/questions/63371961/k8s-kubernetes-coredns-add-additional-srv-or-a-records-manually)
**Creation Date:** 1597218037
**Score:** 2
**Tags:** kubernetes, dns, coredns
## Question Body
<p>I do have the requirement to setup SRV entries for specific application.</p>
<p>I am running a kubernetes cluster with coredns and kubernetes plugin enabled. By standard the coredns is creating an SRV entry in the coredns database.</p>
<p><strong>SRV record</strong></p>
<p><em>K8s service</em></p>
<pre><code>apiVersion: v1
kind: Service
metadata:
  labels:
    run: pod-nginx
  name: svc-nginx
  namespace: default
spec:
  ports:
  - name: test
    nodePort: 31985
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    run: pod-nginx
  type: LoadBalancer
</code></pre>
<p><em>Name resolution</em></p>
<p>I am able to get an answer from DNS query.</p>
<pre><code>root@test:/# dig -t srv _test._tcp.svc-nginx.default.svc.cluster.local

; &lt;&lt;&gt;&gt; DiG 9.16.1-Ubuntu &lt;&lt;&gt;&gt; -t srv _test._tcp.svc-nginx.default.svc.cluster.local
;; global options: +cmd
;; Got answer:
;; WARNING: .local is reserved for Multicast DNS
;; You are currently testing what happens when an mDNS query is leaked to DNS
;; -&gt;&gt;HEADER&lt;&lt;- opcode: QUERY, status: NOERROR, id: 28386
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 2
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
; COOKIE: 66150d8a64d0f92b (echoed)
;; QUESTION SECTION:
;_test._tcp.svc-nginx.default.svc.cluster.local.    IN SRV

;; ANSWER SECTION:
_test._tcp.svc-nginx.default.svc.cluster.local. 5 IN SRV 0 100 80 svc-nginx.default.svc.cluster.local.

;; ADDITIONAL SECTION:
svc-nginx.default.svc.cluster.local. 5 IN A 192.168.200.88

;; Query time: 4 msec
;; SERVER: 192.168.200.2#53(192.168.200.2)
;; WHEN: Wed Aug 12 07:23:48 UTC 2020
;; MSG SIZE  rcvd: 239
</code></pre>
<p>Unfortunatelly I do need another SRV string, as the application is expecting a different SRV resolution. I am not able to edit the application to fit the automatically created SRV string.</p>
<p>How can I manually add SRV entires into coreDNS?</p>
<p>current SRV record:</p>
<pre><code>_test._tcp.svc-nginx.default.svc.cluster.local. 5 IN SRV 0 100 80 svc-nginx.default.svc.cluster.local.
</code></pre>
<p>expected SRV record:</p>
<pre><code>_test._tcp.default.svc.cluster.local.   86400 IN SRV 0 0 80 svc-nginx.default.svc.cluster.local.
</code></pre>
<p><strong>A record</strong></p>
<p>How can I manually add A records into coreDNS? I don't want to use the &quot;rewrite plugin&quot; or the &quot;k8s_external plugin&quot;</p>
<p>current A record:</p>
<pre><code>svc-nginx.default.svc.cluster.local. 5 IN A 192.168.200.88
</code></pre>
<p>expected SRV record:</p>
<pre><code>myapp.cluster.local. 5 IN A 192.168.200.88
</code></pre>

## Answers
### Answer ID: 75700119
<p>According to <a href="https://coredns.io/manual/toc/#configuration" rel="nofollow noreferrer">docs</a>.</p>
<p>In your current directory, create a file named db.example.org and put the following contents in it:</p>
<pre><code>$ORIGIN example.org.
@   3600 IN SOA sns.dns.icann.org. noc.dns.icann.org. (
            2017042745 ; serial
            7200       ; refresh (2 hours)
            3600       ; retry (1 hour)
            1209600    ; expire (2 weeks)
            3600       ; minimum (1 hour)
            )

3600 IN NS a.iana-servers.net.
3600 IN NS b.iana-servers.net.

www     IN A     127.0.0.1
        IN AAAA  ::1

example.com.   IN   TXT   &quot;This domain name is reserved for use in documentation&quot;

_sip._tcp.example.com.   86400 IN    SRV 10       60     5060 bigbox.example.com.
</code></pre>
<p>Next, create this minimal Corefile that handles queries for this domain and adds the log plugin to enable query logging:</p>
<pre><code>example.org {
    file db.example.org
    log
}
</code></pre>
<p>Another <a href="https://savvythrough.medium.com/serve-using-coredns-file-plugin-23b4b1e20d96" rel="nofollow noreferrer">good reading on adding custom records</a></p>

