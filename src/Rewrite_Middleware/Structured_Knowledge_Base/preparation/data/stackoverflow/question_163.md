# Querying Crystal Server 2011 CMS on VS2012 and Win8 64bit?
[Link to question](https://stackoverflow.com/questions/15206224/querying-crystal-server-2011-cms-on-vs2012-and-win8-64bit)
**Creation Date:** 1362414451
**Score:** 0
**Tags:** c#, asp.net, vb.net, crystal-reports
## Question Body
<p>For whatever reason, there are many different SDKs listed on the SAP website. I've tried all of the ones that look appropriate, but no matter which I install, I end up missing the assemblies required for connecting to the Crystal Server CMS and accessing reports in that database.</p>

<p>What I'm trying to do specifically is rewrite an old VB ASP.NET application that queried our Crystal Server 11 CMS, which was hosted on a Windows Server 2003 machine. I've got Crystal Server 2011 installed on a Windows Server 2008 R2 machine now and am wanting to switch this over to C# and .NET 4.0, but am having trouble using the code in that environment due to the missing assemblies.</p>

<p>Here's the include list that was in the original file, so you can see what I'm looking for:</p>

<pre><code>Imports CrystalDecisions.Enterprise
Imports CrystalDecisions.ReportSource
Imports CrystalDecisions.Enterprise.Viewing
Imports CrystalDecisions.Enterprise.Dest
Imports CrystalDecisions.Enterprise.Desktop
Imports CrystalDecisions.ReportAppServer.Controllers
Imports CrystalDecisions.ReportAppServer.ClientDoc
Imports CrystalDecisions.ReportAppServer
Imports CrystalDecisions.Web
Imports CrystalDecisions.Shared
Imports CrystalDecisions.CrystalReports.Engine
</code></pre>

<p>And this is the approach the original code used to fetch the report from the CMS:</p>

<pre><code>Dim mySessionMgr As SessionMgr = New SessionMgr
Dim myEnterpriseSession As EnterpriseSession = mySessionMgr.Logon("XX", "XX", 
      "XX", "secEnterprise")
Dim myEnterpriseService As EnterpriseService =
      myEnterpriseSession.GetService("InfoStore")
Dim myInfoStore As InfoStore = New InfoStore(myEnterpriseService)
myEnterpriseService = myEnterpriseSession.GetService("RASReportFactory")
Dim rrfObject As Object = myEnterpriseService.Interface
Dim myReportAppFactory As ReportAppFactory = CType(rrfObject, ReportAppFactory)
Dim queryString As String = "Select SI_ID From CI_INFOOBJECTS " _
      &amp; "Where SI_PROGID='CrystalEnterprise.Report' " _
      &amp; "And SI_NAME Like '" &amp; ReportID &amp; "'"

Dim myInfoObjects As InfoObjects = myInfoStore.Query(queryString)
Dim myInfoObject As InfoObject = myInfoObjects(1)
myReportClientDocument = New ReportClientDocumentClass
myReportClientDocument = myReportAppFactory.OpenDocument(myInfoObject.ID, 0)
</code></pre>

<p>I'm not sure if this approach is the best to use with the current versions of the software involved, or if there's a better way to achieve the same effect. If this approach is still correct, does anybody have suggestions on what SDK files I need to install in order to have access to these assemblies?</p>

## Answers
### Answer ID: 15274661
<p>The above code worked, but in order to get the references to resolve properly I had to first install the Crystal Reports 2011 for VS (13_0_5) and then install the Business Intelligence 14 SP04 for 32bit, in that order. The 64bit versions of either did not do the trick. Installing just one or the other also did not work, nor did installing them in the reverse order.</p>

