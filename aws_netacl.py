#!/usr/local/bin/python

'''
 BSD License

 Copyright 2018 AT&T Intellectual Property. All other rights reserved.

 Redistribution and use in source and binary forms, with or without modification, are permitted
 provided that the following conditions are met:

 1. Redistributions of source code must retain the above copyright notice, this list of conditions
    and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright notice, this list of
    conditions and the following disclaimer in the documentation and/or other materials provided
    with the distribution.
 3. All advertising materials mentioning features or use of this software must display the
    following acknowledgement:  This product includes software developed by the AT&T.
 4. Neither the name of AT&T nor the names of its contributors may be used to endorse or
    promote products derived from this software without specific prior written permission.
  
 THIS SOFTWARE IS PROVIDED BY AT&T INTELLECTUAL PROPERTY ''AS IS'' AND ANY EXPRESS OR
 IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
 SHALL AT&T INTELLECTUAL PROPERTY BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;  LOSS OF USE, DATA, OR PROFITS;
 OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
 DAMAGE.
'''

from flask import Flask,json,request,jsonify

import boto3

app = Flask(__name__)

@app.route('/')
def index():
	return "Hello, World!\n"

@app.route('/aws/networkacl', methods = ['POST'])
def openc2_aws_sg():
	
	if request.headers['Content-Type'] == 'application/json':
		openc2_action = request.get_json()
		account_id = openc2_action['actuator']['aws_account']
		region = openc2_action['actuator']['aws_region']
		action = openc2_action['action']
		NetAclId = openc2_action['actuator']['aws_net_acl_id']
		IpProto = openc2_action['target']['protocol']
		FromPort = int(openc2_action['target']['dst_port'])
		ToPort = int(openc2_action['target']['dst_port'])
		CidrIp = openc2_action['target']['src_ip']
		rulenm = int(openc2_action['modifiers']['rule_number'])
		direction = openc2_action['modifiers']['direction']

		if not IpProto.isdigit():
			if IpProto.lower() == 'tcp':
				IpProto='6'
			elif IpProto.lower() == 'udp':
				IpProto='17'
			elif IpProto.lower() == 'icmp':
				IpProto='1'

	
		if direction == 'inbound':
			Egress=False
		else:
			Egress=True

		session = boto3.Session(profile_name=account_id)

		ec2 = session.client('ec2',region_name=region)
		
		try:
			data = ec2.create_network_acl_entry(NetworkAclId=NetAclId, CidrBlock=CidrIp, Egress=Egress, PortRange={ 'From': FromPort, 'To': ToPort }, Protocol=IpProto, RuleAction=action, RuleNumber=rulenm )
		except Exception as e:
			errmsg = '{ "err_msg": "' + str(e) + '" }' 
			return errmsg
		else:
			return json.dumps(data)

	else:
		return "425 Unsupported Media Type"

if __name__ == '__main__':
	app.run(debug=False)
