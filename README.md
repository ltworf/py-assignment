py-assignment
=============

Python assignment...

in the User model, the resource_uri is treated almost as a primary key: it is 
used to identify remote resources that are already present locally.

Local records have resource_uri=''

When creating a new User, the record is local, but the new user is also
created remotely, this means that on the next sync, the local record will be
deleted and will be replaced by the identical record imported from remote.

Local records can't be deleted because the delete operation can't be replicated
on the remote database, since the resource_uri of the remote copy is unknown.
Another solution would have been to sync immediately after the creation of a
new record, but I was trying to save on remote calls.

Events listen when the resources are modified and store a timestamp that is then
used to generate the ETag header and let clients cache content. The database is
not huge but it can serve as example for when requests are more complex.
Anyway the ETag header is generated using an indexed field so it should be
faster.