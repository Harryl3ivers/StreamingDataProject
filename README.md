


How to use this tool locally
----------------------------

How to deploy this tool
-----------------------



Please note - 'Data should not be persisted in the message broker longer than three days'
-----------------------------------------------------------------------------------------
The specification has requested the above, but  this will largly depend on the message
broker being used. For instance, AWS Kinesis doesn't have a per record retention polciy
but rather on the entire queue -:
https://docs.aws.amazon.com/streams/latest/dev/kinesis-extended-retention.html

As such ensure that when configuring the AWS kineses queue you set an applciable retention
policy