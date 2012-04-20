BibleBot
========

Overview
--------

BibleBot watches varying sources for incoming messages. When it receives a new message, it reads the message and pulls out any Scripture references (such as "Romans 12:2") -- these become BibleBot's "requests". 

BibleBot then looks up each of these references in a specified translation (currently only ESV is supported and is used by default -- the ability to specify another translation is planned for a future version).

Having fetched the text of each verse, it responds to the original message's sender with the text of each verse.

Configuration
-------------

BibleBot is configured using JSON; the default configuration file is named "BibleBot.conf" and lives in the same directory as BibleBot's source code; other configuration files may be specified using the `-c` or `--config=` options on the command-line. 

Configuration files specify a list of Channels, each of which has a Listener (to receive passage lookup requests) and a Sender (to send responses for each passage looked up)

The syntax for configuration files is:

        {
            "channel_name": {

                "listener": {
                    "type": "listener_type",
                    < listener_configuration >
                },

                "sender": {
                    "type": "sender_type",
                    < sender_configuration >
                }
            }
        }

The options for listener\_configuration and sender\_configuration vary based on the type of listener and sender.

### Available Listener Types ###

#### IMAP ####

IMAP listeners watch an email inbox using the IMAP protocol.

The required configuration options for IMAP listeners are:

* **server**: The address of the IMAP email server BibleBot to which should connect.

* **port**: The port BibleBot should use in connecting to the IMAP email server (most of the time, this should be 993).

* **label**: The address of the email label (like a folder or sub-category of your email) BibleBot should watch for incoming requests (this should usually be "inbox").

* **username**: The username for the email address BibleBot should check.

* **password**: The password for the email address BibleBot should check.

* **use_ssl**: Whether BibleBot should use SSL (sometimes called TLS) for its connection to the email server (for security reasons, this should usually be set to "true").

### Available Sender Types ###

#### SMTP ####

SMTP senders send emails by connecting to an email server using the SMTP protocol.

The required configuration options for IMAP listeners are:

* **server**: The address of the SMTP (outgoing) email server BibleBot to which should connect.

* **port**: The port BibleBot should use in connecting to the SMTP email server (most of the time, this should be either 465, 585, or 587).

* **username**: The username for the email address BibleBot should use to send mail.

* **password**: The password for the email address BibleBot should use to send mail.

* **use_ssl**: Whether BibleBot should use SSL (sometimes called TLS) for its connection to the SMTP email server (for security reasons, this should usually be set to "true").


Requirements
------------
BibleBot requires Python version 2.6 or higher, with the following libraries:

* **Requests** (version 0.11 or higher)
