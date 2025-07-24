# Postfix: Bounce checking. Emails are piped to php but prevents emails from being sent and received properly
[Link to question](https://stackoverflow.com/questions/22979379/postfix-bounce-checking-emails-are-piped-to-php-but-prevents-emails-from-being)
**Creation Date:** 1397107952
**Score:** 2
**Tags:** php, email, postfix-mta, email-bounces
## Question Body
<p>I was told to repost this here in stackoverflow as it may not actually be a postfix issue. However, I do not know enough about the php postfix interactivity, so if there is a problem with the script portion and someone can see it please let me know. I am not sure if there is a special way to get the mail to pass on as it should (either in or out) normally, once it passes through the script, if that is even the issue. Thank you!</p>

<p>--</p>

<p>As I was working, I made a guide of what I was doing, for future use. I have been trying to get this to work for some time and I have gotten the emails to pass through the script. The problem all received mail, bounced or otherwise, is not being put into the mailbox after it is received and the script is done running. The script does run and do everything inside and exits without error, might I add.</p>

<ol>
<li><p>Add directory:
$sudo mkdir /usr/local/bouncehandler</p></li>
<li><p>Add script file to /usr/local/bouncehandler:
mybh.php</p></li>
<li><p>Allow execution of script:
chmod a+x mybh.php</p></li>
<li><p>Add user:
$sudo useradd bounce</p></li>
<li><p>(Create /etc/postfix/virtual_aliases to add a catch-all alias -- localuser needs to be an existing local user:
bounces@bounces.mydomain.com    root:) <strong>THIS WHOLE STEP WAS REMOVED</strong></p></li>
<li><p>Create /etc/postfix/transport to add a transport mapping. "mytransportname" can be whatever you want; it's used below in master.cf:
mydomain.com    mybh:</p></li>
<li><p>Next, both transport and virtual_aliases need to be compiled into db files:
($sudo postmap /etc/postfix/virtual_aliases)<strong>REMOVED</strong>
$sudo postmap /etc/postfix/transport</p></li>
<li><p>Change in /etc/postfix/master.cf:
smtp      inet  n       -       -       -       -       smtpd
    (-o content_filter=mybh:dummy)<strong>REMOVED</strong></p></li>
<li><p>Add the transport to /etc/postfix/master.cf:
mybh      unix  -       n       n       -       10       pipe
flags=q user=bounce argv=/usr/local/bouncehandler/mybh.php ${sender} ${recipient}</p></li>
<li><p>Change in /etc/postfix/master.cf:</p>

<p>pickup    fifo  n       -       -       60      1       pickup
(-o content_filter=mybh:dummy)<strong>REMOVED</strong></p></li>
<li><p>In /etc/postfix/main.cf:</p></li>
</ol>

<p>transport_maps = hash:/etc/postfix/transport
(virtual_alias_maps = hash:/etc/postfix/virtual_aliases))<strong>REMOVED</strong></p>

<ol>
<li><p>Connect to database and create table bounce_list:</p>

<p>CREATE TABLE IF NOT EXISTS bounce_list 
(
email VARCHAR(255) NOT NULL PRIMARY KEY,
bounce_count INT(4) NOT NULL
)ENGINE=InnoDB;</p></li>
<li><p>Restart Postfix:</p></li>
</ol>

<p>$sudo postfix reload</p>

<p>The script that I pass it through check if the recipient is my domain, which I believe would indicate that it is sent to me. Then if it was, I check if it was initially sent to someone else, and if so, I check the user and count the email as having been bounced. I do not doing anything else in the script, so I am not sure if after that I am supposed to some how call the original mail script if there is one.</p>

<p>mybh.php:</p>

<pre><code>#!/usr/bin/php -q
&lt;?php

////////////////////////////////////////////////////////
//Collects sender and recipient data from email pass
////////////////////////////////////////////////////////
$sender = trim($argv[1]);
$recipient = trim($argv[2]);


$bounceProcd = FALSE;

list($name, $domain) = explode('@', $recipient);


