# Upgrading project to Visual Studio 2015 causes errors with Enums
[Link to question](https://stackoverflow.com/questions/34723793/upgrading-project-to-visual-studio-2015-causes-errors-with-enums)
**Creation Date:** 1452522150
**Score:** 1
**Tags:** vb.net, enums, visual-studio-2015
## Question Body
<p>I have a VB.NET project targeting framework 3.5 that references a dynamic DLL of compiled enums generated from a database. My project compiles and runs in Visual Studio 2012. I am beginning to upgrade my solutions to Visual Studio 2015 and ran in to a bunch of errors when I tried doing this project. </p>

<p>The two errors I get for just about every enum are</p>

<ul>
<li>Operator '=' is not defined for types MyEnumType and MyEnumType</li>
<li>Field MyEnumType.Field has an invalid constant value</li>
</ul>

<p>Viewing the definition of the enum meta data (which I can do in 2015 but not 2012) I see it being defined as </p>

<pre><code>    Enum EnumName as Object
      Field1
      Field2
    End Enum
</code></pre>

<p>As you can see its appending As Object which I've never seen before. But that explains the operator = error because if it's an object than you would have to define an overloaded Equals operator.</p>

<p>I'm just seeing if anyone has any insight or know of anything in 2015 that would be causing this issue. I tried creating a new project an importing the .DLLs just to see if they worked at all in VS 2015. They work when referenced in C# but not in VB.NET. The .DLLs were written and compiled in VB.NET. S</p>

<p>For the time being I can still use 2012, but would like to upgrade to 2015 in the future and not have to rewrite a bunch of things.</p>

<p>EDIT:</p>

<p>Here is the (simplified) code that is being used to create the enum .DLL. An xml is being read with the Enum name and sql query used to generate the enum.</p>

<pre><code>Dim myEnumBuilder As Emit.EnumBuilder
Dim myAppDomain as AppDomain
Dim myModuleBuilder As ModuleBuilder

Dim myAssemblyName As New AssemblyName()
myAssemblyName.Name = EnumDll.Name

' Create a dynamic assembly.
myAssemblyBuilder = myAppDomain.DefineDynamicAssembly(myAssemblyName, AssemblyBuilderAccess.Save, msOutputDirectoryPath)

' Create a dynamic module.
myModuleBuilder = myAssemblyBuilder.DefineDynamicModule("Library." &amp; EnumDll.Name, EnumDll.Name &amp; ".dll")
 ' Creating a dynamic Enum.
myEnumBuilder = myModuleBuilder.DefineEnum(EnumDll.Name &amp; "." &amp; EnumName, TypeAttributes.Public, GetType(Int32))

 Dim myFieldBuilder As FieldBuilder = myEnumBuilder.DefineLiteral(StrEnum, CInt(oReader(0)))
 myEnumBuilder.CreateType()
 myAssemblyBuilder.Save(EnumDll.Name &amp; ".dll") 'save the dll
</code></pre>

