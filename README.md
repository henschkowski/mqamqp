### General ###

IBM AMQP Support:
https://www.ibm.com/support/knowledgecenter/en/SSFKSJ_8.0.0/com.ibm.mq.amqp.doc/amqp_support.htm

ApacheQpid Client for Python3:
https://qpid.apache.org/releases/qpid-proton-0.18.1/proton/python/book/index.html




### Setup MQ / Queue Manager ###

Setup AMQP channel:
(From https://www.ibm.com/support/knowledgecenter/en/SSFKSJ_8.0.0/com.ibm.mq.amqp.doc/tamqp_creating.htm)

Create a queue manager:
    crtmqm QMGR2

Increase command level to have AMQP features enabled:
    strmqm -e CMDLEVEL=801  QMGR2


Create an AMQP channel:
    echo "ALTER CHANNEL(SYSTEM.DEF.AMQP) CHLTYPE(AMQP) MCAUSER(mqm)" | runmqsc QMGR2

Give permissions to user:
    setmqaut -m QMGR2 -t qmgr -p mqm -all +connect
    setmqaut -m QMGR2 -t qmgr -p mqm +all 


Open Security for admin user 'mqm' (http://www-01.ibm.com/support/docview.wss?uid=swg21680930):
    echo "ALTER AUTHINFO(SYSTEM.DEFAULT.AUTHINFO.IDPWOS) AUTHTYPE(IDPWOS) CHCKCLNT(OPTIONAL)" | runmqsc QMGR2
    echo "REFRESH SECURITY TYPE(CONNAUTH)" | runmqsc QMGR2


Start AMQP service and channel:
    echo "START SERVICE(SYSTEM.AMQP.SERVICE)" | runmqsc QMGR2
    echo "START CHANNEL(SYSTEM.DEF.AMQP)" | runmqsc QMGR2


### Client side ###

Create a Virtual Environment:
    virtualenv -p python3 .
    . bin/activate

Install the QPID client:
    pip install python-qpid-proton

Run client:
    python client.py