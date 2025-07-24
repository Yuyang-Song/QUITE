# optimize slow sql query with 23 tables
[Link to question](https://stackoverflow.com/questions/38726307/optimize-slow-sql-query-with-23-tables)
**Creation Date:** 1470156655
**Score:** 0
**Tags:** mysql, performance, xampp, mariadb
## Question Body
<p>I triedy to optimize my SQL Query and my SQL-Server (mariaDB 10.1.10 from xampp 5.6.19) for three days but I have to wait for the server response for more than a minute. Sometimes I'll get no answer!</p>

<p>There are two queries, I've a problem with. Today I rewrite the first query from SQL-87-Syntax to SQL-92-Syntax, but there was no speedup. I've read that before.
I read also, that indexes could speedup my query dramatically but all my joins are on keys. Not sure if I could optimize anything at my current database although?</p>

<p>Here is my first query:</p>

<pre><code>SELECT rv.id AS rahmenID, vls.id AS vlsID, vls.leistungsempfanger AS leistungsempfanger, vls.objektbezeichnung AS objektbezeichnung, 
                                        str.bezeichnung AS strName, adr.hausnummer AS hausnummer, plz.bezeichnung AS plz, ort.bezeichnung AS ort, land.bezeichnung AS land,
                                        produkt.bezeichnung AS produkt, vls.vorjahresverbrauch AS vorjahresverbrauch, vls.lieferbeginn AS lieferbeginn, vls.lieferende AS lieferende,
                                        vls.kundennummer_evu AS vertragskonto, anetz.bezeichnung AS ausspeisenetz, mgebiet.bezeichnung AS marktgebiet, qualitat.bezeichnung AS qualitat,
                                        lastprofil.bezeichnung AS lastprofil, unVor.name AS vorlieferant, vls.vorlieferant_kundennummer AS vorlieferantKdNr, vls.zahlernummer AS zahlernummer,
                                        ls.zahlpunkt AS zahlpunkt, vls.jahreshochstleistung AS jahreshochstleistung, vls.stichtag_abrechnung AS abrechnungsdatum,
                                        kennzeichen.bezeichnung AS vertragskennzeichen, kalkArt.bezeichnung AS kalkulationsart, maKalk.vorname AS kalkVorname, maKalk.nachname AS kalkNachname,
                                        vls.kalkulationsdatum AS kalkDatum, pb.jahr AS pbJahr, pb.kalenderwoche AS pbKW, maDist.vorname AS distVorname, maDist.nachname AS distNachname,
                                        pbt.nne_mess_ka AS nneMessKa, pbt.regelenergie AS regelenergie, pbt.energiesteuer AS energiesteuer, pbt.erdgaspreis AS erdgaspreis,
                                        pbt.rohmarge AS rohmarge, pbt.marge_pulsar AS marge_pulsar, pbt.arbeitspreis AS arbeitspreis, pbt.nv_arbeitspreis AS nv_arbeitspreis,
                                        pbt.nv_grundpreis AS nv_grundpreis, vStatus.bezeichnung AS vertragsstatus
                                FROM vertrag__rahmen rv 
                                    INNER JOIN vertrag__lieferstelle__gas vls                       ON rv.id                            = vls.rahmenID 
                                    INNER JOIN lieferstelle__gas ls                                 ON vls.lieferstelle_gasID           = ls.id
                                    INNER JOIN address adr                                          ON ls.addressID                     = adr.id
                                    INNER JOIN address__strasse str                                 ON adr.strasse                      = str.id
                                    INNER JOIN address__plz plz                                     ON adr.postleitzahl                 = plz.id
                                    INNER JOIN address__ort ort                                     ON adr.ort                          = ort.id
                                    INNER JOIN address__land land                                   ON adr.land                         = land.id
                                    INNER JOIN attribut__produkt produkt                            ON rv.produktID                     = produkt.id
                                    INNER JOIN attribut__gas__ausspeisenetz anetz                   ON ls.ausspeisenetzID               = anetz.id
                                    INNER JOIN attribut__gas__marktgebiet mgebiet                   ON ls.marktgebietID                 = mgebiet.id
                                    INNER JOIN attribut__gas__qualitat qualitat                     ON ls.qualitatID                    = qualitat.id
                                    INNER JOIN attribut__gas__lastprofil lastprofil                 ON ls.lastprofilID                  = lastprofil.id
                                    INNER JOIN unternehmen__evu evuVor                              ON vls.vorlieferant                 = evuVor.id
                                    INNER JOIN unternehmen unVor                                    ON evuVor.unternehmenID             = unVor.id
                                    INNER JOIN attribut__vertrag__kennzeichen kennzeichen           ON vls.vertrag_kennzeichenID        = kennzeichen.id
                                    INNER JOIN attribut__vertrag__kalkulationsart kalkArt           ON vls.vertrag_kalkulationsartID    = kalkArt.id
                                    INNER JOIN mitarbeiter maKalk                                   ON vls.kalkulator                   = maKalk.id
                                    INNER JOIN preisblatt__gas pb                                   ON vls.preisblattID                 = pb.id
                                    INNER JOIN mitarbeiter maDist                                   ON vls.distributor                  = maDist.id
                                    INNER JOIN vertrag__lieferstelle__gas__preisbestandteile pbt    ON vls.id                           = pbt.vlsGasID

                                    INNER JOIN vertrag__lieferstelle__gas__status vlsStatus         ON vls.id                           = vlsStatus.vlsGasID
                                    INNER JOIN attribut__vertrag__status vStatus                    ON vlsStatus.statusID               = vStatus.id


                                WHERE rv.id=11925 AND vlsStatus.id = (SELECT max(tmp.id) FROM vertrag__lieferstelle__gas__status tmp WHERE tmp.vlsGasID=vls.id)
                                ORDER BY vls.lieferstelle_gasID, vls.lieferbeginn
</code></pre>

<p>If it would be possible, I would give you the EXPLAIN of this query but I'll get no answer from my database! :(</p>

<p>My database:</p>

<pre><code>-- phpMyAdmin SQL Dump
-- version 4.6.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 02. Aug 2016 um 18:38
-- Server-Version: 10.1.10-MariaDB-log
-- PHP-Version: 5.6.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;



CREATE TABLE `address` (
  `id` int(11) NOT NULL,
  `strasse` int(11) NOT NULL,
  `hausnummer` varchar(10) NOT NULL,
  `postleitzahl` int(11) NOT NULL,
  `ort` int(11) NOT NULL,
  `land` int(11) NOT NULL,
  `angelegt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `angelegt_durch` int(11) NOT NULL,
  `aktualisiert` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `aktualisiert_durch` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `address__ort` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `address__plz` (
  `id` int(11) NOT NULL,
  `bezeichnung` char(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------


CREATE TABLE `address__strasse` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `attribut__gas__ausspeisenetz` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(250) NOT NULL,
  `beschreibung` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `attribut__gas__lastprofil` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(6) NOT NULL,
  `beschreibung` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `attribut__gas__marktgebiet` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(20) NOT NULL,
  `beschreibung` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `attribut__gas__qualitat` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(50) NOT NULL,
  `beschreibung` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `attribut__produkt` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(50) NOT NULL,
  `beschreibung` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `attribut__vertrag__kalkulationsart` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(250) NOT NULL,
  `beschreibung` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `attribut__vertrag__kennzeichen` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(30) NOT NULL,
  `beschreibung` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `attribut__vertrag__status` (
  `id` int(11) NOT NULL,
  `bezeichnung` varchar(250) NOT NULL,
  `beschreibung` varchar(500) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `lieferstelle__gas` (
  `id` int(11) NOT NULL,
  `addressID` int(11) NOT NULL,
  `ausspeisenetzID` int(11) NOT NULL,
  `marktgebietID` int(11) NOT NULL,
  `lastprofilID` int(11) NOT NULL,
  `qualitatID` int(11) NOT NULL,
  `zahlpunkt` varchar(33) DEFAULT NULL,
  `angelegt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `angelegt_durch` int(11) NOT NULL,
  `aktualisiert` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `aktualisiert_durch` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `mitarbeiter` (
  `id` int(11) NOT NULL,
  `geschlecht` varchar(1) DEFAULT NULL,
  `titel` int(11) DEFAULT NULL,
  `vorname` varchar(50) DEFAULT NULL,
  `nachname` varchar(50) DEFAULT NULL,
  `geburtsname` varchar(50) DEFAULT NULL,
  `anmerkung` varchar(500) DEFAULT NULL,
  `geburtsdatum` date DEFAULT NULL,
  `mitarbeiterNr` varchar(20) DEFAULT NULL,
  `foto_dateityp` varchar(150) DEFAULT NULL,
  `foto_size` int(11) DEFAULT NULL,
  `foto_width` int(6) DEFAULT NULL,
  `foto_height` int(6) DEFAULT NULL,
  `anzeigen` tinyint(1) NOT NULL DEFAULT '1',
  `angelegt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `angelegt_durch` int(11) NOT NULL,
  `aktualisiert` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `aktualisiert_durch` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `preisblatt__gas` (
  `id` int(11) NOT NULL,
  `evuID` int(11) NOT NULL COMMENT 'Lieferant',
  `marktgebietID` int(11) NOT NULL COMMENT 'Marktgebiet',
  `erdgasqualitatID` int(11) NOT NULL COMMENT 'Erdgasqualität',
  `kalenderwoche` int(2) NOT NULL,
  `jahr` int(4) NOT NULL,
  `gultig_von` date NOT NULL,
  `gultig_bis` date NOT NULL,
  `angelegt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `angelegt_durch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `unternehmen` (
  `id` int(11) NOT NULL,
  `unternehmenNr` varchar(10) DEFAULT NULL,
  `name` varchar(250) NOT NULL,
  `kurzel` varchar(5) DEFAULT NULL,
  `strasse` int(11) NOT NULL,
  `hausnummer` varchar(5) NOT NULL,
  `postleitzahl` int(11) NOT NULL,
  `ort` int(11) NOT NULL,
  `bundesland` int(11) DEFAULT NULL,
  `land` int(11) NOT NULL,
  `postfach` varchar(10) DEFAULT NULL,
  `postfach_postleitzahl` int(11) DEFAULT NULL,
  `postfach_ort` int(11) DEFAULT NULL,
  `postfach_land` int(11) DEFAULT NULL,
  `url` varchar(150) DEFAULT NULL,
  `bemerkung` varchar(500) DEFAULT NULL,
  `foto_dateityp` varchar(150) DEFAULT NULL,
  `foto_size` int(11) DEFAULT NULL,
  `foto_width` int(6) DEFAULT NULL,
  `foto_height` int(6) DEFAULT NULL,
  `angelegt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `angelegt_durch` int(11) NOT NULL,
  `aktualisiert` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `aktualisiert_durch` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `unternehmen__evu` (
  `id` int(11) NOT NULL,
  `unternehmenID` int(11) NOT NULL,
  `jahresumsatz` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `vertrag__lieferstelle__gas` (
  `id` int(11) NOT NULL,
  `rahmenID` int(11) NOT NULL,
  `maklerID` int(11) NOT NULL,
  `lieferstelle_gasID` int(11) NOT NULL,
  `leistungsempfanger` varchar(250) DEFAULT NULL,
  `objektbezeichnung` varchar(10) DEFAULT NULL,
  `lieferbeginn` date NOT NULL,
  `lieferende` date NOT NULL,
  `kundennummer_evu` varchar(20) DEFAULT NULL,
  `vorlieferant` int(11) NOT NULL,
  `vorlieferant_kundennummer` varchar(30) DEFAULT NULL,
  `zahlernummer` varchar(20) NOT NULL COMMENT 'zum Vertragsabschluss',
  `vorjahresverbrauch` double NOT NULL COMMENT 'in kWh',
  `jahreshochstleistung` double DEFAULT NULL,
  `preisblattID` int(11) NOT NULL,
  `stichtag_abrechnung` date NOT NULL,
  `vertrag_kennzeichenID` int(11) NOT NULL,
  `vertrag_kalkulationsartID` int(11) NOT NULL,
  `kalkulationsdatum` date NOT NULL,
  `kalkulator` int(11) NOT NULL COMMENT 'Excel-Berechner (mitarbeiterID)',
  `distributor` int(11) NOT NULL COMMENT 'Verkäufer Außendienst (mitarbeiterID)',
  `angelegt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `angelegt_durch` int(11) NOT NULL,
  `aktualisiert` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `aktualisiert_durch` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `vertrag__lieferstelle__gas__preisbestandteile` (
  `vlsGasID` int(11) NOT NULL,
  `nne_mess_ka` double DEFAULT NULL,
  `regelenergie` double DEFAULT NULL,
  `energiesteuer` double DEFAULT NULL,
  `erdgaspreis` double DEFAULT NULL,
  `rohmarge` double DEFAULT NULL,
  `marge_vp` double DEFAULT NULL,
  `arbeitspreis` double DEFAULT NULL,
  `nv_arbeitspreis` double DEFAULT NULL COMMENT 'Summe aus allen',
  `nv_grundpreis` double DEFAULT NULL,
  `temp` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `vertrag__lieferstelle__gas__status` (
  `id` int(11) NOT NULL,
  `vlsGasID` int(11) NOT NULL,
  `statusID` int(11) NOT NULL,
  `angelegt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `angelegt_durch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `vertrag__rahmen` (
  `id` int(11) NOT NULL,
  `vertragsnummer` varchar(30) NOT NULL,
  `evuID` int(11) NOT NULL,
  `verwalterID` int(11) NOT NULL,
  `maklerID` int(11) NOT NULL,
  `produktID` int(11) NOT NULL,
  `abschlussdatum` date NOT NULL,
  `bemerkung` varchar(500) NOT NULL,
  `angelegt` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `angelegt_durch` int(11) NOT NULL,
  `aktualisiert` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `aktualisiert_durch` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE `address`
  ADD PRIMARY KEY (`id`),
  ADD KEY `strasse` (`strasse`),
  ADD KEY `postleitzahl` (`postleitzahl`),
  ADD KEY `ort` (`ort`),
  ADD KEY `land` (`land`),
  ADD KEY `angelegt_durch` (`angelegt_durch`),
  ADD KEY `aktualisiert_durch` (`aktualisiert_durch`);


ALTER TABLE `address__ort`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bezeichnung` (`bezeichnung`);

ALTER TABLE `address__plz`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bezeichnung` (`bezeichnung`);


ALTER TABLE `address__strasse`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bezeichnung` (`bezeichnung`);

ALTER TABLE `attribut__gas__ausspeisenetz`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `attribut__gas__lastprofil`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `attribut__gas__marktgebiet`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `attribut__gas__qualitat`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `attribut__produkt`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `attribut__vertrag__kalkulationsart`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `attribut__vertrag__kennzeichen`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `attribut__vertrag__status`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `bezeichnung` (`bezeichnung`);

ALTER TABLE `lieferstelle__gas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lieferstelleID` (`addressID`),
  ADD KEY `ausspeisenetzID` (`ausspeisenetzID`),
  ADD KEY `marktgebietID` (`marktgebietID`),
  ADD KEY `zahlertypID` (`lastprofilID`),
  ADD KEY `qualitatID` (`qualitatID`),
  ADD KEY `angelegt_durch` (`angelegt_durch`),
  ADD KEY `aktualisiert_durch` (`aktualisiert_durch`);

ALTER TABLE `mitarbeiter`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mitarbeiterID` (`id`),
  ADD KEY `titel` (`titel`),
  ADD KEY `angelegt_durch` (`angelegt_durch`),
  ADD KEY `aktualisiert_durch` (`aktualisiert_durch`);
ALTER TABLE `mitarbeiter` ADD FULLTEXT KEY `vorname` (`vorname`);
ALTER TABLE `mitarbeiter` ADD FULLTEXT KEY `nachname` (`nachname`);
ALTER TABLE `mitarbeiter` ADD FULLTEXT KEY `vorname_2` (`vorname`,`nachname`);

ALTER TABLE `preisblatt__gas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `preisblattID` (`id`),
  ADD KEY `unternehmen_evuID` (`evuID`),
  ADD KEY `lieferstelle_marktgebietID` (`marktgebietID`),
  ADD KEY `lieferstelle_erdgasqualitatID` (`erdgasqualitatID`),
  ADD KEY `angelegt_durch` (`angelegt_durch`),
  ADD KEY `datum` (`jahr`,`kalenderwoche`) USING BTREE;


ALTER TABLE `unternehmen`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `kurzel` (`kurzel`),
  ADD UNIQUE KEY `unternehmenNr` (`unternehmenNr`),
  ADD KEY `angelegt_durch` (`angelegt_durch`),
  ADD KEY `aktualisiert_durch` (`aktualisiert_durch`),
  ADD KEY `strasse` (`strasse`),
  ADD KEY `postleitzahl` (`postleitzahl`),
  ADD KEY `ort` (`ort`),
  ADD KEY `bundesland` (`bundesland`),
  ADD KEY `land` (`land`),
  ADD KEY `postfach_postleitzahl` (`postfach_postleitzahl`),
  ADD KEY `postfach_ort` (`postfach_ort`),
  ADD KEY `postfach_land` (`postfach_land`);

ALTER TABLE `unternehmen__evu`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unternehmenID_2` (`unternehmenID`),
  ADD KEY `unternehmenID` (`unternehmenID`);

ALTER TABLE `vertrag__lieferstelle__gas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `vertrag_kennzeichenID` (`vertrag_kennzeichenID`),
  ADD KEY `lieferstelleID` (`lieferstelle_gasID`),
  ADD KEY `preisblattID` (`preisblattID`),
  ADD KEY `distributor` (`distributor`),
  ADD KEY `maklerID` (`maklerID`),
  ADD KEY `angelegt_durch` (`angelegt_durch`),
  ADD KEY `aktualisiert_durch` (`aktualisiert_durch`),
  ADD KEY `kalkulator` (`kalkulator`),
  ADD KEY `rahmenID` (`rahmenID`),
  ADD KEY `vorlieferant` (`vorlieferant`),
  ADD KEY `vertrag_berechnungsartID` (`vertrag_kalkulationsartID`),
  ADD KEY `lieferbeginn` (`lieferbeginn`),
  ADD KEY `lieferende` (`lieferende`),
  ADD KEY `anlage2index` (`id`,`rahmenID`,`lieferstelle_gasID`,`vorlieferant`,`preisblattID`,`vertrag_kennzeichenID`,`vertrag_kalkulationsartID`,`kalkulator`,`distributor`) USING BTREE;

ALTER TABLE `vertrag__lieferstelle__gas__preisbestandteile`
  ADD PRIMARY KEY (`vlsGasID`);

ALTER TABLE `vertrag__lieferstelle__gas__status`
  ADD PRIMARY KEY (`id`),
  ADD KEY `angelegt_durch` (`angelegt_durch`),
  ADD KEY `vlsGasID` (`vlsGasID`),
  ADD KEY `statusID` (`statusID`);


ALTER TABLE `vertrag__rahmen`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unternehmen_evuID_2` (`evuID`,`produktID`,`verwalterID`) USING BTREE,
  ADD KEY `unternehmen_evuID` (`evuID`),
  ADD KEY `unternehmen_verwalterID` (`verwalterID`),
  ADD KEY `unternehmen_maklerID` (`maklerID`),
  ADD KEY `produktID` (`produktID`),
  ADD KEY `angelegt_durch` (`angelegt_durch`),
  ADD KEY `aktualisiert_durch` (`aktualisiert_durch`);



ALTER TABLE `address`
  ADD CONSTRAINT `address_ibfk_05` FOREIGN KEY (`strasse`) REFERENCES `address__strasse` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `address_ibfk_06` FOREIGN KEY (`postleitzahl`) REFERENCES `address__plz` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `address_ibfk_07` FOREIGN KEY (`ort`) REFERENCES `address__ort` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `address_ibfk_08` FOREIGN KEY (`land`) REFERENCES `address__land` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `address_ibfk_09` FOREIGN KEY (`angelegt_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `address_ibfk_10` FOREIGN KEY (`aktualisiert_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE;


ALTER TABLE `lieferstelle__gas`
  ADD CONSTRAINT `lieferstelle_gas_ibfk_01` FOREIGN KEY (`addressID`) REFERENCES `address` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `lieferstelle_gas_ibfk_02` FOREIGN KEY (`ausspeisenetzID`) REFERENCES `attribut__gas__ausspeisenetz` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `lieferstelle_gas_ibfk_03` FOREIGN KEY (`marktgebietID`) REFERENCES `attribut__gas__marktgebiet` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `lieferstelle_gas_ibfk_04` FOREIGN KEY (`lastprofilID`) REFERENCES `attribut__gas__lastprofil` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `lieferstelle_gas_ibfk_05` FOREIGN KEY (`qualitatID`) REFERENCES `attribut__gas__qualitat` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `lieferstelle_gas_ibfk_06` FOREIGN KEY (`angelegt_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `lieferstelle_gas_ibfk_07` FOREIGN KEY (`aktualisiert_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE;


ALTER TABLE `mitarbeiter`
  ADD CONSTRAINT `mitarbeiter_ibfk_1` FOREIGN KEY (`titel`) REFERENCES `attribut__mitarbeiter__titel` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `mitarbeiter_ibfk_2` FOREIGN KEY (`angelegt_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `mitarbeiter_ibfk_3` FOREIGN KEY (`aktualisiert_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE;


ALTER TABLE `preisblatt__gas`
  ADD CONSTRAINT `preisblatt__gas_ibfk_1` FOREIGN KEY (`evuID`) REFERENCES `unternehmen__evu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `preisblatt__gas_ibfk_2` FOREIGN KEY (`marktgebietID`) REFERENCES `attribut__gas__marktgebiet` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `preisblatt__gas_ibfk_3` FOREIGN KEY (`erdgasqualitatID`) REFERENCES `attribut__gas__qualitat` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `preisblatt__gas_ibfk_4` FOREIGN KEY (`angelegt_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE;


ALTER TABLE `unternehmen`
  ADD CONSTRAINT `unternehmen_ibfk_1` FOREIGN KEY (`angelegt_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_10` FOREIGN KEY (`postfach_land`) REFERENCES `address__land` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_2` FOREIGN KEY (`aktualisiert_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_3` FOREIGN KEY (`strasse`) REFERENCES `address__strasse` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_4` FOREIGN KEY (`postleitzahl`) REFERENCES `address__plz` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_5` FOREIGN KEY (`ort`) REFERENCES `address__ort` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_6` FOREIGN KEY (`bundesland`) REFERENCES `address__bundesland` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_7` FOREIGN KEY (`land`) REFERENCES `address__land` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_8` FOREIGN KEY (`postfach_postleitzahl`) REFERENCES `address__plz` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `unternehmen_ibfk_9` FOREIGN KEY (`postfach_ort`) REFERENCES `address__ort` (`id`) ON UPDATE CASCADE;

ALTER TABLE `unternehmen__evu`
  ADD CONSTRAINT `unternehmen__evu_ibfk_1` FOREIGN KEY (`unternehmenID`) REFERENCES `unternehmen` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `vertrag__lieferstelle__gas`
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_01` FOREIGN KEY (`rahmenID`) REFERENCES `vertrag__rahmen` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_02` FOREIGN KEY (`maklerID`) REFERENCES `unternehmen__makler` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_03` FOREIGN KEY (`lieferstelle_gasID`) REFERENCES `lieferstelle__gas` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_04` FOREIGN KEY (`preisblattID`) REFERENCES `preisblatt__gas` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_06` FOREIGN KEY (`vertrag_kennzeichenID`) REFERENCES `attribut__vertrag__kennzeichen` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_07` FOREIGN KEY (`vertrag_kalkulationsartID`) REFERENCES `attribut__vertrag__kalkulationsart` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_08` FOREIGN KEY (`kalkulator`) REFERENCES `mitarbeiter` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_09` FOREIGN KEY (`distributor`) REFERENCES `mitarbeiter` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_10` FOREIGN KEY (`angelegt_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_11` FOREIGN KEY (`aktualisiert_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__lieferstelle__gas_ibfk_12` FOREIGN KEY (`vorlieferant`) REFERENCES `unternehmen__evu` (`id`) ON UPDATE CASCADE;


ALTER TABLE `vertrag__lieferstelle__gas__preisbestandteile`
  ADD CONSTRAINT `vlsGas_pb2_ibfk_01` FOREIGN KEY (`vlsGasID`) REFERENCES `vertrag__lieferstelle__gas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;


ALTER TABLE `vertrag__lieferstelle__gas__status`
  ADD CONSTRAINT `vlsGasStatus_ibfk_01` FOREIGN KEY (`vlsGasID`) REFERENCES `vertrag__lieferstelle__gas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `vlsGasStatus_ibfk_02` FOREIGN KEY (`statusID`) REFERENCES `attribut__vertrag__status` (`id`) ON UPDATE CASCADE;


ALTER TABLE `vertrag__rahmen`
  ADD CONSTRAINT `vertrag__rahmen_ibfk_01` FOREIGN KEY (`evuID`) REFERENCES `unternehmen__evu` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__rahmen_ibfk_02` FOREIGN KEY (`verwalterID`) REFERENCES `unternehmen__verwalter` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__rahmen_ibfk_03` FOREIGN KEY (`maklerID`) REFERENCES `unternehmen__makler` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__rahmen_ibfk_04` FOREIGN KEY (`produktID`) REFERENCES `attribut__produkt` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__rahmen_ibfk_05` FOREIGN KEY (`angelegt_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `vertrag__rahmen_ibfk_06` FOREIGN KEY (`aktualisiert_durch`) REFERENCES `db__user` (`id`) ON UPDATE CASCADE;
</code></pre>

<p>my my.ini:</p>

<pre><code>[mysqld]
port= 3306
socket = "C:/xampp/mysql/mysql.sock"
basedir = "C:/xampp/mysql" 
tmpdir = "C:/xampp/tmp" 
datadir = "C:/xampp/mysql/data"
pid_file = "mysql.pid"
# enable-named-pipe
key_buffer = 16M
max_allowed_packet = 1M
sort_buffer_size = 512K
net_buffer_length = 8K
read_buffer_size = 256K
read_rnd_buffer_size = 512K
myisam_sort_buffer_size = 8M
log_error = "mysql_error.log"

slow_query_log=ON
long_query_time=1
table_open_cache=10000
thread_cache_size=25
query_cache_type=ON
query_cache_size=128MiB
query_cache_limit=100MiB
tmp_table_size=64MiB
</code></pre>

<p>Thank you for your help!</p>

<p>edit: I recognized, that the query starts to be slow from " INNER JOIN vertrag__lieferstelle__gas__preisbestandteile pbt ..." and the other joins after it.</p>

## Answers
### Answer ID: 38728115
<p>How much RAM do you have?  Since I don't see <code>innodb_buffer_pool_size</code> in your <code>my.ini</code>, I suspect you are using some low default.  Set it to about 70% of <em>available</em> RAM.  This should help this query and others.</p>

<pre><code>table_open_cache=10000 -- lower to 3000
query_cache_size=128MiB -- lower to 50M
tmp_table_size=64MiB -- not more than 1% of RAM
</code></pre>

<p>Other notes:</p>

<ul>
<li><code>jahr</code> int(4) NOT NULL, -- Why not use the <code>YEAR</code> datatype?</li>
<li><code>INT(2)</code> -- the <code>(2)</code> says nothing; perhaps you meant <code>TINYINT</code>?</li>
<li><code>char(5)</code> -- you probably want <code>CHAR(5) CHARACTER SET ascii</code>, otherwise, you are allocating 15 bytes because of <code>utf8</code>.</li>
</ul>

<p>Because of the large number of normalization tables, this <em>may</em> help:</p>

<pre><code>SET @@optimizer_search_depth=1
</code></pre>

<p>You can <em>probably</em> test its utility by trying the <code>EXPLAIN SELECT ...</code> with it 1 versus its default of 62.</p>

### Answer ID: 38726438
<p>Not sure how much of a difference it will make with a 23 table query, but I generally try to avoid correlated subqueries like the one used here:</p>

<p><code>vlsStatus.id = (SELECT max(tmp.id) FROM vertrag__lieferstelle__gas__status tmp WHERE tmp.vlsGasID=vls.id)</code></p>

<p>Instead try this:</p>

<p><code>(vls.id, vlsStatus.id) IN (SELECT vlsGasID, max(id) FROM vertrag__lieferstelle__gas__status GROUP BY vlsGasID)</code></p>

<p>The subquery will only run once (<em>compared to once for each result in the outer query with the correlated version</em>)</p>

<p><em>Edit: Also, it may not affect performance, but I generally try to put tables referenced in the WHERE earlier in the JOIN sequence when possible.</em></p>

<p>Edit2:
Another possibility is to create a temporary table with the subquery, index the temp table appropriately (both fields), and include it in the JOIN portion of the main query.</p>

