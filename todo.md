To do
-----
* Allow specification of polling interval for each channel

    * Conf needs to be able to pull out this value

    * Main needs to be smart enough to check if any channels are ready for polling


Next Version
------------
* Bible translation selection
    
    * More translations need to be available

* Concurrency
    
    * Channels will be the basic unit of concurrency 
    
        * The responsibility of Main, then, will be to create necessary Channels and start them

        * Use `multiprocessing` lib, not `threading`
