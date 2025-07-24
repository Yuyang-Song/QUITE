# How to run Background Services in parallel (on different threads) in a .NET 5 console application/windows service
[Link to question](https://stackoverflow.com/questions/69179234/how-to-run-background-services-in-parallel-on-different-threads-in-a-net-5-co)
**Creation Date:** 1631628110
**Score:** 0
**Tags:** vb.net, multithreading, dependency-injection, backgroundworker, .net-5
## Question Body
<p>It's pretty new to me using .NET Core/.NET 5 and Dependency Injection and I'm having trouble doing things I did my own way in .NET Framework 4.8.</p>
<p>My app is running 3 background services, and I would like to have them run in parallel on separate threads. Currently, if I output <code>Thread.CurrentThread.ManagedThreadId</code>, they all share the same thread, so if one is waiting for a DB query or doing something else, it's blocking other services. Each service is a <code>While True</code> loop (polling database, doing work, sleeping a minute or so, polling db, etc.) The 3 services are all related to our software, but not that much related one to the other, and do not interact with one an other.</p>
<p>I started the project as a Console Application using the template from VS, and did a little reading on how to make a Windows Service out of it, but now I'm a bit stuck on how doing these things.</p>
<p>What I would like to accomplish :</p>
<ol>
<li>Have my console app run my 3 main background services in parallel instead of sequentially or async (I would like to avoid rewriting everything to run async)</li>
<li>Be able to catch exceptions and restart each service a certain amount of times before failing completely</li>
</ol>
<p>Here is a sample from my code starting the program (in VB.NET because I'm kinda upgrading from an existing app in VB.NET, so I don't want to rewrite everything in C#, but you can give answers in C#, I'm used to translating) :</p>
<pre><code>Imports System.IO
Imports Microsoft.Extensions.Hosting
Imports Microsoft.Extensions.DependencyInjection
Imports Microsoft.Extensions.Configuration

Public Class Program
    Public Shared Sub Main(ByVal args As String())
        CreateHostBuilder(args).Build().Run()
    End Sub

    Public Shared Function CreateHostBuilder(ByVal args As String()) As IHostBuilder
        Return Host.CreateDefaultBuilder(args) _
        .ConfigureServices(
            Sub(hostContext, services)
                ' @TODO check how to handle crashed services
                services.AddHostedService(Of MyFirstService)()
                services.AddHostedService(Of MySecondService)()
                services.AddHostedService(Of MyThirdService)()
            End Sub) _
        .UseWindowsService(
            Sub(options)
                options.ServiceName = &quot;My Service&quot;
            End Sub)
    End Function
End Class
</code></pre>
<p>Here is the pattern of my services :</p>
<pre><code>Imports System.Threading
Imports Microsoft.Extensions.Hosting

Public Class MyFirstService

    Protected Overrides Async Function ExecuteAsync(stoppingToken As CancellationToken) As Task
        Do While True
            If stoppingToken.IsCancellationRequested Then
                ' Exit main loop when task is cancelled, so task will end
                Exit Do
            End If

            ' Do Useful Work, call database, etc.

            ' Sleep a little before checking back DB
            Await Task.Delay(60000, stoppingToken)
        Loop
    End Function
End Class
</code></pre>

