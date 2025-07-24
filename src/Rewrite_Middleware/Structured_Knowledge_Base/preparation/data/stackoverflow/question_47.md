# Making My PHP Site Hack Resistant
[Link to question](https://stackoverflow.com/questions/11027088/making-my-php-site-hack-resistant)
**Creation Date:** 1339651349
**Score:** -1
**Tags:** php, mysql, content-management-system, pdo, salt-cryptography
## Question Body
<p>I'm making a custom CMS for a website I've been planning and security is a big concern. </p>

<p>I probably lack the expertise to fend off a full scale hacker social engineering his way into the server room but this is a list of what I've compiled from here and other sites to prevent hacking attempts please comment if anything here is lacking or if further steps should be taken</p>

<p><strong>STAGE 1</strong></p>

<hr>

<p>using PDO to make database calls and htaccess to rewrite urls as to conceal things such as
index.php?get=variable now is myurl.com/get/variable</p>

<p>and aforementioned variable is passed through PDO as outlined <a href="https://stackoverflow.com/questions/60174/best-way-to-prevent-sql-injection-in-php">here</a> </p>

<p>moving database queries and functions into folders that deny HTTP access and lock certain admin functions behind a server usergroup which only the few will be trusted with access to.</p>

<p>All passwords are encrypted and will never be decrypted for plain text as I have no sane reason to need to read other peoples passwords.</p>

<p>Login and user creation stop gaped by an IP address auto lockout based on X amount of attempts and reCapatcha</p>

<p><strong>Stage 2</strong></p>

<hr>

<p>these steps find a home mostly because I intend to one day distribute this software and don't want egg on my face</p>

<p>User tracking to prevent finding files and logging intrusion attempts</p>

<p>IP tracking to prevent XXS hijacking and possible behavior monitoring for similar reasons</p>

<p>I'd think of more but my brain is now jumping to requiring two stage facial recognition and a DB of state ID's </p>

## Answers
### Answer ID: 11027332
<p>I think it's admirable that you're thinking big and want an accomplishment under your belt that you've coded and that you're proud of. I think we all would like to code something really solid that we can point to and say "I did that" and feel a real sense of accomplishment.</p>

<p>I won't tell you that it can't be done, but I well agree with the other comments that security is a huge, huge, huge topic and you've only scraped the very surface here. You have some good items in your list of steps, but web application security goes well beyond authentication and intrusion. From the steps you've written, it seems like you have an understanding of some of the basics of application security.</p>

<p>With that said, a really thorough and comprehensive security professional needs to consider:
* what version of apache do you recommend people deploy on? what are the known issues with the versions of mod_php or mod_fcgid that you'll recommend?
* what version of PHP will you run? are you aware of any outstanding vulnerabilities with the version of the interpreter that you'll code in?
* how will you recommend that people harden the server? e.g. besides having apache and mysql running, what other services need to be active? will you allow SSH to the server? if the web server and db are on two different machines, how do you ensure that only the web server can talk to the db server?</p>

<p>Some of the other things you mentioned like intrusion detection, facial recognition, etc. are extremely complex topics and there are whole companies building products just around each topic area. </p>

<p>My point is: it is basically impossible for one person to be able to think of every possible security issue that could come up and - even if you <em>could</em> think of all of them today - tomorrow someone is likely to discover a security issue that no-one has heard of before.</p>

<p>So, it's good to be ambitious, but it's also good to know what you're dealing with before you get in over your head. (That's another trait of a good security professional, too).</p>

### Answer ID: 11027139
<p>Unless you have a lot of time on your hands and a team of experienced people, your CMS will never be up to par with ones like Joomla, Drupal, or Wordpress. </p>

<p>Since they've been around for a while, they've been weatherproofed, but even then hackers find exploits.</p>

<p>Not trying to discourage you, but if security is a big concern, I would just go with a well established CMS. More specifically I would use Wordpress for simplicity. It's also very easy to create custom themes and create custom functions and plugins.</p>

<p>Like PST mentioned above, <em>no need to reinvent the wheel</em></p>

