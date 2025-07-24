# Ordering without JOIN from Second Table
[Link to question](https://stackoverflow.com/questions/16695869/ordering-without-join-from-second-table)
**Creation Date:** 1369236716
**Score:** 1
**Tags:** mysql
## Question Body
<p>I have a unique situation.  I have a function that generates SQl on the fly and runs it against the mySQL database.  It builds the SQL query step by ste and is highly complex. </p>

<p>It can have up to 40 different ANDs in the WHERE clause.  For example.</p>

<pre><code>SELECT * FROM TableX   //yea I know  don't search for * ...  trying to save typing on stack.
WHERE  Size = 'Large'
AND color= 'blue'
AND smell = 'stinky'
AND ugly = 'no'
AND brand = 'United'
etc...
</code></pre>

<p>At the End it puts out a line of ORDER BY.  Such as:</p>

<pre><code>ORDER BY brand
</code></pre>

<p>My challenge is that I can only ORDER using the ORDER BY <em>some string</em>.   This works just fine if I want to order the data from the primary table.  But what can I do if it comes out of a related table?</p>

<p>Say I have the following schema:</p>

<pre><code>CREATE  TABLE `Trucks` (
  `ID` INT NOT NULL AUTO_INCREMENT ,
  `Make` VARCHAR(45) NULL ,
  `Current_PartList_ID` INT NULL ,
  PRIMARY KEY (`ID`) );

INSERT INTO `Trucks` (`Make`, `Current_PartList_ID`) VALUES ('Volvo', '1');
INSERT INTO `Trucks` (`Make`, `Current_PartList_ID`) VALUES ('Volvo', '2');
INSERT INTO `Trucks` (`Make`, `Current_PartList_ID`) VALUES ('Mac', '3');
INSERT INTO `Trucks` (`Make`, `Current_PartList_ID`) VALUES ('Mac', '5');
INSERT INTO `Trucks` (`Make`, `Current_PartList_ID`) VALUES ('Daihatsu', '8');
INSERT INTO `Trucks` (`Make`, `Current_PartList_ID`) VALUES ('Volvo', '4');


CREATE  TABLE `Parts_lists` (
  `ID` INT NOT NULL AUTO_INCREMENT ,
  `Carb_Model` VARCHAR(45) NULL ,
  `Carb_date` DATE NULL ,
  `Tire_type` VARCHAR(45) NULL ,
  `Tire_date` DATE NULL ,
  PRIMARY KEY (`ID`) );

INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Hirsch', '2012-12-19', 'Toyo', '2013-01-01');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('HIrsch', '2013-02-14', 'Goodyear', '2011-03-16');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Bosch', '2011-11-04', 'Toyo', '2013-01-01');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Miller', '2009-10-11', 'Toyo', '2010-04-17');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Bosch', '2011-01-07', 'Goodyear', '2013-01-06');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Bosch', '2012-09-16', 'Lamb', '2012-06-25');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Miller', '2011-07-22', 'Unknown', '2012-04-07');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Davis', '2009-03-09', 'Hawking', '2012-06-16');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Sanno', '2010-01-07', 'Goodyear', '2009-07-16');
INSERT INTO `Parts_lists` (`Carb_Model`, `Carb_date`, `Tire_type`, `Tire_date`) VALUES ('Thrust', '2012-11-11', 'Lamb', '2004-04-08');
</code></pre>

<p>I would Like to get:</p>

<p>SELECT * FROM Trucks WHERE Make = 'volvo' ORDER BY (*Parts_List.Carb_date*)</p>

<p>Thus giving me the following selection</p>

<pre><code>ID    Make      (why)
6     Volvo     (Because the Carb_date is 2009-10-11)
1     Volvo     (Because the Carb_date is 2012-12-19)
2     Volvo     (Because the Carb_date is 2013-02-14)
</code></pre>

<p>To be very clear:  Im stuck with: The following text (I cant edit it at all: without a total rewrite of an archaic ugly app ):</p>

<pre><code>SELECT * FROM Trucks WHERE Make = 'volvo' ORDER BY
</code></pre>

<p>I need a string for XXXXXXX</p>

<pre><code>SELECT * FROM Trucks WHERE Make = 'volvo' ORDER BY   XXXXXXX
</code></pre>

## Answers
### Answer ID: 16697748
<p>This should work as your <code>ORDER BY</code> string:</p>

<p><code>(SELECT Carb_date FROM Parts_lists WHERE ID = Trucks.Current_PartList_ID)</code></p>

