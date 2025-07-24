# How to achieve the same result using Mysql Joins instead of nested subqueries?
[Link to question](https://stackoverflow.com/questions/38887737/how-to-achieve-the-same-result-using-mysql-joins-instead-of-nested-subqueries)
**Creation Date:** 1470892504
**Score:** 2
**Tags:** php, mysql, database, mysqli, phpmyadmin
## Question Body
<p>I've got some nested subquerys which turned out to be VERY slow and I'm struggling to rewrite the same code with Mysql Joins, I hope someone can help me.
I want to get the data from all the songs on the database except the ones on my playlist, and after that I only want the ones on my playlist.
Here you can see my querys</p>

<p>Thanks in advance.</p>

<h2>Querys</h2>

<pre><code>$sql1 = "Select distinct title, artist, album from songs where id not in(Select id from songs where id 
        IN(Select id from songs where title IN(Select title from songs where id 
        IN(Select song_id from playlist where playlist_id IN (Select playlist_id from playlists where name = '$playlist_name')))))";


$sql2 = "Select distinct title, artist, album from songs where id in(Select id from songs where id 
        IN(Select id from songs where title IN(Select title from songs where id 
        IN(Select song_id from playlist where playlist_id IN (Select playlist_id from playlists where name = '$playlist_name')))))";
</code></pre>

<h2>Database Design</h2>

<pre><code>SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;


CREATE TABLE IF NOT EXISTS playlist (
  playlist_id int(11) NOT NULL,
track_id int(11) NOT NULL,
  song_id int(11) NOT NULL,
  votes int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=1463 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS playlists (
playlist_id int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  created_at datetime NOT NULL,
  updated_at datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS songs (
id int(11) NOT NULL,
  path varchar(100) NOT NULL,
  artist varchar(60) NOT NULL,
  title varchar(60) NOT NULL,
  album varchar(50) NOT NULL,
  added_at datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=3759 DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS users (
userID int(11) NOT NULL,
  voices int(11) NOT NULL,
  pass varchar(18) NOT NULL,
  created_at datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


ALTER TABLE playlist
 ADD PRIMARY KEY (track_id), ADD KEY song_id (song_id), ADD KEY playlist_id (playlist_id);

ALTER TABLE playlists
 ADD PRIMARY KEY (playlist_id);

ALTER TABLE songs
 ADD PRIMARY KEY (id), ADD UNIQUE KEY title (title,artist,album);

ALTER TABLE users
 ADD PRIMARY KEY (userID);


ALTER TABLE playlist
MODIFY track_id int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=1463;
ALTER TABLE playlists
MODIFY playlist_id int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=14;
ALTER TABLE songs
MODIFY id int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3759;
ALTER TABLE users
MODIFY userID int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE playlist
ADD CONSTRAINT playlist_ibfk_1 FOREIGN KEY (song_id) REFERENCES songs (id) ON DELETE CASCADE,
ADD CONSTRAINT playlist_ibfk_2 FOREIGN KEY (playlist_id) REFERENCES playlists (playlist_id) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
</code></pre>

## Answers
### Answer ID: 38888675
<p>You can change your query as,</p>

<p>For all the songs on the database except the ones on your playlist</p>

<pre><code>$sql1 = "Select distinct title, artist, album 
from songs where id not in(Select distinct song.id
from songs song inner join playlist playlist 
on playlist.song_id=song.id
inner join playlists playlists 
on playlists.playlist_id=playlist.playlist_id
and playlists.name = '$playlist_name')";
</code></pre>

<p>The ones on your playlist,</p>

<pre><code>$sql2 = "Select distinct song.title, song.artist, song.album
from songs song inner join playlist playlist 
on playlist.song_id=song.id
inner join playlists playlists 
on playlists.playlist_id=playlist.playlist_id
and playlists.name = '$playlist_name'";
</code></pre>

