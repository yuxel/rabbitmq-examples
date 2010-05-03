""" 
Simple AMQP consumer which simulates a mail sender 

@author Osman Yuksel < yuxel |ET| sonsuzdongu |DOT| com >

"""

from amqplib import client_0_8 as amqp
import simplejson as json # simple json to decode sent message
import time # simulates that sending message will took some time

class rabbitMQMailQueue:
  # config parameters
  def __init__(self):
    self.rabbitMQConf = {"hostPort" : "localhost:5672",
                    "user" : "guest",
                    "pass" : "guest",
                    "virtualHost" : "/"
    }

    self.queueConf = {"name" : "mails",
                      "exchange" : "bulletin"
    }

  # start listening and call sendMail on every message popped
  def listen(self):
    try:

        conn = amqp.Connection(self.rabbitMQConf['hostPort'],
                               self.rabbitMQConf['user'],
                               self.rabbitMQConf['pass'],
                               virtualHost = self.rabbitMQConf['virtualHost'],
                               insist = False)
        chan = conn.channel()

        chan.queue_declare( self.queueConf['name'], # queue name 
                            durable=True,  # create automatically on reboot
                            exclusive=False, #  we dont want it to be only accesible by queue creator
                            auto_delete=False) # we dont want the queue to be deleted when last consumer detached

        chan.exchange_declare(self.queueConf['exchange'], # exchange name
                              type="direct", # direct exchange
                              durable=True, # create automatically on reboot
                              auto_delete=False,) # do not delete when last consumer detached

        # bind queue with exchange
        chan.queue_bind(self.queueConf['name'], self.queueConf['exchange'])

        # set consumers callback method
        chan.basic_consume(self.queueConf['name'], 
                           no_ack=True, # if set to false, message will stay on server till chan.basic_ack() called  
                           callback=self.sendEmail) #set callback


        # start listening
        while True:
          chan.wait()

        chan.close()
        conn.close()

    except Exception, error :
        print "Something went wrong : ",error

  # sendMail on every message
  def sendEmail(self,msg):
    msgReceived = json.loads (msg.body) # decode json message
    print "I'm gonna send a mesage with this data : ", msgReceived
    time.sleep(10) # assume that sending this email tooks 10 seconds, next message will be poped after 10 seconds from queue

mailQueue = rabbitMQMailQueue()
mailQueue.listen()
