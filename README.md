# LaunchKey SDK for Python - Web Example

  * [Overview](#overview)
  * [Pre-Requisites](#prerequisites)
  * [Installing](#installing)
  * [Usage](#usage)
  * [Support](#support)

<a name="overview"></a>
# Overview

LaunchKey is an identity and access management platform  This SDK enables developers to quickly integrate
the LaunchKey platform and Python based applications without the need to directly interact with the platform API.

Developer documentation for using the LaunchKey API is found [here](https://launchkey.com/docs/).

An overview of the LaunchKey platform can be found [here](https://launchkey.com/platform).

#  <a name="prerequisites"></a>Pre-Requisites

Utilization of the LaunchKey SDK requires the following items:

 * LaunchKey Account - The [LaunchKey Mobile App](https://launchkey.com/app) is required to set up a new account and
 access the LaunchKey Dashboard.

 * An application - A new application can be created in the [LaunchKey Dashboard](https://dashboard.launchkey.com/).
   From the application, you will need the following items found in the keys section of the application details:

    * The app key
    * The secret key
    * The private key

<a name="installing"></a>
# Installing

## Get the example code

```bash
git clone https://github.com/LaunchKey/launchkey-python-example-cli.git
```

or get a an archive from [the latest release](https://github.com/LaunchKey/launchkey-python-example-web/releases/latest).

## Install The Application

Once you have the code you need to install it:

```bash
$ python setup.py install
```

<a name="usage"></a>
# Usage

1. Get the app info necesary to start the web server

    * ```app_key``` - The app key value.  This value is automatically generate
    
    * ```secret_key``` - The secret key value.  Create a new one to copy if you have not done so already.
    
    * ```rsa_private_key_location``` - The location of the private key.  Download a new key from the dashboard if you have
    not done so already.  This must be an absolute path.

2. Start your web server

    ```bash
    $ launchkeywebdemo app_key secret_key rsa_private_key_location
      Starting server, use <Ctrl-C> to stop
    ```

3. Verify the server is running by accessing the URL of your web server: [http://127.0.0.1:8080](http://127.0.0.1:8080).

4. Start your reverse proxy.

    ```bash
    $ ngrok 8080
    ```

    Once started, you should see a a screen similar to:

    ```
    ngrok                                                                                          (Ctrl+C to quit)

    Tunnel Status                 online
    Version                       1.7/1.7
    Forwarding                    http://z4182320.ngrok.com -> 127.0.0.1:8080
    Forwarding                    https://z4182320.ngrok.com -> 127.0.0.1:8080
    Web Interface                 127.0.0.1:4040
    # Conn                        0
    Avg Conn Time                 0.00ms

    ```

4. Verify your reverse proxy by accessing the reverse proxy endpoint.  The endpoint will be the first part of one of the
Forwarding lines.  Based on the example above it would be ```https://z4182320.ngrok.com``` or
```http://z4182320.ngrok.com```.  Copy your value for the Forwarding endpoint into you browser to ensure it is
working correctly.  If working correctly, it will displaying the same web page you saw when verifying your web server
as well as show 200 OK responses in the HTTP Requests section of the ngrok screen like below:

    ```
    ngrok                                                                                          (Ctrl+C to quit)

    Tunnel Status                 online
    Version                       1.7/1.7
    Forwarding                    http://z4182320.ngrok.com -> 127.0.0.1:8080
    Forwarding                    https://z4182320.ngrok.com -> 127.0.0.1:8080
    Web Interface                 127.0.0.1:4040
    # Conn                        2
    Avg Conn Time                 3.07ms


    HTTP Requests
    -------------

    GET /favicon.ico              200 OK
    GET /                         200 OK

    ```

5. Now that your web server and reverse proxy are working, update your application with the callback URL.  This is done
by placing the URL you just verified from Ngrok into the callback field in the General section of your LaunchKey
application configuration.

5. __Winning!__ - You should be ready to try the demo and see how the Python SDK can be used to quickly and easily secure
your application with LaunchKey.


<a name="support"></a>
# Support

## GitHub

Submit feature requests and bugs on [GitHub](https://github.com/LaunchKey/launchkey-python-example-cli/issues).

## Twitter

Submit a question to the Twitter Handle [@LaunchKeyHelp](https://twitter.com/LaunchKeyHelp).

## IRC

Engage the LaunchKey team in the `#launchkey` chat room on [freenode](https://freenode.net/).

## LaunchKey Help Desk

Browse FAQ's or submit a question to the LaunchKey support team for both
technical and non-technical issues. Visit the LaunchKey Help Desk [here](https://launchkey.desk.com/).
