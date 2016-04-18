This is the python version that uses a sqlite database for storage.
If you want a better performance you can add caching between DAO and sqlite.
But this will significantly increase the complexity so I avoided to implement the cache layer here.

The error handling can also be improved in the future.

Also there is no input validation for the AppRun demo. Just for fun

Important: 
For the AppRun system, PLEASE use function 5 "Transaction Settlement" to persist the transactions and update the account balances.
