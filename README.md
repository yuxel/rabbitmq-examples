# RabbitMQ examples

An example which demonstrates Consumer(server)/Publisher(client) integration to [RabbitMQ](http://www.rabbitmq.com)

## Prerequisites

* [RabbitMQ Server](http://www.rabbitmq.com/download.html) : To handle our queue
* [py-amqplib](http://barryp.org/software/py-amqplib/) : Python libraries for AMQP
* [simplejson](http://pypi.python.org/pypi/simplejson/) : Python library to encode/decode JSON data 
* [php-amqplib](http://code.google.com/p/php-amqplib/) : PHP library for AMQP


## Contents

* consumer/consumer.py : A simple consumer, which listens RabbitMQ messages and simulates a mail queue
* publisher/publisher.py : A simple consumer, which listens RabbitMQ messages and simulates a mail queue
* publisher/publisher.php : A simple consumer, which listens RabbitMQ messages and simulates a mail queue


## How to run

Ensure that you installed and started RabbitMQ server, py-amqplib, simplejson and php-amqplib

First you need to run your consumer which will simulate a mail sender

    cd consumer && python consumer.py

After then you can send messages with one your publisher

    cd publisher && python publisher.py
    cd publisher && php publisher.php or run this PHP code from your web server

