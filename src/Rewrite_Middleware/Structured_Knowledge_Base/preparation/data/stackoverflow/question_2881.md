# Mysql query taking long time even with LIMITS
[Link to question](https://stackoverflow.com/questions/56941266/mysql-query-taking-long-time-even-with-limits)
**Creation Date:** 1562613304
**Score:** 1
**Tags:** php, mysql
## Question Body
<p><strong>1. Summarise the problem</strong></p>

<p>Our company has been using this system for a long time and people feel huge system slowdown. I can't rewrite code because its super hardcoded and too many files to do so. </p>

<p>Few months ago we saw that one query takes about 170 s to execute. 
My workaround was add LIMITS to each query and from 170s it went down to 2-3s. But last week i saw that code now takes about 5-25 sec.</p>

<p>Also this system is on php 5.2. Its basically impossible to upgrade code to work for 5.6
3 people was rewriting this code and after 8 hour we managed to make to login page.
Indexing is limited because most of database info have strings rather than integer.</p>

<p><b>2. Provide background including what you've already tried</b></p>

<p>What i tried:<br>
- Adding limits by default 300, also users can change this limit.<br>
- Migrating server to better hardware. <br>
- Giving more RAM (10gb now) and two virtual CPU.<br>
- Migrating from local storage to network (better performance at this moment).<br></p>

<p><b>3. Show some code</b></p>

<pre><code>SELECT pastabos_apskaitininkui, 
       uzdaviniai.pakr_salis, 
       uzdaviniai.iskr_salis, 
       uzdaviniai.id                       AS uzdavinio_id, 
       salys.salis                         AS muitines_salis, 
       uzdaviniai.pakr_regionas, 
       uzdaviniai.iskr_regionas, 
       uzdaviniai.pakr_miestas, 
       uzdaviniai.iskr_miestas, 
       uzdavinio_priekaba, 
       priekabos.tipas                     AS priekabos_tipas, 
       uzdaviniai.kas_sukure_skyrius, 
       uzdaviniai.kam_sukure_skyrius, 
       uzdaviniai.kas_sukure_vadyb, 
       uzdaviniai.kam_sukure_vadyb, 
       uzdav_users.vardas_sutr             AS uzdav_user_vardas, 
       pakrov_salis.sutrumpinimas          AS uzdav_pakr_salis, 
       iskrov_salis.sutrumpinimas          AS uzdav_iskr_salis, 
       uzdaviniai.pasikrovimo_data         AS uzd_pasikrovimo_data, 
       uzdaviniai.pristatymo_data          AS uzd_pristatymo_data, 
       uzdaviniai.pastabos, 
       suma_vykdytojui_valiuta, 
       vykdytojui_valiuta, 
       uzdaviniai.eil_nr, 
       uzdaviniai.statusas, 
       uzdaviniai.statusas_baigtas_ranka, 
       keliones_lapas.reiso_nr, 
       keliones_lapas.masina, 
       keliones_lapas.masinos_id, 
       keliones_lapas.priekabos_nr, 
       keliones_lapas.priekabos_id, 
       keliones_lapas.priekabos2_nr, 
       keliones_lapas.reiso_pavadinimas, 
       keliones_lapas.vykdytojo_tipas, 
       keliones_lapas.vykdytojo_imone, 
       keliones_lapas.atvykimo_data, 
       keliones_lapas.vairuotojas, 
       keliones_lapas.vairuotojas2, 
       keliones_lapas.vairuotojas3, 
       keliones_lapas.vairuotojas4, 
       keliones_lapas.marsrutas, 
       klientai.firmos_pavadinimas         AS uzsakovas, 
       uzsakovo_uzs_nr, 
       valiutos.valiuta                    AS frachto_valiuta, 
       uzsakymas.vadybininkas, 
       uzsakymas.skyrius, 
       uzsakymas.frachtas_suma, 
       uzsakymas.pavadinimas, 
       uzsakymas.uzsakymo_id, 
       uzsakymas.reg_data, 
       uzsakymas.pastabos                  AS uzs_pastabos, 
       uzsakymas.statusas                  AS uzsakymo_statusas, 
       sask_ist.serija, 
       sask_ist.sask_nr, 
       sask_ist.id                         AS sask_id, 
       sask_ist.suma, 
       sask_ist.valiuta, 
       sask_ist.kursas                     AS sask_ist_kursas, 
       sask_ist.apmoketi_iki, 
       sask_ist.atidejimas, 
       issiuntimo_data, 
       sask_ist_apmokejimas.suma           AS ist_apm_suma, 
       sask_ist_apmokejimas.valiuta        AS ist_apm_valiuta, 
       sask_ist_apmokejimas.kursas         AS ist_apm_kursas, 
       sask_ist_apmokejimas.id             AS ist_apm_id, 
       klientu_pakr_vietos.pavadinimas     AS muitines_pavadinimas, 
       klientu_pakr_vietos.miestas         AS muitines_miestas, 
       klientu_pakr_vietos.adresas         AS muitines_adresas, 
       kokio_krovinio_dalis, 
       krovinys_konsoliduotas, 
       kroviniu_tipai.pavadinimas          AS krovinio_pavadinimas, 
       kroviniai.pasikrovimo_data, 
       kroviniai.pristatymo_data, 
       kroviniai.uzsakovo_krovinio_nr, 
       kroviniai.id                        AS krovinio_id, 
       svoris_t, 
       ldm, 
       turis, 
       paleciu_skaicius, 
       vnt, 
       temperature, 
       kroviniai.konteinerio_nr, 
       kroviniai.pakr_vietos_id            AS kr_pakr_vietos_id, 
       kroviniai.iskr_vietos_id            AS kr_iskr_vietos_id, 
       kroviniai.pakr_salis                AS kr_pakr_salis, 
       kroviniai.iskr_salis                AS kr_iskr_salis, 
       kroviniai.pakr_miestas              AS kr_pakr_miestas, 
       kroviniai.pakr_regionas             AS kr_pakr_regionas, 
       kroviniai.iskr_regionas             AS kr_iskr_regionas, 
       kroviniai.iskr_miestas              AS kr_iskr_miestas, 
       kroviniai.ismuitinimo_data          AS ismuitinimo_data, 
       kroviniai.uzmuitinimo_data          AS uzmuitinimo_data, 
       kroviniai.pasienio_postas           AS pasienio_postas, 
       kroviniai.ismuitinimo_vieta         AS ismuitinimo_vieta, 
       statusai.pavadinimas                AS st_pavadinimas, 
       st_uzsakymai.id                     AS st_id, 
       st_salys.salis                      AS st_salis, 
       st_uzsakymai.data                   AS st_data, 
       st_uzsakymai.laikas                 AS st_laikas, 
       st_uzsakymai.ivykio_pastabos_sutr   AS st_pastabos_sutr, 
       st_uzsakymai.ivykio_pastabos        AS st_pastabos, 
       st_keliones_lapas.reiso_pavadinimas AS st_reiso_pav, 
       vairuotojai.vardas                  AS sq_vardas, 
       priekabos.masinos_nr                AS sq_priekaba 
FROM   uzdaviniai 
       LEFT JOIN priekabos 
              ON priekabos.id = uzdaviniai.uzdavinio_priekaba 
       LEFT JOIN users AS uzdav_users 
              ON uzdav_users.id = uzdaviniai.kam_sukure_vadyb 
       LEFT JOIN salys AS pakrov_salis 
              ON pakrov_salis.id = uzdaviniai.pakr_salis 
       LEFT JOIN salys AS iskrov_salis 
              ON iskrov_salis.id = uzdaviniai.iskr_salis 
       LEFT JOIN uzsakymas 
              ON uzdaviniai.uzsakymo_id = uzsakymas.uzsakymo_id 
       LEFT JOIN uzd_kur_vykdytas 
              ON uzdaviniai.id = uzd_kur_vykdytas.uzdavinio_id 
       LEFT JOIN keliones_lapas 
              ON keliones_lapas.reiso_nr = uzd_kur_vykdytas.reiso_nr 
       LEFT JOIN st_uzsakymai 
              ON st_uzsakymai.uzdavinio_id = uzdaviniai.id 
       LEFT JOIN statusai 
              ON statusai.id = st_uzsakymai.statuso_id 
       LEFT JOIN salys AS st_salys 
              ON st_salys.id = st_uzsakymai.salis 
       LEFT JOIN keliones_lapas AS st_keliones_lapas 
              ON st_keliones_lapas.reiso_nr = st_uzsakymai.reiso_nr 
       LEFT JOIN vairuotojai 
              ON vairuotojai.id = keliones_lapas.vairuotojas 
       LEFT JOIN sask_ist_uz_ka 
              ON sask_ist_uz_ka.uzsakymo_id = uzsakymas.uzsakymo_id 
       LEFT JOIN sask_ist 
              ON sask_ist.id = sask_ist_uz_ka.sask_id 
       LEFT JOIN sask_ist_apmokejimas 
              ON sask_ist.id = sask_ist_apmokejimas.sask_id 
       LEFT JOIN uzsakymo_kroviniai 
              ON uzsakymas.uzsakymo_id = uzsakymo_kroviniai.uzsakymo_id 
       LEFT JOIN kroviniai 
              ON kroviniai.id = uzsakymo_kroviniai.krovinio_id 
       LEFT JOIN klientu_pakr_vietos 
              ON klientu_pakr_vietos.id = kroviniai.ismuitinimo_vieta 
       LEFT JOIN klientu_pakr_vietos AS iskr_vietos_uzd 
              ON iskr_vietos_uzd.id = uzdaviniai.pakr_vietos_id 
       LEFT JOIN salys 
              ON salys.id = klientu_pakr_vietos.salis 
       LEFT JOIN cmr_kroviniai 
              ON kroviniai.id = cmr_kroviniai.krovinio_id 
       LEFT JOIN cmr 
              ON cmr.id = cmr_kroviniai.cmr_id 
       LEFT JOIN cmr_panaudojimas 
              ON cmr_panaudojimas.cmr_id = cmr_kroviniai.cmr_id 
                 AND keliones_lapas.reiso_nr = cmr_panaudojimas.reiso_nr 
       LEFT JOIN kroviniu_tipai 
              ON kroviniu_tipai.id = kroviniai.krovinio_pavadinimas 
       LEFT JOIN klientai 
              ON klientai.id = uzsakymas.kliento_id 
       LEFT JOIN valiutos 
              ON valiutos.id = uzsakymas.frachtas_valiuta 
WHERE  1 = 1 
       AND ( `uzdaviniai`.`pasikrovimo_data` BETWEEN 
             '2019-07-08' AND '2019-07-08 23:59:59' 
           ) 
ORDER  BY uzdaviniai.pasikrovimo_data DESC 
LIMIT  300
</code></pre>

<p>As you can see there is many left join, statements.</p>

<p><b>4. Result</b></p>

<p>What i want is some help what can i do with this piece of crap or some recommendation what can i change. As i expect these query will take more and more time to execute.</p>

## Answers
### Answer ID: 56943982
<p>Consider changing your  </p>

<pre><code>WHERE  1 = 1 
   AND ( `uzdaviniai`.`pasikrovimo_data` BETWEEN 
         '2019-07-08' AND '2019-07-08 23:59:59' 
       ) 
</code></pre>

<p>TO</p>

<p>WHERE  <code>uzdaviniai</code>.<code>pasikrovimo_data</code> BETWEEN 
             '2019-07-08' AND '2019-07-08 23:59:59' </p>

<p>and let us know results (with the backticks), please.</p>

### Answer ID: 56941762
<p>If the query is fast when executed directly in mysql console, then the query has no problem at all, and what is slow is the php code that uses the results of the query, php code that you don't show and that you should revise/post here.</p>

<p>If the query is slow even in mysql console, then the problem can be the size of the master/joined tables (but this may be resolved by relaxing the memory limits of the mysql server and/or adding ram to the server), or could be non correct indexing of the joined tables, since any LEFT JOIN needs the joined table to be indexed on the field you use to join it (and this could be resolved by creating the correct indexes on the joined tables).</p>

