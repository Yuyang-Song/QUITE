# Hoping for easy filling of classes generated from an XSD, where the DataSet has a different schema
[Link to question](https://stackoverflow.com/questions/55836275/hoping-for-easy-filling-of-classes-generated-from-an-xsd-where-the-dataset-has)
**Creation Date:** 1556129777
**Score:** 0
**Tags:** c#, xml, xsd
## Question Body
<p>I have data in a database in one schema that I need to turn into XML of another schema. </p>

<p>The XML is a 3rd party proprietary message / response system. We have access to a help document that gives a breakdown of all the entities and complex types and we have XSD documents. There are potentially hundreds of different XML document request variations as the 2nd and 3rd level elements contain choice indicators ranging from 2- 200. </p>

<p>The current method that has been employed is a brute force approach - query to get all the data into a DataSet object then (using the help document) manually generate the XML by concatenating the data into a string. This approach works for the 2 or 3 variations that we needed. </p>

<p>Now that we want to support more variations we are wanting to move away from the brute force approach. We are also several versions behind, yet using the most supported version, and would like to approach a resolution with scalability in mind. </p>

<p><strong>What have we done?</strong> 
We generated the classes from the XSD document which gave us 2300 + partial classes. I started developing a library of filling methods for each class object that uses a coordinate object (table, column, row properties) to the specific data in the DataSet. But realizing, that we would need to go over the data to fill the coordinate objects, the question arises 
 - Why not just fill the actual xml object at that time? </p>

<p>It would be less of an issue if each of the dataset tables were able to be mapped to a single XML object however the data for a single object is likely spread over multiple tables.</p>

<pre><code>Idea 1
</code></pre>

<p>Lately, I have been thinking of a more Factory / Builder combination to create / fill the xml objects. </p>

<pre><code>Idea 2
</code></pre>

<p>Another idea I had was to incorporate a property attribute system that has the tablename, columnname - this runs into an issue when the same xml object gets an identical property from 2 different locations in the DataSet based on 2nd or 3rd level element choice. Could always add another designator (choice type?) and then have multiple attributes on a property.</p>

<pre><code>Idea 3
</code></pre>

<p>Another consideration is rewriting the stored procedure to retrieve the data in correct tables-to-objects, the issue that I have with this is moving logic from code to SQL. It really just puts the problem in a different area of the application.</p>

<p>Third party solutions are not entirely out of the question. I am looking for suggestions of how to approach this problem. </p>

<p>UPDATE:
The XML that is generated is written to a file and then consumed by a 3rd party application. </p>

## Answers
### Answer ID: 56135075
<p>We decided on a combination of Idea 1 and Idea 2.<br>
The XSD generated classes number 2300 +, which will be used to generate a filled root object that we can pass to XmlSerializer class. It will generate the xml we need to pass to the 3rd party tool. </p>

<p>The xml root and top 2 levels of class objects are going to be generated with the Builder and Factory Design patterns. We will be using copies of the generated partial classes to add functionality, through interfaces or base classes.  </p>

<pre><code>[System.CodeDom.Compiler.GeneratedCodeAttribute("xsd", "4.6.1055.0")]
[System.SerializableAttribute()]
[System.Diagnostics.DebuggerStepThroughAttribute()]
[System.ComponentModel.DesignerCategoryAttribute("code")]
[System.Xml.Serialization.XmlTypeAttribute(Namespace = "http://temp")]
[System.Xml.Serialization.XmlRootAttribute("NumberType", Namespace = "http://temp", IsNullable = false)]    
public partial class IdGroup
{

    private string idField;

    private string valueField;

    /// &lt;remarks/&gt;
    [System.Xml.Serialization.XmlAttributeAttribute()]
    public string id
    {
        get
        {
            return this.idField;
        }
        set
        {
            this.idField = value;
        }
    }

    /// &lt;remarks/&gt;
    [System.Xml.Serialization.XmlTextAttribute()]
    [CustomPropertyAttribute("TableName", "ColumnName", Level2Type)]
    [CustomPropertyAttribute("AltTableName", "AltColumnName", AltLevel2Type)]
    public string Value
    {
        get
        {
            return this.valueField;
        }
        set
        {
            this.valueField = value;
        }
    }
}

public partial class IdGroup : IExtendFunctionality
{ }
</code></pre>

<p>I realized that this question is rather open to interpretation and so was probably not a very good question. I apologize for this.</p>

<p>Thanks for everyone who stopped by to take look. </p>