if(strpos($recipient, 'mydomain.com') !== false)
{

    ////////////////////////////////////////////////////////
    //Database variable initialization
    ////////////////////////////////////////////////////////
    $host = "localhost";
    $user = "user";
    $pass = "password";
    $db = "database";

    ////////////////////////////////////////////////////////
    //Establish database connection
    ////////////////////////////////////////////////////////
    $con = mysqli_connect($host, $user, $pass, $db);

    ////////////////////////////////////////////////////////
    //Verify that database is connected properly
    ////////////////////////////////////////////////////////
    if(!$con)
    {
        exit(75);
    }

    ////////////////////////////////////////////////////////
    //Initialize query into variable
    ////////////////////////////////////////////////////////
    $query = "INSERT INTO bounce_list VALUES ('$recipient', 1) ON DUPLICATE KEY UPDATE bounce_count = bounce_count + 1";

    ////////////////////////////////////////////////////////
    //Run query and store in variable
    ////////////////////////////////////////////////////////
    $result = mysqli_query($con, $query);

    $bounceProcd = mysqli_affected_rows($con) &gt; 0;

    ////////////////////////////////////////////////////////
    //Verify that query executed
    ////////////////////////////////////////////////////////
    if (!$result) {

        $con-&gt;close();

        exit(75);
    }


    $con-&gt;close();

    $dataLen = IgnoreMessageData();
}


$exitStatus = (TRUE == $bounceProcd) ? 0 : 75;

////////////////////////////////////////////////////////
//Pass email to mailbox
////////////////////////////////////////////////////////
exit($exitStatus+0);


function IgnoreMessageData()
{
    $msgLen = 0;
    $fd = fopen('php://stdin', 'r');
    while (FALSE === feof($fd))
    {
        $dunsel = fread($fd, 1024);
        $msgLen += strlen($dunsel);
    }
    fclose($fd);
    return $msgLen;
}
return;
?&gt;
</code></pre>

<p>main.cf:</p>

<pre><code># See /usr/share/postfix/main.cf.dist for a commented, more complete
version
# Debian specific:  Specifying a file name will cause the first
# line of that file to be used as the name.  The Debian default
# is /etc/mailname.
#myorigin = /etc/mailname

smtpd_banner = $myhostname ESMTP $mail_name (Ubuntu)

biff = no

# appending .domain is the MUA's job.
append_dot_mydomain = no

# Uncomment the next line to generate "delayed mail" warnings
#delay_warning_time = 4h
readme_directory = no

# TLS parameters
smtpd_tls_cert_file=/etc/ssl/certs/ssl­cert­snakeoil.pem

smtpd_tls_key_file=/etc/ssl/private/ssl­cert­snakeoil.key

smtpd_use_tls=yes

smtpd_tls_session_cache_database = btree:${data_directory}/smtpd_scache

smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache

# See /usr/share/doc/postfix/TLS_README.gz in the postfix­doc package for
# information on enabling SSL in the smtp client.

myhostname = main.mydomain.com

alias_maps = hash:/etc/aliases

alias_database = hash:/etc/aliases

smtp_generic_maps = hash:/etc/postfix/generic

myorigin = /etc/mailname

mydestination = admin.mydomain.com, main.mydomain.com,  
localhost.mydomain.com, localhost

relayhost =

mynetworks = (deleted this line)

mailbox_size_limit = 0

recipient_delimiter = +

inet_interfaces = all

transport_maps = hash:/etc/postfix/transport
</code></pre>

<p>master.cf:</p>

<pre><code>#
# Postfix master process configuration file.  For details on the format
# of the file, see the master(5) manual page (command: "man 5 master").
#
# Do not forget to execute "postfix reload" after editing this file.
#
# ==========================================================================
# service type  private unpriv  chroot  wakeup  maxproc command + args
#               (yes)   (yes)   (yes)   (never) (100)
# ==========================================================================
smtp      inet  n       -       -       -       -       smtpd

mybh      unix  -       n       n       -       -       pipe
    flags=q user=bounce argv=/usr/local/bouncehandler/mybh.php ${sender} ${recipient}

