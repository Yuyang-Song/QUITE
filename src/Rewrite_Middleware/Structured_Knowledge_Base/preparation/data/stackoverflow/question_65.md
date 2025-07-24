# How to make multiple slightly different inserts fast from PHP
[Link to question](https://stackoverflow.com/questions/11604192/how-to-make-multiple-slightly-different-inserts-fast-from-php)
**Creation Date:** 1342993328
**Score:** 1
**Tags:** php, mysql
## Question Body
<p>I'm doing around 600 <code>INSERT ON DUPLICATE KEY UPDATE</code> queries where each insert can have a different set of columns.</p>

<p>The way i'm doing it now is just a foreach loop with a <code>mysql_query()</code>. It's really slow, the php script stops due to maximum execution time of 30s.</p>

<p>I cant use <code>INSERT INTO table (columns) VALUES (values 1), (values 2), ..., (values n)</code> because each insert must be able to have a different set of columns.</p>

<p>I also looked at prepared queries but from what i saw it seems like that won't work with different column sets either.</p>

<p>I'm quite a novice to databases and MYSQL. I'm just hacking together something as a weekend project, and right now i just want to get this last piece of the project to work. I'm sorry about not doing this the proper way. (sorry about using deprecated php mysql functions too.) Maybe i should go to bed and rewrite this later. What would be the proper way to do it?</p>

<p>EDIT: here is some info on the table type</p>

<pre>
-- phpMyAdmin SQL Dump
-- version 3.5.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jul 22, 2012 at 09:59 PM
-- Server version: 5.5.24-log
-- PHP Version: 5.3.13

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `trailerbay`
--

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE IF NOT EXISTS `movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `imdb` int(7) NOT NULL,
  `title` text COLLATE utf8_unicode_ci,
  `releasedate` date DEFAULT NULL,
  `enlistdate` datetime NOT NULL,
  `runtime` time DEFAULT NULL,
  `trailer` text COLLATE utf8_unicode_ci NOT NULL,
  `plot` text COLLATE utf8_unicode_ci,
  `cover` text COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `imdb` (`imdb`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=1145 ;
</pre>

## Answers
### Answer ID: 11604278
<p>Are your inserts being executed in a mysql transaction?  If not, this might help improve performance for you.</p>

<p><a href="http://kevin.vanzonneveld.net/techblog/article/improve_mysql_insert_performance/" rel="nofollow">http://kevin.vanzonneveld.net/techblog/article/improve_mysql_insert_performance/</a></p>

### Answer ID: 11604337
<p>I don't think you can have SO MANY columns in table, that their on/off combinations are prohibitively numerous.</p>

<p>So for each row you can extract its column combination (you can order the fields alphabetically, for example) and use its structure as a key:</p>

<pre><code>// $tuple has been sorted based on keys

$syndrome = implode(',', array_keys($tuple));

$values = array_values($tuple);    

if (isset($big_inserts[$syndrome]))
    array_push($big_inserts[$syndrome], $values);
else
    $big_inserts[$syndrome] = array($values);
</code></pre>

<p>At the end of the loop you will find yourself with a <code>$big_inserts</code> array with a certain number of keys. Each key will map an array of sets of values, suitable for a multiple insert.</p>

<p>Unless you're really, really unlucky, you'll have much fewer "multiple inserts" than the individual inserts you started with. If all inserts have the same columns, you will have only one key in big_inserts, holding all the tuples.</p>

<p>Now, cycle on big_inserts, and for every key you can prepare a statement. The array of values to be sent to PDO is the concatenation of all the tuples in <code>$big_inserts[$key]</code>. </p>

<pre><code>foreach($big_inserts as $fields =&gt; $lot)
{
    $SQL = "INSERT INTO table ($fields) VALUES ";
    // I need a (?.?.?---) tuple
    $tuple = '('.implode(',', array_fill(0, count($lot[0]), '?')).')';
    // How many tuples are in a lot?
    $SQL .= implode(',', array_fill(0, count($lot), $tuple));
    $values = array();
    foreach($lot as $set)
        $values = array_merge($values, $set);
    // Now $SQL has all the '?'s, and $values contains all the values.
    // Run the statement.
 }
</code></pre>

<p>If this is not enough, you might have to separate the statements in chunks, save them in session and execute each chunk sequentially, maybe using a separate table to simulate a "multi-roundtrip" transaction (in case connection gets lost / user closes browser / whatever with half the chunks already executed and the other half still to go. Use straight INSERTs into a table with the same structure, then when the table is ready run one single INSERT INTO ... SELECT FROM within a transaction and drop the ancillary table after commit.</p>

<p>If they were simple INSERTs I'd try disabling temporarily some indexes, but you rely on them for the ON DUPLICATE KEY UPDATE, so this is a no go.</p>

### Answer ID: 11604230
<p>Just split it up in 50 inserts at a time, divide it over 12 files and execute them in order. Simple javascript to redirect on completion to next one.</p>

<p>if its just a one time deal that may be the easiest solution.</p>

<p>otherwise post some example code so we can give some more helpfull answers.</p>

