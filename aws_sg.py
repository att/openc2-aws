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

from sg_ap import AWSSecurityGroup
from openc2 import parse, Response

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!\n"

@app.route('/aws/securitygroup', methods = ['POST'])
def openc2_aws_sg():
    if request.headers['Content-Type'] == 'application/json':
        cmd = parse(request.get_json())
        try:
            sgap = AWSSecurityGroup(**cmd)
        except Exception as e:
            resp = Response(status=400,
                status_text="Invalid command format/arguments (%s)"%str(e))
            return resp.serialize()

        session = boto3.Session(profile_name=sgap.actuator.aws_account_id)
        ec2 = session.client('ec2',region_name=sgap.actuator.aws_region)
		
        if sgap.action == "allow":
            try:
                data = ec2.authorize_security_group_ingress( GroupId=sgap.actuator.aws_resource_id, IpProtocol=sgap.target.protocol, 
                            FromPort=sg.target.dst_port, ToPort=sg.target.dst_port, CidrIp=sg.target.src_addr)
            except Exception as e:
                #todo: parse boto3 for http code and resp
                resp = Response(status=400,
                                status_text=str(e))
                return resp.serialize()
            else:
                resp = Response(status=200,
                                results = {"x-aws-sg":data})
                return resp.serialize()
        elif sgap.action == "delete":
            try:
                data = ec2.revoke_security_group_ingress( GroupId=sgap.actuator.aws_sg_id, IpProtocol=sgap.target.protocol, 
                        FromPort=sgap.target.dst_port, ToPort=sgap.target.dst_port, CidrIp=sgap.target.src_addr )
            except Exception as e:
                #todo: parse boto3 for http code and resp
                resp = Response(status=400,
                                status_text=str(e))
                return resp.serialize()
            else:
                resp = Response(status=200,
                                results = {"x-aws-sg":data})
                return resp.serialize()
    else:
        resp = Response(status=425,
                        status_text="Unsupported Media Type")
        return resp.serialize()

if __name__ == '__main__':
    app.run(debug=False)
