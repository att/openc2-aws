# openc2-aws

This is a small openC2 (OC2) reference implementation demonstrating the
rudimentary use of OC2 to manage both network ACLs and security groups in
AWS.

This particular implementation uses Flask in order to process RESTful POST calls
with the payload consisting of JSON requests. This is covered in more detail
later in this document. 

&nbsp;

## Requirements

 * Flask 0.12
 * boto3 1.7.51
 * openc2-lycan-python 1.0
 * Python 3.x

&nbsp;
## Installation

Make sure you are using a Python 3 interpreter and install AWS boto3 along
Flask. Both boto3 and Flask can be installed through pip. For example,
<br>
&nbsp;&nbsp;&nbsp;&nbsp;<b>pip install boto3</b>

You will also need to create an AWS profile containing your AWS API access
information. This is typically done by creating a file called "credentials"
and stored under an ".aws" subdirectory. I direct you to the AWS boto3 
documentation for more information.

##Example credentials file

```text
[default]
aws_access_key_id=<default access key>
aws_secret_access_key=<default access key secret>

[123456789000]
aws_access_key_id=<access key for given account>
aws_secret_access_key=<access key secret for givin account>
```

## Running the client

There are currenly two REST clients:

### aws_netacl.py

This client processes Network ACLs via the RESTful POST api call:
<p>
&nbsp;&nbsp;&nbsp;&nbsp;<b>/aws/networkacl</b>
</p>

The client can be started from the command line as follows:
<p>
&nbsp;&nbsp;&nbsp;&nbsp;<b>python -m aws_netacl.py</b>
</p>

By default, Flask listens on port 5000 which can be changed through a
Flask configuration file. I direct the user to the Flask documentation
for more information on how to change this.

###Example

To test the interface, the following curl command can be made:
<br>
&nbsp;&nbsp;&nbsp;&nbsp;<b>curl -XPOST -H'Content-Type: application/json' -d "@aclAllow.json" localhost:5000/aws/networkacl</b>
</br>

The following is an example of a JSON request. Again, the "aws_account"
is tied to the credentials file under your ".aws" subdirectory.

#### aclAllow.json

```json
{
  "action": "allow",
  "actuator": {
    "x-aws-nacl": {
        "aws_account" : "123456789000",
        "aws_region" : "eu-west-3",
        "aws_nacl_id": "nacl ID"
    }
  },
  "args": {
    "x-aws-nacl:rule_number": "10",
    "x-aws-nacl:direction": "inbound"
  },
  "target": {
    "ipv4_connection": {
        "src_addr": "135.0.0.0/24",
        "dst_port": "8888",
        "protocol": "tcp"
    }
  }
}
```

### aws_sg.py

Similarly the security group client can be run from the command line
 as follows: 
 
<p>
&nbsp;&nbsp;&nbsp;&nbsp;<b>python -m aws_sg.py</b>
</p>

The REST API call in this case is:
<br>
&nbsp;&nbsp;&nbsp;&nbsp;<b>/aws/securitygroup</b>
</br>

To test the interface, the following curl command can be made:
<br>
&nbsp;&nbsp;&nbsp;&nbsp;<b>curl -XPOST -H'Content-Type: application/json' -d "@allow.json" localhost:5000/aws/networkacl</b>
</br>
