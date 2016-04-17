This is the python version that uses a sqlite database for storage.
If you want a better performance you can add caching between DAO and sqlite.
But this will significantly increase the complexity so I avoid implementing the cache here.
The error handling can also be improved in the future