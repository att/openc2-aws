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

@app.route('/aws/securitygroup', methods = ['POST'])
def openc2_aws_sg():
	
	if request.headers['Content-Type'] == 'application/json':
		openc2_action = request.get_json()
		account_id = openc2_action['actuator']['aws_account']
		region = openc2_action['actuator']['aws_region']
		sg_id = openc2_action['actuator']['aws_sgid']
		IpProto = openc2_action['target']['protocol']
		FromPort = int(openc2_action['target']['dst_port'])
		ToPort = int(openc2_action['target']['dst_port'])
		CidrIp = openc2_action['target']['src_ip']

		session = boto3.Session(profile_name=account_id)

		ec2 = session.client('ec2',region_name=region)
		
		if openc2_action['action'] == 'allow':
			try:
				data = ec2.authorize_security_group_ingress( GroupId=sg_id, IpProtocol=IpProto, FromPort=FromPort, ToPort=ToPort, CidrIp=CidrIp )
			except Exception as e:
				errmsg = '{ "err_msg": "' + str(e) + '" }' 
				return errmsg
			else:
				return json.dumps(data)

		elif openc2_action['action'] == 'deny':
			try:
				data = ec2.revoke_security_group_ingress( GroupId=sg_id, IpProtocol=IpProto, FromPort=FromPort, ToPort=ToPort, CidrIp=CidrIp )
			except Exception as e:
				errmsg = '{ "err_msg": "' + str(e) + '" }'	
				return errmsg
			else:
				return json.dumps(data)

		else:
			return "No action specified"
			

	else:
		return "425 Unsupported Media Type"

if __name__ == '__main__':
	app.run(debug=False)
