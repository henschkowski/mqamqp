### General ###

This repository provides instructions on setting up a IBM MQ Queue
manager with a AMQP channel, and a working Apache QPid python3 client to send and receive messages.

IBM AMQP Support:
https://www.ibm.com/support/knowledgecenter/en/SSFKSJ_8.0.0/com.ibm.mq.amqp.doc/amqp_support.htm

ApacheQpid Client for Python3:
https://qpid.apache.org/releases/qpid-proton-0.18.1/proton/python/book/index.html




### Setup MQ / Queue Manager ###

Setup AMQP channel:
(From https://www.ibm.com/support/knowledgecenter/en/SSFKSJ_8.0.0/com.ibm.mq.amqp.doc/tamqp_creating.htm)

Create a queue manager:

```bash
crtmqm QMGR2
```

Increase command level to have AMQP features enabled:

```bash
strmqm -e CMDLEVEL=801  QMGR2
```


Create an AMQP channel:

```bash
echo "ALTER CHANNEL(SYSTEM.DEF.AMQP) CHLTYPE(AMQP) MCAUSER(mqm)" | runmqsc QMGR2
```

Give permissions to user:

```bash
setmqaut -m QMGR2 -t qmgr -p mqm -all +connect
setmqaut -m QMGR2 -t qmgr -p mqm +all 
```


Security alternatives:

-  Disable password check for admin user 'mqm' (http://www-01.ibm.com/support/docview.wss?uid=swg21680930):

    ```bash
    echo "ALTER AUTHINFO(SYSTEM.DEFAULT.AUTHINFO.IDPWOS) AUTHTYPE(IDPWOS) CHCKCLNT(OPTIONAL)" | runmqsc QMGR2
    echo "REFRESH SECURITY TYPE(CONNAUTH)" | runmqsc QMGR2
    ```


-  Set the UNIX password for user mqm and change connection URL in client.py like

    ```python
    ...
    Container(HelloWorld("amqp://mqm:<mqm-password>@localhost:5672", "/examples/test")).run()
    ...
    ```


Start AMQP service and channel:

```bash
echo "START SERVICE(SYSTEM.AMQP.SERVICE)" | runmqsc QMGR2
echo "START CHANNEL(SYSTEM.DEF.AMQP)" | runmqsc QMGR2
```


### Client side ###

Create a Virtual Environment:

```bash
virtualenv -p python3 .
. bin/activate
```

Install the QPID client:

```bash
pip install python-qpid-proton
```

Run the client. The client publishes messages to a Topic
(`/examples/test`), and afterwards reads its message from the same
topic.

```bash
python client.py
```