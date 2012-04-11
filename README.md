BibleBot
========

Overview
--------

BibleBot watches a given email account (using IMAP) for incoming messages. When it receives a new email, it reads the email and pulls out any Scripture references (such as "Romans 12:2").

BibleBot then looks up each of these references in a specified translation (currently only ESV is supported and is used by default -- the ability to specify another translation is planned for a future version).

Having fetched the text of each verse, it replies to the original email with the text of each verse.



Configuration
-------------

BibleBot is configured using JSON; the default configuration file is named "BibleBot.conf" and lives in the same directory as BibleBot's source code; other configuration files may be specified using the "-c" or "--config=" options on the command-line. 

The keys that BibleBot needs from this JSON config file are:

* **check_interval**: the time (in seconds) BibleBot waits before checking for new emails.

* **imap_hostname**: The address of the IMAP (incoming) email server BibleBot to which should connect.

* **imap_port**: The port BibleBot should use in connecting to the IMAP email server (most of the time, this should be 993).

* **imap_label**: The address of the IMAP label BibleBot should read from (this should probably be "inbox").

* **imap_username**: The IMAP username for the email address BibleBot should check.

* **imap_password**: The IMAP password for the email address BibleBot should check.

* **smtp_hostname**: The address of the SMTP (outgoing) email server BibleBot to which should connect.

* **smtp_port**: The port BibleBot should use in connecting to the SMTP email server (most of the time, this should be either 465, 585, or 587).

* **smtp_username**: The SMTP username for the email address BibleBot should use for sending mail.

* **smtp_password**: The SMTP password for the email address BibleBot should use for sending mail.

* **smtp_use_ssl**: Whether BibleBot should use SSL (sometimes called TLS) for its connection to the SMTP email server (for security reasons, this should usually be set to "true").




Requirements
------------
BibleBot requires Python version 2.6 or higher, with the following libraries:

* **Requests** (version 0.11 or higher)
