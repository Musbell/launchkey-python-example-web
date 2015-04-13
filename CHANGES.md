CHANGELOG for LaunchKey Python SDK Web Example
==============================================

1.1.0
-----

Updates for cleaner code and distribution

* Use SQLite memory database to not have to write to the file system
* Move static files to their own directories at the root of the project
* Update the README to alert the user of why there are 401 and 403 responses in the logs
* Move the LaunchKey API instantiation to the main instead of the handler to reduce file access
* Override finish_request on the socket server to ignore broken pipe response errors when closing the connection
* Refactor handler do_POST do pull out duplicate code

1.0.0
-----

Initial release