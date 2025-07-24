# Perl forking and IPC::Open2 exec pipes
[Link to question](https://stackoverflow.com/questions/27017770/perl-forking-and-ipcopen2-exec-pipes)
**Creation Date:** 1416402873
**Score:** 1
**Tags:** multithreading, perl, fork
## Question Body
<p>I'm running a script via cron every 5 minutes. This script collects a large number of performance metrics from across my environment, and uses them to update round robin databases using <code>rrdtool</code>. </p>

<p>At the moment, I'm doing so via <code>threads</code> and <code>Thread::Queue</code>. I have 'collector' threads, and 'updater' threads:</p>

<pre><code>#!/usr/bin/perl

use strict;
use warnings;

use IPC::Open2;
use Thread::Queue;
use English;

my $update_q = Thread::Queue-&gt;new();

sub updater {
    open2( my $rrdtool_response, my $rrdtool, "/usr/bin/rrdtool -" )
        or warn $OS_ERROR;
    while ( my $item = $update_q-&gt;dequeue ) {
        my ( $rrd, $data ) = split( /,/, $item );
        print {$rrdtool}
            "update --daemon /tmp/rrdcached.sock $rrd $data\n";
        my $result = &lt;$rrdtool_response&gt;;
        if ( not $result =~ m/^OK/ ) {
            print "$rrd $data $result\n";
            close($rrdtool_response);
            close($rrdtool);
            open2(
                my $rrdtool_response,
                my $rrdtool,
                "/usr/bin/rrdtool -"
            ) or warn $OS_ERROR;
        }
    }
    close($rrdtool_response);
    close($rrdtool);
}


for ( 1 .. $update_threads ) {
    my $thr = threads-&gt;create( \&amp;updater );
}
</code></pre>

<p>This updater will get fed a whole load of strings of the type of:</p>

<pre><code>"/path/to/data/file.rrd,N:1:4:3:2:234:3"; 
</code></pre>

<p>(That's the update format for <code>rrdtool</code> - <code>N</code> being 'now` and the colon separated values being the things to update).</p>

<p>Because I use a queue, it's serialised, and I can ensure I'm running an appropriate number of instances of rrdtool. </p>

<p>I collect around 20,000 metrics in this fashion every 5 minutes, and it broadly works ok. </p>

<p>I'm in the middle of a bit of a rewrite, to see if I can't get this to work with forking. I had intended to spawn multiple 'rrdtool' update instances, but slightly accidentally I did the <code>open2</code> outside the forked code. </p>

<p>E.g.:</p>

<pre><code>    open2( my $rrdtool_response, my $rrdtool, "/usr/bin/rrdtool -" )
        or warn $OS_ERROR;

    $manager -&gt; start and next 
    while ( my $item = $update_q-&gt;dequeue ) {
        my ( $rrd, $data ) = split( /,/, $item );
        print {$rrdtool}
            "update --daemon /tmp/rrdcached.sock $rrd $data\n";
        my $result = &lt;$rrdtool_response&gt;;
        if ( not $result =~ m/^OK/ ) {
            print "$rrd $data $result\n";
            close($rrdtool_response);
            close($rrdtool);
            open2(
                my $rrdtool_response,
                my $rrdtool,
                "/usr/bin/rrdtool -"
            ) or warn $OS_ERROR;
        }
    }


    close($rrdtool_response);
    close($rrdtool);
</code></pre>

<p>And because children inherit the filehandles, it <em>almost</em> worked. Printing to the <code>{$rrdtool}</code> filehandle worked. Re-opening it on error also worked. (You did end up with extra rrdtool instances, but 'a few' based on error rate, rather than the 20,000 I was trying to avoid). </p>

<pre><code>#!/usr/bin/perl

use strict;
use warnings;

use IPC::Open2;
use Parallel::ForkManager;
use English;

my $max_concurrency = 100;

my %metric_subs = (
    "fetch_iops" =&gt; \&amp;fetch_io_operations_on,

    #... more here;
);

sub fetch_io_operations_on {
    my ($hostname) = @_;
    my $rrd = "/path/to/data/$hostname/iops.rrd";

    #do some stuff to fetch data
    update_rrd( $rrd, $data );
}

{
    my $rrdtool;
    my $rrd_response;

    sub start_updates {
        open2( my $rrdtool_response, my $rrdtool, "/usr/bin/rrdtool -" )
            or warn $OS_ERROR;
    }

    sub update_rrd {
        my ( $rrd, $data ) = @ARG;
        print {$rrdtool}
            "update --daemon /tmp/rrdcached.sock $rrd $data\n";
        my $result = &lt;$rrdtool_response&gt;;
        if ( not $result =~ m/^OK/ ) {
            print "$rrd $data $result\n";
            close($rrdtool_response);
            close($rrdtool);
            open2(
                my $rrdtool_response,
                my $rrdtool,
                "/usr/bin/rrdtool -"
            ) or warn $OS_ERROR;
        }
    }

    sub end_updates {
        print {$rrdtool} "quit\n";
        close($rrdtool);
        close($rrdtool_response);
    }
}

##main

my $manager = Parallel::ForkManager-&gt;new($max_concurrency);

start_updates();
foreach my $host (@list_of_hosts) {
    foreach my $metric ( keys %metric_subs ) {
        $manager-&gt;start and next;
        ##parallel bit
        print "Fetching $metric on $host\n";
        &amp;{ $metric_subs{$metric} }($host);
        $manager-&gt;finish();
    }
}
end_updates();


$manager-&gt;wait_all_children();
</code></pre>

<p>This is broadly satisfactory - because the restart is within a forked child, you do end up with multiple rrdtool instances if there's an error, but they're all updating via rrdcached anyway, so that's acceptable. <code>ForkManager</code> limiting will ensure I don't get an absurd number </p>

<p>However I had started getting a few cases where 'response' query was blocking, and I realised that my IO to the process was effectively suffering race conditions. I started trying to match the 'update' and the 'responses' via debugging prints, but ... well, as I'm sure you'll have realised that because of buffering, there's not really any way to be sure that the fork who reads the response filehandle is also the one that printed the matching update to the update filehandle. </p>

<p>So - if I'm looking to do this in way that's a little less shoddy - what's the right way to handle exec pipes across forks in perl, such that I'm not building race conditions into my code? </p>

## Answers
### Answer ID: 27019945
<blockquote>
  <p><em>what's the right way to handle exec pipes across forks in perl, such that I'm not building race conditions into my code?</em></p>
</blockquote>

<p>It's very easy to ensure that only one child executes at a time, but then only one child would be executing at a time. That would defy the purpose of your multitasking.</p>

<hr>

<p>You reuse workers in your threaded model, but P::FM uses a new worker for each job.</p>

<p>As such, the initialization code you have outside the loop will need to be moved into the loop.</p>

<pre><code>for my $item (...) {
    $pm-&gt;start and next;
    open2( my $rrdtool_response, my $rrdtool, "/usr/bin/rrdtool -" )
        or warn $OS_ERROR;
    my ( $rrd, $data ) = split( /,/, $item );
    print { $rrdtool } "update --daemon /tmp/rrdcached.sock $rrd $data\n";
    my $result = &lt;$rrdtool_response&gt;;
    if ( not $result =~ m/^OK/ ) {
        print "$rrd $data $result\n";
        close($rrdtool_response);
        close($rrdtool);
        open2(
            my $rrdtool_response,
            my $rrdtool,
            "/usr/bin/rrdtool -"
        ) or warn $OS_ERROR;
    }

    close($rrdtool_response);
    close($rrdtool)
    $pm-&gt;finish();
}
</code></pre>

<p>This needs some cleanup.</p>

<ul>
<li>The whole relaunching of <code>rrdtool</code> is no longer useful. </li>
<li><code>open2</code> never returns false when provided a command. </li>
<li>You aren't reaping your <code>rrdtool</code> children. You need to call <code>waitpid</code>.</li>
</ul>

<p>&#x20;</p>

<pre><code>for my $item (...) {
    $pm-&gt;start and next;
    my $pid = open2( my $rrdtool_response, my $rrdtool, "/usr/bin/rrdtool -" );
    my ( $rrd, $data ) = split( /,/, $item );
    print { $rrdtool } "update --daemon /tmp/rrdcached.sock $rrd $data\n";
    my $result = &lt;$rrdtool_response&gt;;
    print "$rrd $data $result\n"
        if $result !~ /^OK/;

    close($rrdtool_response);
    close($rrdtool)
    waitpid($pid, 0);
    $pm-&gt;finish();
}
</code></pre>

