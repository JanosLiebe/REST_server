### items.py and server.py has been implemented by XXX company (I share this information only by request).

However these has been modified by me to be able to initialize item's store due to testing purposes.
The idea behind is when a database solution is under testing then initialization of database before or 
after each testcase should be done independently the interface is used during testing. Eg. if we test an sql database via REST
then there should be a separate connection to sql database to initialize that.
Currently it was not possible fully as database is based on python's dictionary element, but still there is a independently 
implemented solution to initialize database.
