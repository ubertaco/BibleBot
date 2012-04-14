To do
-----
* New configuration file format

    * needs to support specification of multiple channels, each with a sender and a listener, with options for each.

        * Best option might be to stick with JSON; each root-level entry is a channel containing a "name" entry, a "listener" entry, and a "sender" entry

* Finish implementing IMAPListener and SMTPSender

* Migrate Main.py to new system
