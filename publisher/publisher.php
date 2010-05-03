<?php
/**
 * Simple message sender to an AMQP server
 *
 * @author Osman Yuksel < yuxel |ET | sonsuzdongu |DOT| com >
 */

//path to your amqp-php library
require_once('../amqp.inc');


class sendMailToQueue {
  //set configs
  function __construct() {
    $this->rabbitMQConf = array("host"=>"localhost",
                                "port"=>"5672",
                                "user"=>"guest",
                                "pass"=>"guest",
                                "virtualHost"=>"/");


    $this->queueConf = array("exchange"=>"bulletin");
  }

  //send  $text $to someone with a $subject
  function send($to,$subject,$text) {
    try{
      $conn = new AMQPConnection($this->rabbitMQConf['host'], 
                                 $this->rabbitMQConf['port'],
                                 $this->rabbitMQConf['user'],
                                 $this->rabbitMQConf['pass']);

      $channel = $conn->channel();

      $channel->access_request($this->rabbitMQConf['virtualHost'], false, false, true, true);

      $mailData = array("to"=>$to,
                        "subject"=>$subject,
                        "text"=>$text);

      $mailDataToJson = json_encode($mailData);
 
      $msg = new AMQPMessage($mailDataToJson, array('content_type' => 'text/plain'));
      $channel->basic_publish($msg, $this->queueConf['exchange']);

      $channel->close();
      $conn->close();
      
      return true;
    }
    catch(Exception $e) {
      echo "Something went wrong ".$e->getMessage();
    }

  }
}


$mailSender = new sendMailToQueue();

$to = "foo@bar.com";
$subject = "This is a text message";
$text = "I show you how deep the rabbit-hole goes";

if ( $mailSender->send($to, $subject, $text ) ) {
   echo "Mail sent to queue"; 
}

