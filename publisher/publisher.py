""" 
Simple message sender to an AMQP server

@author Osman Yuksel < yuxel |ET | sonsuzdongu |DOT| com >
"""

from amqplib import client_0_8 as amqp
import simplejson as json # to encode message into json


class sendMailToQueue:

  #configs
  def __init__(self):
    self.rabbitMQConf = {"hostPort" : "localhost:5672",
                         "user" : "guest",
                         "pass" : "guest",
                         "virtualHost" : "/"
    }

    self.queueConf = {"exchange" : "bulletin"}


  #send 'text' 'to' someone with a 'subject'
  def send(self, to, subject, text):
    mailData = {"to" : to,
                "subject" : subject,
                "text" : text
    }
    
    # encode data into JSON
    mailDataToJson = json.dumps ( mailData )

    try:
      conn = amqp.Connection(self.rabbitMQConf['hostPort'],
                             self.rabbitMQConf['user'],
                             self.rabbitMQConf['pass'],
                             virtualHost = self.rabbitMQConf['virtualHost'],
                             insist=False)
      chan = conn.channel()

      msg = amqp.Message(mailDataToJson)
      msg.properties["delivery_mode"] = 2 # message is persistent
      chan.basic_publish(msg,exchange=self.queueConf['exchange'])

      chan.close()
      conn.close()

    except Exception, error :
      print "Something went wrong : ",error


mailSender = sendMailToQueue()
mailSender.send("foo@bar.com",
                "This is text message",
                "I show you how deep the rabbit-hole goes")

