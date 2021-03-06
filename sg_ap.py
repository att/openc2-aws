'''
 BSD License

 Copyright 2019 AT&T Intellectual Property. All other rights reserved.

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

from stix2 import properties
from openc2.properties import TargetProperty, ActuatorProperty, ArgsProperty
from openc2.base import _Target
from openc2 import Command
from nacl_ap import AWSResourceActuator
from collections import OrderedDict

class AWSSecurityGroup(Command):
    _type = 'x-aws-sg'
    _properties = OrderedDict([
        ('action', properties.EnumProperty(
            allowed=[
                "allow",
                "delete"
            ], required=True
        )),
        ('target', TargetProperty(required=True)),
        ('args', ArgsProperty()),
        ('actuator', ActuatorProperty(required=True)),
        ('command_id', properties.StringProperty())
    ])

    def _check_object_constraints(self):
        super(AWSSecurityGroup, self)._check_object_constraints()
        if not isinstance(self.target, _Target) or \
                not self.target.type in ['ipv4_connection']:
            raise ValueError("Unsupported target (%s)"%self.target)
        if not isinstance(self.actuator, AWSResourceActuator):
            raise ValueError("Unsupported actuator (%s)"%self.actuator)
