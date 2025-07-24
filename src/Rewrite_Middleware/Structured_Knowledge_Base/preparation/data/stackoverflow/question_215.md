# Windows Setup: Dynamic Registry Keys/Values
[Link to question](https://stackoverflow.com/questions/16901329/windows-setup-dynamic-registry-keys-values)
**Creation Date:** 1370276439
**Score:** 2
**Tags:** c#, visual-studio-2010, setup-project
## Question Body
<p><strong>A synopsis of my question:</strong></p>

<p>Is it possible to use your own, custom variables (the way that you can use [TARGETDIR]) in the Registry screen of a Windows Setup project in VS2010? Specifically, I need to store my assembly's strong name and assembly version in the registry, in order to register a COM object on a machine without the installing user having admin rights.</p>

<p>I already tried using a custom action, and I'd rather not continue down that road if possible.</p>

<p><strong>Here are the specifics, and what I've tried:</strong></p>

<p>Recently, my employer started blindly removing all employees' admin rights from their machines.</p>

<p>I had created a COM-exposed C# class that I'd been using on a few of my workstations, which is no longer able to be registered, because I no longer have the appropriate permissions under HKEY_CLASSES_ROOT.</p>

<p>Through Googling, I found out how to register all of the appropriate keys under HKCU*, but now I'd like to implement this in my deployment project.</p>

<p>I understand how to use the Registry screen within Windows Setup, but there are custom keys/values that need to be stored (install folder, assembly strong name, version).</p>

<p>I could use a custom action, but ideally, I want Windows Setup to manage my registry settings, because (a) it's better than I am at automatically removing all the proper keys/values upon uninstall, (b) during the install, registry changes are transactional &amp; rolled back upon install error, and (c) the logic for registry key install/removal/transactions is already written by Microsoft, and I won't have to rewrite it myself.</p>

<p>The project was in VS2008 until today, but I just upgraded it to VS2010, so perhaps something has changed between 2008 and 2010 that might allow this behavior.</p>

<p>So, rather than using a custom action, is there a better way to do this?</p>

<p><strong>EDIT:</strong> I found <a href="https://stackoverflow.com/a/1801639/864414">this</a> answer, which seems to suggest that you can access the Windows Install "Registry" table within your install project. I'm not sure how to do access it, though. In the past, I seem to recall that you could access the MSI databases from a special external tool (Orca), but I don't know if you can access these tables in your setup project.</p>

<p><strong>EDIT 2:</strong> Ah, I may be on to something; perhaps a post-build event:</p>

<ul>
<li><a href="https://stackoverflow.com/questions/886842/use-orca-to-edit-msi-from-command-line">Use Orca to edit msi from command line?</a>, </li>
<li><a href="http://msdn.microsoft.com/en-us/library/aa368562.aspx" rel="nofollow noreferrer">Examples of Database Queries Using SQL and Script</a>, </li>
<li><a href="http://source.db4o.com/db4o/trunk/enterprise/omn/BuildScripts/WiRunSQL.vbs" rel="nofollow noreferrer">WiRunSQL.vbs</a></li>
</ul>

<hr>

<p>* Run RegAsm twice - once with /codebase and once without; both times with the /regfile option. Then merge both files together (removing duplicates), and replace all HKCR references with HKCU\Software\Classes.</p>

## Answers
### Answer ID: 16928518
<p>Yes, this can be done*.</p>

<p>First, create a Console executable that will be run as part of a post-build event of the Windows Setup project. This modifies the <code>Registry</code> table in the MSI file that has been built by VS2010.</p>

<p>Note: You must add a reference to "Microsoft Windows Installer Object Library" under COM, for the below code to compile.</p>

<pre><code>using System;
using WindowsInstaller;
using System.Runtime.InteropServices;
using System.Reflection;

namespace Post_Setup_Scripting
{
    class Program
    {

        static void Main(string[] args)
        {
            if (args.Length != 2)
            {
                Console.WriteLine("Incorrect args.");
                return;
            }

            //arg 1 - path to MSI
            string PathToMSI = args[0];
            //arg 2 - path to assembly
            string PathToAssembly = args[1];

            Type InstallerType;
            WindowsInstaller.Installer Installer;
            InstallerType = Type.GetTypeFromProgID("WindowsInstaller.Installer");
            Installer = (WindowsInstaller.Installer)Activator.CreateInstance(InstallerType);

            Assembly Assembly = Assembly.LoadFrom(PathToAssembly);
            string AssemblyStrongName = Assembly.GetName().FullName;
            string AssemblyVersion = Assembly.GetName().Version.ToString();

            string SQL = "SELECT `Key`, `Name`, `Value` FROM `Registry`";
            WindowsInstaller.Database Db = Installer.OpenDatabase(PathToMSI, WindowsInstaller.MsiOpenDatabaseMode.msiOpenDatabaseModeDirect);
            WindowsInstaller.View View = Db.OpenView(SQL);
            View.Execute();
            WindowsInstaller.Record Rec = View.Fetch();
            while (Rec != null)
            {
                for (int c = 0; c &lt;= Rec.FieldCount; c++)
                {
                    string Column = Rec.get_StringData(c);
                    Column = Column.Replace("[AssemblyVersion]", AssemblyVersion);
                    Column = Column.Replace("[AssemblyStrongName]", AssemblyStrongName);
                    Rec.set_StringData(c, Column);
                    View.Modify(MsiViewModify.msiViewModifyReplace, Rec);
                    Console.Write("{0}\t", Column);
                    Db.Commit();
                }
                Console.WriteLine();
                Rec = View.Fetch();
            }
            View.Close();

            GC.Collect();
            Marshal.FinalReleaseComObject(Installer);

            Console.ReadLine();
        }
    }
}
</code></pre>

<p>The "variables" that we are going to use in the Windows Setup Registry screen get replaced in these lines of the above code; this could be adapted to any items that are necessary.</p>

<pre><code>string Column = Rec.get_StringData(c);
Column = Column.Replace("[AssemblyVersion]", AssemblyVersion);
Column = Column.Replace("[AssemblyStrongName]", AssemblyStrongName);
</code></pre>

<p>Second, create a .reg file that contains the registry keys you want to create upon install. In the code above, we modify the MSI database in the post-build by replacing all instances of [AssemblyVersion] with the assembly version, and [AssemblyStrongName] with the assembly's strong name.</p>

<pre><code>[HKEY_CURRENT_USER\Software\Classes\Record\{XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX}\[AssemblyVersion]]
"Class"="MyClass.MyClass"
"Assembly"="[AssemblyStrongName]"
"RuntimeVersion"="v2.0.50727"
"CodeBase"="[TARGETDIR]MyClass.dll"
</code></pre>

<p>Third, import the .reg file into the Windows Setup registry screen in VS2010 by right-clicking "Registry On Target Machine", and clicking "Import".</p>

<p>Finally, call the post-build executable in the "PostBuildEvent" property of the setup project:</p>

<pre><code>"C:\Path\To\Exe\Post-Setup Scripting.exe" [Path to MSI] [Path To DLL to extract strong name/version]
</code></pre>

<hr>

<p>* This is a little different than using [TARGETDIR], because [TARGETDIR] gets resolved at install time, and these "variables" will get resolved at build time. For my solution, I needed to resolve at build time, because my version number increments with each build.</p>