#smtp      inet  n       -       -       -       1       postscreen
#smtpd     pass  -       -       -       -       -       smtpd
#dnsblog   unix  -       -       -       -       0       dnsblog
#tlsproxy  unix  -       -       -       -       0       tlsproxy
#submission inet n       -       -       -       -       smtpd
#  -o syslog_name=postfix/submission
#  -o smtpd_tls_security_level=encrypt
#  -o smtpd_sasl_auth_enable=yes
#  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
#  -o milter_macro_daemon_name=ORIGINATING
#smtps     inet  n       -       -       -       -       smtpd
#  -o syslog_name=postfix/smtps
#  -o smtpd_tls_wrappermode=yes
#  -o smtpd_sasl_auth_enable=yes
#  -o smtpd_client_restrictions=permit_sasl_authenticated,reject
#  -o milter_macro_daemon_name=ORIGINATING
#628       inet  n       -       -       -       -       qmqpd

pickup    fifo  n       -       -       60      1       pickup

cleanup   unix  n       -       -       -       0       cleanup
qmgr      fifo  n       -       n       300     1       qmgr
#qmgr     fifo  n       -       n       300     1       oqmgr
tlsmgr    unix  -       -       -       1000?   1       tlsmgr
rewrite   unix  -       -       -       -       -       trivial-rewrite
bounce    unix  -       -       -       -       0       bounce
defer     unix  -       -       -       -       0       bounce
trace     unix  -       -       -       -       0       bounce
verify    unix  -       -       -       -       1       verify
flush     unix  n       -       -       1000?   0       flush
proxymap  unix  -       -       n       -       -       proxymap
proxywrite unix -       -       n       -       1       proxymap
smtp      unix  -       -       -       -       -       smtp
relay     unix  -       -       -       -       -       smtp
#       -o smtp_helo_timeout=5 -o smtp_connect_timeout=5
showq     unix  n       -       -       -       -       showq
error     unix  -       -       -       -       -       error
retry     unix  -       -       -       -       -       error
discard   unix  -       -       -       -       -       discard
local     unix  -       n       n       -       -       local
virtual   unix  -       n       n       -       -       virtual
lmtp      unix  -       -       -       -       -       lmtp
anvil     unix  -       -       -       -       1       anvil
scache    unix  -       -       -       -       1       scache
#
# ====================================================================
# Interfaces to non-Postfix software. Be sure to examine the manual
# pages of the non-Postfix software to find out what options it wants.
#
# Many of the following services use the Postfix pipe(8) delivery
# agent.  See the pipe(8) man page for information about ${recipient}
# and other message envelope options.
# ====================================================================
#
# maildrop. See the Postfix MAILDROP_README file for details.
# Also specify in main.cf: maildrop_destination_recipient_limit=1
#
maildrop  unix  -       n       n       -       -       pipe
  flags=DRhu user=vmail argv=/usr/bin/maildrop -d ${recipient}
#
# ====================================================================
#
# Recent Cyrus versions can use the existing "lmtp" master.cf entry.
#
# Specify in cyrus.conf:
#   lmtp    cmd="lmtpd -a" listen="localhost:lmtp" proto=tcp4
#
# Specify in main.cf one or more of the following:
#  mailbox_transport = lmtp:inet:localhost
#  virtual_transport = lmtp:inet:localhost
#
# ====================================================================
#
# Cyrus 2.1.5 (Amos Gouaux)
# Also specify in main.cf: cyrus_destination_recipient_limit=1
#
#cyrus     unix  -       n       n       -       -       pipe
#  user=cyrus argv=/cyrus/bin/deliver -e -r ${sender} -m ${extension} ${user}
#
# ====================================================================
# Old example of delivery via Cyrus.
#
#old-cyrus unix  -       n       n       -       -       pipe
#  flags=R user=cyrus argv=/cyrus/bin/deliver -e -m ${extension} ${user}
#
# ====================================================================
#
# See the Postfix UUCP_README file for configuration details.
#
uucp      unix  -       n       n       -       -       pipe
  flags=Fqhu user=uucp argv=uux -r -n -z -a$sender - $nexthop!rmail ($recipient)
