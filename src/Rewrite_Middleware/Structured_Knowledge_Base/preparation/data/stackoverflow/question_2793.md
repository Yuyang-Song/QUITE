# Running Excel refresh all from USB drive
[Link to question](https://stackoverflow.com/questions/52479395/running-excel-refresh-all-from-usb-drive)
**Creation Date:** 1537791974
**Score:** 0
**Tags:** excel, ms-access, vba, ms-query
## Question Body
<p>I have an Access database and an Excel file with some charts &amp; pivots linked to it, and I want to put them on a USB stick so anyone can update and view the data.</p>

<p>I have some VBA in the Access file which rewrites the Excel connection strings to the queries, and this works OK. </p>

<p>Everything runs OK on my machine, but when I give it to someone else, they are able to view the database OK, but when trying to Refresh All connections in Excel, they get an error message showing the file path where I had initially saved the file on my C drive. </p>

<p>I have taken out every reference to this path I can see. Is there somewhere else in Excel / MS Query I need to update?</p>

## Answers
### Answer ID: 52484846
<p>I figured out what was going wrong.</p>

<p>There were some linked tables in the Access database and the path references were not being updated. I wrote some VBA to update these linked locations using CurrentProject.path as a starting reference.</p>

