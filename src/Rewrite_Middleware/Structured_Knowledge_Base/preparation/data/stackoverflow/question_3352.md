# slapd configuration database meta unknown directive &lt;acl-authcDN&gt;
[Link to question](https://stackoverflow.com/questions/77038101/slapd-configuration-database-meta-unknown-directive-acl-authcdn)
**Creation Date:** 1693833806
**Score:** 1
**Tags:** active-directory, ldap, openldap
## Question Body
<p>i'm new to openldap and trying to setup a ldap service, to act like an Active Directory. I'm using scripts of dkoudela (<a href="https://github.com/dkoudela/active-directory-to-openldap/tree/master" rel="nofollow noreferrer">https://github.com/dkoudela/active-directory-to-openldap/tree/master</a>).
To provide rewrite of MS non-standard LDAP Search queries, i try to setup meta database in my slapd.conf.</p>
<p>In this section &quot;acl-authcDN&quot; is used, which (according to slapd-meta's man page) is supported. Anyways i'm getting <code>unknown directive &lt;acl-authcDN&gt; inside backend database definition</code> when running <code>slaptest -f slapd.conf</code>.</p>
<p>Does anyone see whats wrong?</p>
<p>Thanks &amp; cheers
Zwaem</p>
<p>My slapd.conf:</p>
<pre><code>#
# See slapd.conf(5) for details on configuration options.
# This file should NOT be world readable.
#

include     /root/openldap/schema/microsoftattributetype.schema
include     /root/openldap/schema/microsoftattributetypestd.schema
include     /root/openldap/schema/corba.schema
include     /root/openldap/schema/core.schema
include     /root/openldap/schema/cosine.schema
include     /root/openldap/schema/duaconf.schema
include     /root/openldap/schema/dyngroup.schema
include     /root/openldap/schema/inetorgperson.schema
include     /root/openldap/schema/java.schema
include     /root/openldap/schema/misc.schema
include     /root/openldap/schema/nis.schema
include     /root/openldap/schema/openldap.schema
include     /root/openldap/schema/ppolicy.schema
include     /root/openldap/schema/collective.schema
include     /root/openldap/schema/microsoftobjectclass.schema


# Allow LDAPv2 client connections.  This is NOT the default.
allow bind_v2


pidfile     /var/run/openldap/slapd.pid
argsfile    /var/run/openldap/slapd.args


modulepath /usr/lib64/openldap
moduleload back_meta.la
moduleload back_ldap.la
moduleload rwm.la

TLSCACertificatePath /etc/openldap/certs
TLSCertificateFile &quot;\&quot;OpenLDAP Server\&quot;&quot;
TLSCertificateKeyFile /etc/openldap/certs/password


database config
access to *
    by dn.exact=&quot;gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth&quot; manage
    by * none

# enable server status monitoring (cn=monitor)
database monitor
access to *
    by dn.exact=&quot;gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth&quot; read
        by dn.exact=&quot;cn=Manager,dc=example,dc=com&quot; read
        by * none

#######################################################################
# database definitions
#######################################################################

#######################################################################
# Meta backend providing rewrite of MS non-standard LDAP Search queries
#######################################################################
database        meta
suffix          &quot;dc=sub,dc=example,dc=com&quot;
uri             &quot;ldap://0.0.0.0/dc=sub,dc=example,dc=com&quot;
suffixmassage   &quot;dc=sub,dc=example,dc=com&quot; &quot;dc=example,dc=com&quot;
acl-authcDN     &quot;cn=Manager,dc=example,dc=com&quot;
acl-passwd xtime
rebind-as-user
rewriteEngine   on
rewriteContext  searchFilter
rewriteRule     &quot;(.*)objectCategory=[a-zA-Z]+(.*)&quot; &quot;%1objectCategory=cn=Person*%2&quot; &quot;:&quot;

#######################################################################
# Configuration backend providing config and schema settings
#######################################################################
database    config
rootdn      &quot;cn=config&quot;
rootpw  xtime

#######################################################################
# Database backend containing the LDAP data
#######################################################################
database    bdb
suffix      &quot;dc=example,dc=com&quot;
checkpoint  1024 15
rootdn      &quot;cn=Manager,dc=example,dc=com&quot;
# Cleartext passwords, especially for the rootdn, should
# be avoided.  See slappasswd(8) and slapd.conf(5) for details.
# Use of strong authentication encouraged.
# rootpw        secret
# rootpw        {crypt}ijFYNcSNctBYg
rootpw  xtime

# The database directory MUST exist prior to running slapd AND 
# should only be accessible by the slapd and slap tools.
# Mode 700 recommended.
directory   /var/lib/ldap

# Indices to maintain for this database
index objectClass                       eq,pres
index ou,cn,mail,surname,givenname      eq,pres,sub
index uidNumber,gidNumber,loginShell    eq,pres
index uid,memberUid                     eq,pres,sub
index nisMapName,nisMapEntry            eq,pres,sub
index objectCategory,sAMAccountName     eq,pres,sub

# Replicas of this database
#replogfile /var/lib/ldap/openldap-master-replog
#replica host=ldap-1.example.com:389 starttls=critical
#     bindmethod=sasl saslmech=GSSAPI
#     authcId=host/ldap-master.example.com@EXAMPLE.COM

</code></pre>