#
# Other external delivery methods.
#
ifmail    unix  -       n       n       -       -       pipe
  flags=F user=ftn argv=/usr/lib/ifmail/ifmail -r $nexthop ($recipient)
bsmtp     unix  -       n       n       -       -       pipe
  flags=Fq. user=bsmtp argv=/usr/lib/bsmtp/bsmtp -t$nexthop -f$sender $recipient
scalemail-backend unix  -   n   n   -   2   pipe
  flags=R user=scalemail argv=/usr/lib/scalemail/bin/scalemail-store ${nexthop} ${user} ${extension}
mailman   unix  -       n       n       -       -       pipe
  flags=FR user=list argv=/usr/lib/mailman/bin/postfix-to-mailman.py
  ${nexthop} ${user}
</code></pre>

<p>mail.log:</p>

<blockquote>
  <p>Apr 16 05:55:37 serverName postfix/pickup[1774]: 48F1F2C0663: uid=0
  from=</p>
  
  <p>Apr 16 05:55:37 serverName postfix/cleanup[1789]: 48F1F2C0663:
  message-id=&lt;20140416055537.48F1F2C0663@serverName.mydomain.com></p>
  
  <p>Apr 16 05:55:37 serverName postfix/qmgr[1773]: 48F1F2C0663:
  from=, size=294, nrcpt=1 (queue active)</p>
  
  <p>Apr 16 05:55:58 serverName postfix/smtp[1791]: 48F1F2C0663:
  to=&lt;12356fdgjn56y23refsdv2ecwsdf21dfsdf@drdrb.net>,
  relay=mail.digitalsanctuary.com[174.73.49.123]:52, delay=40,
  delays=19/0.01/0.42/20, dsn=5.1.1, status=bounced (host
  mail.digitalsanctuary.com[174.37.94.132] said: 550 5.1.1
  &lt;12356fdgjn56y23refsdv2ecwsdf21dfsdf@drdrb.net>: Recipient address
  rejected: User unknown in virtual alias table (in reply to RCPT TO
  command))</p>
  
  <p>Apr 16 05:55:58 serverName postfix/cleanup[1789]: 3F13A2C0869:
  message-id=&lt;20140614055558.3F13A2C0869@serverName.mydomain.com></p>
  
  <p>Apr 16 05:55:58 serverName postfix/bounce[1800]: 48F1F2C0663: sender
  non-delivery notification: 3F13A2C0869</p>
  
  <p>Apr 16 05:55:58 serverName postfix/qmgr[1773]: 3F13A2C0869: from=&lt;>,
  size=2513, nrcpt=1 (queue active)</p>
  
  <p>Apr 16 05:55:58 serverName postfix/qmgr[1773]: 48F1F2C0663: removed</p>
  
  <p>Apr 16 05:55:58 serverName postfix/pipe[1801]: 3F13A2C0869:
  to=, relay=mybh, delay=0.04,
  delays=0/0/0/0.03, dsn=2.0.0, status=sent (delivered via mybh service)</p>
  
  <p>Apr 16 05:55:58 serverName postfix/qmgr[1773]: 3F13A2C0869: removed</p>
</blockquote>

<p>I have included all information that I thought may be helpful as from necessary info that I have seen for reading many guides and many other posts and tried to figure this out myself.</p>

<p>If a fresh pair of eyes can help me out, I would greatly appreciate this.</p>

<ul>
<li>I would also like to know, if anyone has an idea how to do this, append the original destination email to the bounced email.</li>
</ul>

<p>Thank you</p>

## Answers
### Answer ID: 23910126
<p>So when you add a filter you're basically saying I'll handle things from here, so in order to still receive the bounce message you need to send the message to the original recipient.</p>

<pre><code>// original bounce handling code

// Now resend the bounced message
// get message from stdin
$fp = fopen("php://stdin", "r");

$message= '';
while (! feof($fp)) {
    $message.= fgets($fp);
}

// send to original recipient, lazy but easiest just to pipe the message in to sendmail
shell_exec('echo ' . escapeshellarg($message) . ' | /usr/sbin/sendmail -G -i ' . $recipient);
</code></pre>

