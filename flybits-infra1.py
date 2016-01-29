# Python code based on Pyplates to generate CloudFormation template
# Authors: Mehdi Kianpour, Nick Majedi
# Date: 12-01-2016

import sys
import json
sys.path.append('../pyplates')


stack_name = 'Production'
version = '2.1.0'

vpc_fb = stack_name + 'VPCfb'
gw_main = stack_name + 'Gateway'

api_ami = 'ami-69795403'
devportal_ami = 'ami-9f7855f5'
staffportal_ami = 'ami-2079544a'
moments_ami = 'ami-407e532a'
scheduler_ami = 'ami-69052703'

vpc_net = '10.0.0.0/16'

api_subnet1 = '10.0.10.0/24'
api_subnet2 = '10.0.11.0/24'
api_subnet3 = '10.0.12.0/24'
devportal_subnet1 = '10.0.20.0/24'
devportal_subnet2 = '10.0.21.0/24'
devportal_subnet3 = '10.0.22.0/24'
staffportal_subnet1 = '10.0.30.0/24'
staffportal_subnet2 = '10.0.31.0/24'
staffportal_subnet3 = '10.0.32.0/24'
task_scheduler_subnet = '10.0.40.0/24'
moments_subnet1 = '10.0.60.0/24'
moments_subnet2 = '10.0.61.0/24'
moments_subnet3 = '10.0.62.0/24'

rc4_subnet = '141.117.160.0/22'

cert_arn = 'arn:aws:iam::118253587892:server-certificate/api-cert'

api_asg_max = 2
api_asg_min = 1
api_instance_type = 'c4.large'

devportal_asg_max = 2
devportal_asg_min = 1
devportal_instance_type = 'c4.large'

staffportal_asg_max = 2
staffportal_asg_min = 1
staffportal_instance_type = 'c4.large'

moments_asg_max = 2
moments_asg_min = 1
moments_instance_type = 'c4.large'

elb_health_port = 443
elb_protocol = "TCP"

vol_size = 100
fb_key = 'TornadoDevKeyPair'

with open('templates/api_files.cfn') as api_json_files:
  api_json_files_data = json.load(api_json_files)
with open('templates/api_services.cfn') as api_json_services:
  api_json_services_data = json.load(api_json_services)
with open('templates/api_commands.cfn') as api_json_commands:
  api_json_commands_data = json.load(api_json_commands)

json_files_string = json.dumps(api_json_files_data)
json_commands_string = json.dumps(api_json_commands_data)

api_json_files_string = json_files_string.replace("APIasg", stack_name + "APIasg")
api_json_files_string = api_json_files_string.replace("/CoreAPIs.zip", '/' + version + "/CoreAPIs.zip")
api_json_files_data = json.loads(api_json_files_string)

dev_json_files_string = json_files_string.replace("APIasg", stack_name + "DevPortalasg")
dev_json_files_string = dev_json_files_string.replace("/CoreAPIs.zip", '/' + version + "/DeveloperAPIs.zip")
dev_json_files_string = dev_json_files_string.replace("\CoreAPIs.zip","\DeveloperAPIs.zip")
dev_json_files_data = json.loads(dev_json_files_string)
dev_json_commands_string = json_commands_string.replace("CoreAPIs", "DeveloperAPIs")
dev_json_commands_data = json.loads(dev_json_commands_string)

staff_json_files_string = json_files_string.replace("APIasg", stack_name + "StaffPortalasg")
staff_json_files_string = staff_json_files_string.replace("/CoreAPIs.zip", '/' + version + "/StaffAPIs.zip")
staff_json_files_data = json.loads(staff_json_files_string)

# Following Availability zones will be automatically chosen based on the region
az1 = {
          "Fn::Select": [
            0,
            {
              "Fn::GetAZs": ""
            }
          ]
        }
az2 = {
          "Fn::Select": [
            1,
            {
              "Fn::GetAZs": ""
            }
          ]
        }
az3 = {
          "Fn::Select": [
            3,
            {
              "Fn::GetAZs": ""
            }
          ]
        }

cft = CloudFormationTemplate(description="Flybits" + stack_name + "Template")

cft.resources.add(Resource(vpc_fb, 'AWS::EC2::VPC',
	{
      "CidrBlock" : vpc_net,
      "EnableDnsSupport" : 'true',
      "EnableDnsHostnames" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : vpc_fb } ]	
    })
)

cft.resources.add(Resource(gw_main, 'AWS::EC2::InternetGateway'))

cft.resources.add(Resource(stack_name + 'Route', 'AWS::EC2::Route',
	{
      "GatewayId" : { "Ref" : gw_main },
      "DestinationCidrBlock": "0.0.0.0/0",
      "RouteTableId": { "Ref" : stack_name + 'RouteTable' }
	}
	)
)

cft.resources.add(Resource('VPCGWAttach', 'AWS::EC2::VPCGatewayAttachment',
	{
      "InternetGatewayId" : { "Ref" : gw_main },
      "VpcId": { "Ref" : vpc_fb }
	}
	)
)

cft.resources.add(Resource(stack_name + 'RouteTable', 'AWS::EC2::RouteTable',
	{
      "VpcId" : { "Ref" : vpc_fb }
	}
	)
)

cft.resources.add(Resource('APISUBNET1', 'AWS::EC2::Subnet',
	{
      "AvailabilityZone" : az1,
      "CidrBlock" : api_subnet1,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "APISUBNET1"} ]	,
      "VpcId" : { "Ref" : vpc_fb }	 
	}
	)
)

cft.resources.add(Resource('APISUBNET2', 'AWS::EC2::Subnet',
	{
      "AvailabilityZone" : az2,
      "CidrBlock" : api_subnet2,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "APISUBNET2"} ]	,
      "VpcId" : { "Ref" : vpc_fb }	 
	}
	)
)

cft.resources.add(Resource('APISUBNET3', 'AWS::EC2::Subnet',
	{
      "AvailabilityZone" : az3,
      "CidrBlock" : api_subnet3,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "APISUBNET3"} ]	,
      "VpcId" : { "Ref" : vpc_fb }	 
	}
	)
)

cft.resources.add(Resource('ApiSubnetRouteAssociation1', 'AWS::EC2::SubnetRouteTableAssociation',
		{
			"RouteTableId": { "Ref": stack_name + 'RouteTable' },
	        "SubnetId": { "Ref": "APISUBNET1" }
		}
	)
)

cft.resources.add(Resource('ApiSubnetRouteAssociation2', 'AWS::EC2::SubnetRouteTableAssociation',
		{
			"RouteTableId": { "Ref": stack_name + 'RouteTable' },
	        "SubnetId": { "Ref": "APISUBNET2" }
		}
	)
)

cft.resources.add(Resource('ApiSubnetRouteAssociation3', 'AWS::EC2::SubnetRouteTableAssociation',
		{
			"RouteTableId": { "Ref": stack_name + 'RouteTable' },
	        "SubnetId": { "Ref": "APISUBNET3" }
		}
	)
)

# cft.resources.add(Resource('DBSubnetGrp', 'AWS::RDS::DBSubnetGroup',
# 	{
#         "SubnetIds": [
#           {
#             "Ref": "DatabaseSubnetGroup1"
#           },
#           {
#             "Ref": "DatabaseSubnetGroup2"
#           },
#           {
#             "Ref": "DatabaseSubnetGroup3"
#           }
#         ]
# 	}
# 	)
# )

#This variable will be used for other applications as well
fb_ec2_role = {
        "AssumeRolePolicyDocument": {
          "Statement": [
            {
              "Action": [
                "sts:AssumeRole"
              ],
              "Effect": "Allow",
              "Principal": {
                "Service": "ec2.amazonaws.com"
              }
            }
          ],
          "Version": "2012-10-17"
        },
        "Path": "/",
        "Policies": [
          {
            "PolicyDocument": {
              "Statement": [
                {
                  "Action": [
                    "cloudwatch:GetMetricStatistics",
                    "cloudwatch:ListMetrics",
                    "cloudwatch:PutMetricData",
                    "ec2:DescribeTags"
                  ],
                  "Effect": "Allow",
                  "Resource": "*"
                }
              ],
              "Version": "2012-10-17"
            },
            "PolicyName": "IamRolePolicy0"
          },
          {
            "PolicyDocument": {
              "Statement": [
                {
                  "Action": [
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:DescribeLogGroups",
                    "logs:PutLogEvents",
                    "logs:DescribeLogStreams"
                  ],
                  "Effect": "Allow",
                  "Resource": "arn:aws:logs:*:*:*"
                }
              ],
              "Version": "2012-10-17"
            },
            "PolicyName": "IamRolePolicy2"
          },
          {
            "PolicyDocument": {
              "Statement": [
                {
                  "Action": [
                    "s3:GetObject",
                    "s3:ListBucket"
                  ],
                  "Effect": "Allow",
                  "Resource": [
                    "arn:aws:s3:::flybits-artifacts",
                    "arn:aws:s3:::flybits-artifacts/*"
                  ]
                }
              ],
              "Version": "2012-10-17"
            },
            "PolicyName": "IamRolePolicy3"
          }
    ]
}

cft.resources.add(Resource('APIEC2ROLE', 'AWS::IAM::Role',
		fb_ec2_role
	)
)

cft.resources.add(Resource('APIinstancePROFILE', 'AWS::IAM::InstanceProfile',
	{
		"Path": "/",
        "Roles": [
          {
            "Ref": "APIEC2ROLE"
          }
        ]
	}
  )
)

api_asg_attributes = [
    Metadata(
        {
        "AWS::CloudFormation::Authentication": {
           "S3AccessCreds": {
             "roleName": {
               "Ref": "APIEC2ROLE"
               },
            "type": "s3"
          }
        },
        "AWS::CloudFormation::Init": {
                "config": {
                    "sources": {},
                    "commands": api_json_commands_data,
                    "files": api_json_files_data,
                    "services": api_json_services_data
                }
            }
        }
    ),
	UpdatePolicy(
		{
	        "AutoScalingRollingUpdate": {
	        "MaxBatchSize": 1,
	        "MinInstancesInService": 1,
	        "PauseTime": "PT60S"
        	}		
		}
	)    
]

api_asg_properties = {
	"AvailabilityZones": [ az1, 
						   az2, 
						   az3 
						 ],
    "HealthCheckGracePeriod": 600,
    "HealthCheckType": "ELB",
    "LaunchConfigurationName": {
      "Ref": stack_name + "APILaunch"
    },
    "LoadBalancerNames": [
      {
        "Ref": stack_name + "APIELB"
      }
    ],
    "MaxSize": api_asg_max,
    "MinSize": api_asg_min,
    "Tags": [
      {
        "Key": "Name",
        "PropagateAtLaunch": 'true',
        "Value": stack_name + "ApiApplicationAutoScalingGroup"
      }
    ],
    "VPCZoneIdentifier": [
      { "Ref": "APISUBNET1" },
      { "Ref": "APISUBNET2" },
      { "Ref": "APISUBNET3" }
    ]
}

cft.resources.add(
	  Resource(stack_name + 'APIasg', 'AWS::AutoScaling::AutoScalingGroup' ,api_asg_properties, api_asg_attributes)
)

cft.resources.add(Resource('WebSecurityGroup', 'AWS::EC2::SecurityGroup',
		{
	        "GroupDescription": "SecurityGroup",
	        "SecurityGroupIngress": [
	          {
	            "FromPort": 80,
	            "IpProtocol": 6,
	            "CidrIp": "0.0.0.0/0",
	            "ToPort": 80
	          },
	          {
	            "FromPort": 443,
	            "IpProtocol": 6,
	            "CidrIp": "0.0.0.0/0",
	            "ToPort": 443
	          },
	          {
	            "CidrIp": rc4_subnet,
	            "FromPort": 3389,
	            "IpProtocol": 6,
	            "ToPort": 3389
	          }
	        ],
	        "Tags": [ {"Key": "Name", "Value": "WebSecurityGroup"}],
	        "VpcId": { "Ref" : vpc_fb }
		}
	)
)

cft.resources.add(Resource(stack_name + "APILaunch", 'AWS::AutoScaling::LaunchConfiguration',
		{
	        "AssociatePublicIpAddress": 'true',
	        "BlockDeviceMappings": [
	          {
	            "DeviceName": "/dev/sda1",
	            "Ebs": { "VolumeSize": vol_size }
	          }
	        ],
	        "EbsOptimized": 'false',
	        "IamInstanceProfile": { "Ref": "APIinstancePROFILE" },
	        "ImageId": api_ami,
	        "InstanceMonitoring": 'true',
	        "InstanceType": api_instance_type,
	        "KeyName": fb_key,
	        "SecurityGroups": [ { "Ref": "WebSecurityGroup" } ],
	        "UserData": {
	          "Fn::Base64": {
	            "Fn::Join": [
	              "",
	              [
	                "<powershell>\ncfn-init.exe -v -s \"",
	                {
	                  "Ref": "AWS::StackName"
	                },
	                "\" -r \"",
	                stack_name + 'APIasg',
	                "\" --region \"",
	                {
	                  "Ref": "AWS::Region"
	                },
	                "\"\n</powershell>\n"
	              ]
	            ]
	          }
	        }			
		}
	)
)

cft.resources.add(Resource(stack_name + 'APIELB', 'AWS::ElasticLoadBalancing::LoadBalancer', {
	        "HealthCheck": {
	          "HealthyThreshold": 5,
	          "Interval": 60,
            "Target": "TCP:" + str(elb_health_port),
	          # "Target": "HTTP:80/ping",
	          "Timeout": 59,
	          "UnhealthyThreshold": 5
	        },
	        "Listeners": [
	          {
	            "InstancePort": 443,
	            "InstanceProtocol": elb_protocol,
	            "LoadBalancerPort": 80,
	            "Protocol": elb_protocol
	          },
	          {
	            "InstancePort": 443,
	            "InstanceProtocol": elb_protocol,
	            "LoadBalancerPort": 443,
              "Protocol": elb_protocol
	            # "Protocol": "HTTPS",
	            # "SSLCertificateId": cert_arn
	          }
	        ],
	        "Scheme": "internet-facing",
	        "SecurityGroups": [ { "Ref": "WebSecurityGroup" } ],
	        "Subnets": [
			    { "Ref": "APISUBNET1" },
			    { "Ref": "APISUBNET2" },
			    { "Ref": "APISUBNET3" }
	        ],
	        	"Tags": [ {"Key": "Name", "Value": stack_name + "APIELB"}]
		}
	)
)

cft.resources.add(Resource('ApiScaleInAlarm', 'AWS::CloudWatch::Alarm',
  {
        "AlarmActions": [ { "Ref": "ApiScaleInPolicy" } ],
        "ComparisonOperator": "LessThanOrEqualToThreshold",
        "Dimensions": [ { "Name": "AutoScalingGroupName", "Value": {"Ref": stack_name + "APIasg"}}],
        "EvaluationPeriods": 5,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Period": 60,
        "Statistic": "Average",
        "Threshold": 30,
        "Unit": "Percent"
  }
  )
)

cft.resources.add(Resource('ApiScaleInPolicy', 'AWS::AutoScaling::ScalingPolicy',
  {
        "AdjustmentType": "ChangeInCapacity",
        "AutoScalingGroupName": { "Ref": stack_name + "APIasg" },
        "Cooldown": 300,
        "ScalingAdjustment": -1
  }
  )
)

cft.resources.add(Resource('ApiScaleOutAlarm', 'AWS::CloudWatch::Alarm',
  {
        "AlarmActions": [ { "Ref": "ApiScaleOutPolicy" } ],
        "ComparisonOperator": "GreaterThanThreshold",
        "Dimensions": [ { "Name": "AutoScalingGroupName", "Value": {"Ref": stack_name + "APIasg"}}],
        "EvaluationPeriods": 5,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Period": 60,
        "Statistic": "Average",
        "Threshold": 50,
        "Unit": "Percent"
  }
  )
)

cft.resources.add(Resource('ApiScaleOutPolicy', 'AWS::AutoScaling::ScalingPolicy',
  {
        "AdjustmentType": "ChangeInCapacity",
        "AutoScalingGroupName": { "Ref": stack_name + "APIasg" },
        "Cooldown": 300,
        "ScalingAdjustment": 1
  }
  )
)

##################### Dev Portal Part ###########################
cft.resources.add(Resource('DevPortalSUBNET1', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az1,
      "CidrBlock" : devportal_subnet1,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "DevPortalSUBNET1"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('DevPortalSUBNET2', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az2,
      "CidrBlock" : devportal_subnet2,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "DevPortalSUBNET2"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('DevPortalSUBNET3', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az3,
      "CidrBlock" : devportal_subnet3,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "DevPortalSUBNET3"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('devportalSubnetRouteAssociation1', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "DevPortalSUBNET1" }
    }
  )
)

cft.resources.add(Resource('devportalSubnetRouteAssociation2', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "DevPortalSUBNET2" }
    }
  )
)

cft.resources.add(Resource('devportalSubnetRouteAssociation3', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "DevPortalSUBNET3" }
    }
  )
)

cft.resources.add(Resource('DevPortalEC2ROLE', 'AWS::IAM::Role',
    fb_ec2_role
  )
)

cft.resources.add(Resource('DevPortalinstancePROFILE', 'AWS::IAM::InstanceProfile',
  {
    "Path": "/",
        "Roles": [
          {
            "Ref": "DevPortalEC2ROLE"
          }
        ]
  }
  )
)

devportal_asg_attributes = [
    Metadata(
        {
        "AWS::CloudFormation::Authentication": {
           "S3AccessCreds": {
             "roleName": {
               "Ref": "DevPortalEC2ROLE"
               },
            "type": "s3"
          }
        },
        "AWS::CloudFormation::Init": {
                "config": {
                    "sources": {},
                    "commands": dev_json_commands_data,
                    "files":  dev_json_files_data,
                    "services": api_json_services_data
                }
            }
        }
    ),
  UpdatePolicy(
    {
          "AutoScalingRollingUpdate": {
          "MaxBatchSize": 1,
          "MinInstancesInService": 1,
          "PauseTime": "PT60S"
          }   
    }
  )    
]

devportal_asg_properties = {
  "AvailabilityZones": [ az1, 
               az2, 
               az3 
             ],
    "HealthCheckGracePeriod": 600,
    "HealthCheckType": "ELB",
    "LaunchConfigurationName": {
      "Ref": stack_name + "DevPortalLaunch"
    },
    "LoadBalancerNames": [
      {
        "Ref": stack_name + "DevPortalELB"
      }
    ],
    "MaxSize": devportal_asg_max,
    "MinSize": devportal_asg_min,
    "Tags": [
      {
        "Key": "Name",
        "PropagateAtLaunch": 'true',
        "Value": stack_name + "devportalApplicationAutoScalingGroup"
      }
    ],
    "VPCZoneIdentifier": [
      { "Ref": "DevPortalSUBNET1" },
      { "Ref": "DevPortalSUBNET2" },
      { "Ref": "DevPortalSUBNET3" }
    ]
}

cft.resources.add(
    Resource(stack_name + 'DevPortalasg', 'AWS::AutoScaling::AutoScalingGroup' ,devportal_asg_properties, devportal_asg_attributes)
)

cft.resources.add(Resource(stack_name + "DevPortalLaunch", 'AWS::AutoScaling::LaunchConfiguration',
    {
          "AssociatePublicIpAddress": 'true',
          "BlockDeviceMappings": [
            {
              "DeviceName": "/dev/sda1",
              "Ebs": { "VolumeSize": vol_size }
            }
          ],
          "EbsOptimized": 'false',
          "IamInstanceProfile": { "Ref": "DevPortalinstancePROFILE" },
          "ImageId": devportal_ami,
          "InstanceMonitoring": 'true',
          "InstanceType": devportal_instance_type,
          "KeyName": fb_key,
          "SecurityGroups": [ { "Ref": "WebSecurityGroup" } ],
          "UserData": {
            "Fn::Base64": {
              "Fn::Join": [
                "",
                [
                  "<powershell>\ncfn-init.exe -v -s \"",
                  {
                    "Ref": "AWS::StackName"
                  },
                  "\" -r \"",
                  stack_name + 'DevPortalasg',
                  "\" --region \"",
                  {
                    "Ref": "AWS::Region"
                  },
                  "\"\n</powershell>\n"
                ]
              ]
            }
          }     
    }
  )
)

cft.resources.add(Resource(stack_name + 'DevPortalELB', 'AWS::ElasticLoadBalancing::LoadBalancer', {
          "HealthCheck": {
            "HealthyThreshold": 5,
            "Interval": 60,
            "Target": "TCP:" + str(elb_health_port),
            # "Target": "HTTP:80/ping",
            "Timeout": 59,
            "UnhealthyThreshold": 5
          },
          "Listeners": [
            {
              "InstancePort": 443,
              "InstanceProtocol": elb_protocol,
              "LoadBalancerPort": 80,
              "Protocol": elb_protocol
            },
            {
              "InstancePort": 443,
              "InstanceProtocol": elb_protocol,
              "LoadBalancerPort": 443,
              "Protocol": elb_protocol
              # "Protocol": "HTTPS",
              # "SSLCertificateId": cert_arn
            }
          ],
          "Scheme": "internet-facing",
          "SecurityGroups": [ { "Ref": "WebSecurityGroup" } ],
          "Subnets": [
          { "Ref": "DevPortalSUBNET1" },
          { "Ref": "DevPortalSUBNET2" },
          { "Ref": "DevPortalSUBNET3" }
          ],
            "Tags": [ {"Key": "Name", "Value": stack_name + "DevPortalELB"}]
    }
  )
)

cft.resources.add(Resource('DevPortalScaleInAlarm', 'AWS::CloudWatch::Alarm',
  {
        "AlarmActions": [ { "Ref": "DevPortalScaleInPolicy" } ],
        "ComparisonOperator": "LessThanOrEqualToThreshold",
        "Dimensions": [ { "Name": "AutoScalingGroupName", "Value": {"Ref": stack_name + "DevPortalasg"}}],
        "EvaluationPeriods": 5,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Period": 60,
        "Statistic": "Average",
        "Threshold": 30,
        "Unit": "Percent"
  }
  )
)

cft.resources.add(Resource('DevPortalScaleInPolicy', 'AWS::AutoScaling::ScalingPolicy',
  {
        "AdjustmentType": "ChangeInCapacity",
        "AutoScalingGroupName": { "Ref": stack_name + "DevPortalasg" },
        "Cooldown": 300,
        "ScalingAdjustment": -1
  }
  )
)

cft.resources.add(Resource('DevPortalScaleOutAlarm', 'AWS::CloudWatch::Alarm',
  {
        "AlarmActions": [ { "Ref": "DevPortalScaleOutPolicy" } ],
        "ComparisonOperator": "GreaterThanThreshold",
        "Dimensions": [ { "Name": "AutoScalingGroupName", "Value": {"Ref": stack_name + "DevPortalasg"}}],
        "EvaluationPeriods": 5,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Period": 60,
        "Statistic": "Average",
        "Threshold": 50,
        "Unit": "Percent"
  }
  )
)

cft.resources.add(Resource('DevPortalScaleOutPolicy', 'AWS::AutoScaling::ScalingPolicy',
  {
        "AdjustmentType": "ChangeInCapacity",
        "AutoScalingGroupName": { "Ref": stack_name + "DevPortalasg" },
        "Cooldown": 300,
        "ScalingAdjustment": 1
  }
  )
)

########### Staff Portal Section ##############
cft.resources.add(Resource('StaffPortalSUBNET1', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az1,
      "CidrBlock" : staffportal_subnet1,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "StaffPortalSUBNET1"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('StaffPortalSUBNET2', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az2,
      "CidrBlock" : staffportal_subnet2,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "StaffPortalSUBNET2"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('StaffPortalSUBNET3', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az3,
      "CidrBlock" : staffportal_subnet3,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "StaffPortalSUBNET3"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('staffportalSubnetRouteAssociation1', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "StaffPortalSUBNET1" }
    }
  )
)

cft.resources.add(Resource('staffportalSubnetRouteAssociation2', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "StaffPortalSUBNET2" }
    }
  )
)

cft.resources.add(Resource('staffportalSubnetRouteAssociation3', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "StaffPortalSUBNET3" }
    }
  )
)

cft.resources.add(Resource('StaffPortalEC2ROLE', 'AWS::IAM::Role',
    fb_ec2_role
  )
)

cft.resources.add(Resource('StaffPortalinstancePROFILE', 'AWS::IAM::InstanceProfile',
  {
    "Path": "/",
        "Roles": [
          {
            "Ref": "StaffPortalEC2ROLE"
          }
        ]
  }
  )
)

staffportal_asg_attributes = [
    Metadata(
        {
        "AWS::CloudFormation::Authentication": {
           "S3AccessCreds": {
             "roleName": {
               "Ref": "StaffPortalEC2ROLE"
               },
            "type": "s3"
          }
        },
        "AWS::CloudFormation::Init": {
                "config": {
                    "sources": {},
                    "commands": {},
                    "files": staff_json_files_data,
                    "services": api_json_services_data
                }
            }
        }
    ),
  UpdatePolicy(
    {
          "AutoScalingRollingUpdate": {
          "MaxBatchSize": 1,
          "MinInstancesInService": 1,
          "PauseTime": "PT60S"
          }   
    }
  )    
]

staffportal_asg_properties = {
  "AvailabilityZones": [ az1, 
               az2, 
               az3 
             ],
    "HealthCheckGracePeriod": 600,
    "HealthCheckType": "ELB",
    "LaunchConfigurationName": {
      "Ref": stack_name + "StaffPortalLaunch"
    },
    "LoadBalancerNames": [
      {
        "Ref": stack_name + "StaffPortalELB"
      }
    ],
    "MaxSize": staffportal_asg_max,
    "MinSize": staffportal_asg_min,
    "Tags": [
      {
        "Key": "Name",
        "PropagateAtLaunch": 'true',
        "Value": stack_name + "staffportalApplicationAutoScalingGroup"
      }
    ],
    "VPCZoneIdentifier": [
      { "Ref": "StaffPortalSUBNET1" },
      { "Ref": "StaffPortalSUBNET2" },
      { "Ref": "StaffPortalSUBNET3" }
    ]
}

cft.resources.add(
    Resource(stack_name + 'StaffPortalasg', 'AWS::AutoScaling::AutoScalingGroup' ,staffportal_asg_properties, staffportal_asg_attributes)
)

cft.resources.add(Resource(stack_name + "StaffPortalLaunch", 'AWS::AutoScaling::LaunchConfiguration',
    {
          "AssociatePublicIpAddress": 'true',
          "BlockDeviceMappings": [
            {
              "DeviceName": "/dev/sda1",
              "Ebs": { "VolumeSize": vol_size }
            }
          ],
          "EbsOptimized": 'false',
          "IamInstanceProfile": { "Ref": "StaffPortalinstancePROFILE" },
          "ImageId": staffportal_ami,
          "InstanceMonitoring": 'true',
          "InstanceType": staffportal_instance_type,
          "KeyName": fb_key,
          "SecurityGroups": [ { "Ref": "WebSecurityGroup" } ],
          "UserData": {
            "Fn::Base64": {
              "Fn::Join": [
                "",
                [
                  "<powershell>\ncfn-init.exe -v -s \"",
                  {
                    "Ref": "AWS::StackName"
                  },
                  "\" -r \"",
                  stack_name + 'StaffPortalasg',
                  "\" --region \"",
                  {
                    "Ref": "AWS::Region"
                  },
                  "\"\n</powershell>\n"
                ]
              ]
            }
          }     
    }
  )
)

cft.resources.add(Resource(stack_name + 'StaffPortalELB', 'AWS::ElasticLoadBalancing::LoadBalancer', {
          "HealthCheck": {
            "HealthyThreshold": 5,
            "Interval": 60,
            "Target": "TCP:" + str(elb_health_port),
            # "Target": "HTTP:80/ping",
            "Timeout": 59,
            "UnhealthyThreshold": 5
          },
          "Listeners": [
            {
              "InstancePort": 443,
              "InstanceProtocol": elb_protocol,
              "LoadBalancerPort": 80,
              "Protocol": elb_protocol
            },
            {
              "InstancePort": 443,
              "InstanceProtocol": elb_protocol,
              "LoadBalancerPort": 443,
              "Protocol": elb_protocol
              # "Protocol": "HTTPS",
              # "SSLCertificateId": cert_arn
            }
          ],
          "Scheme": "internet-facing",
          "SecurityGroups": [ { "Ref": "WebSecurityGroup" } ],
          "Subnets": [
          { "Ref": "StaffPortalSUBNET1" },
          { "Ref": "StaffPortalSUBNET2" },
          { "Ref": "StaffPortalSUBNET3" }
          ],
            "Tags": [ {"Key": "Name", "Value": stack_name + "StaffPortalELB"}]
    }
  )
)

cft.resources.add(Resource('StaffPortalScaleInAlarm', 'AWS::CloudWatch::Alarm',
  {
        "AlarmActions": [ { "Ref": "StaffPortalScaleInPolicy" } ],
        "ComparisonOperator": "LessThanOrEqualToThreshold",
        "Dimensions": [ { "Name": "AutoScalingGroupName", "Value": {"Ref": stack_name + "StaffPortalasg"}}],
        "EvaluationPeriods": 5,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Period": 60,
        "Statistic": "Average",
        "Threshold": 30,
        "Unit": "Percent"
  }
  )
)

cft.resources.add(Resource('StaffPortalScaleInPolicy', 'AWS::AutoScaling::ScalingPolicy',
  {
        "AdjustmentType": "ChangeInCapacity",
        "AutoScalingGroupName": { "Ref": stack_name + "StaffPortalasg" },
        "Cooldown": 300,
        "ScalingAdjustment": -1
  }
  )
)

cft.resources.add(Resource('StaffPortalScaleOutAlarm', 'AWS::CloudWatch::Alarm',
  {
        "AlarmActions": [ { "Ref": "StaffPortalScaleOutPolicy" } ],
        "ComparisonOperator": "GreaterThanThreshold",
        "Dimensions": [ { "Name": "AutoScalingGroupName", "Value": {"Ref": stack_name + "StaffPortalasg"}}],
        "EvaluationPeriods": 5,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Period": 60,
        "Statistic": "Average",
        "Threshold": 50,
        "Unit": "Percent"
  }
  )
)

cft.resources.add(Resource('StaffPortalScaleOutPolicy', 'AWS::AutoScaling::ScalingPolicy',
  {
        "AdjustmentType": "ChangeInCapacity",
        "AutoScalingGroupName": { "Ref": stack_name + "StaffPortalasg" },
        "Cooldown": 300,
        "ScalingAdjustment": 1
  }
  )
)

################# Moments Server Section ###################
cft.resources.add(Resource('MomentsSUBNET1', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az1,
      "CidrBlock" : moments_subnet1,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "MomentsSUBNET1"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('MomentsSUBNET2', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az2,
      "CidrBlock" : moments_subnet2,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "MomentsSUBNET2"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('MomentsSUBNET3', 'AWS::EC2::Subnet',
  {
      "AvailabilityZone" : az3,
      "CidrBlock" : moments_subnet3,
      "MapPublicIpOnLaunch" : 'true',
      "Tags" : [ {"Key" : "Name", "Value" : stack_name + "MomentsSUBNET3"} ]  ,
      "VpcId" : { "Ref" : vpc_fb }   
  }
  )
)

cft.resources.add(Resource('momentsSubnetRouteAssociation1', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "MomentsSUBNET1" }
    }
  )
)

cft.resources.add(Resource('momentsSubnetRouteAssociation2', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "MomentsSUBNET2" }
    }
  )
)

cft.resources.add(Resource('momentsSubnetRouteAssociation3', 'AWS::EC2::SubnetRouteTableAssociation',
    {
      "RouteTableId": { "Ref": stack_name + 'RouteTable' },
          "SubnetId": { "Ref": "MomentsSUBNET3" }
    }
  )
)

cft.resources.add(Resource('MomentsEC2ROLE', 'AWS::IAM::Role',
    fb_ec2_role
  )
)

cft.resources.add(Resource('MomentsinstancePROFILE', 'AWS::IAM::InstanceProfile',
  {
    "Path": "/",
        "Roles": [
          {
            "Ref": "MomentsEC2ROLE"
          }
        ]
  }
  )
)

moments_asg_attributes = [
    Metadata(
        {
        "AWS::CloudFormation::Authentication": {
           "S3AccessCreds": {
             "roleName": {
               "Ref": "MomentsEC2ROLE"
               },
            "type": "s3"
          }
        },
        "AWS::CloudFormation::Init": {
                "config": {
                    "sources": {},
                    "commands": {},
                    "files": {},
                    "services": api_json_services_data
                }
            }
        }
    ),
  UpdatePolicy(
    {
          "AutoScalingRollingUpdate": {
          "MaxBatchSize": 1,
          "MinInstancesInService": 1,
          "PauseTime": "PT60S"
          }   
    }
  )    
]

moments_asg_properties = {
  "AvailabilityZones": [ az1, 
               az2, 
               az3 
             ],
    "HealthCheckGracePeriod": 600,
    "HealthCheckType": "ELB",
    "LaunchConfigurationName": {
      "Ref": stack_name + "MomentsLaunch"
    },
    "LoadBalancerNames": [
      {
        "Ref": stack_name + "MomentsELB"
      }
    ],
    "MaxSize": moments_asg_max,
    "MinSize": moments_asg_min,
    "Tags": [
      {
        "Key": "Name",
        "PropagateAtLaunch": 'true',
        "Value": stack_name + "momentsApplicationAutoScalingGroup"
      }
    ],
    "VPCZoneIdentifier": [
      { "Ref": "MomentsSUBNET1" },
      { "Ref": "MomentsSUBNET2" },
      { "Ref": "MomentsSUBNET3" }
    ]
}

cft.resources.add(
    Resource(stack_name + 'Momentsasg', 'AWS::AutoScaling::AutoScalingGroup' ,moments_asg_properties, moments_asg_attributes)
)

cft.resources.add(Resource(stack_name + "MomentsLaunch", 'AWS::AutoScaling::LaunchConfiguration',
    {
          "AssociatePublicIpAddress": 'true',
          "BlockDeviceMappings": [
            {
              "DeviceName": "/dev/sda1",
              "Ebs": { "VolumeSize": vol_size }
            }
          ],
          "EbsOptimized": 'false',
          "IamInstanceProfile": { "Ref": "MomentsinstancePROFILE" },
          "ImageId": moments_ami,
          "InstanceMonitoring": 'true',
          "InstanceType": moments_instance_type,
          "KeyName": fb_key,
          "SecurityGroups": [ { "Ref": "WebSecurityGroup" } ],
          "UserData": {
            "Fn::Base64": {
              "Fn::Join": [
                "",
                [
                  "<powershell>\ncfn-init.exe -v -s \"",
                  {
                    "Ref": "AWS::StackName"
                  },
                  "\" -r \"",
                  stack_name + 'Momentsasg',
                  "\" --region \"",
                  {
                    "Ref": "AWS::Region"
                  },
                  "\"\n</powershell>\n"
                ]
              ]
            }
          }     
    }
  )
)

cft.resources.add(Resource(stack_name + 'MomentsELB', 'AWS::ElasticLoadBalancing::LoadBalancer', {
          "HealthCheck": {
            "HealthyThreshold": 5,
            "Interval": 60,
            "Target": "TCP:" + str(elb_health_port) ,
            # "Target": "HTTP:80/ping",
            "Timeout": 59,
            "UnhealthyThreshold": 5
          },
          "Listeners": [
            {
              "InstancePort": 443,
              "InstanceProtocol": elb_protocol,
              "LoadBalancerPort": 80,
              "Protocol": elb_protocol
            },
            {
              "InstancePort": 443,
              "InstanceProtocol": elb_protocol,
              "LoadBalancerPort": 443,
              "Protocol": elb_protocol
              # "Protocol": "HTTPS",
              # "SSLCertificateId": cert_arn
            }
          ],
          "Scheme": "internet-facing",
          "SecurityGroups": [ { "Ref": "WebSecurityGroup" } ],
          "Subnets": [
          { "Ref": "MomentsSUBNET1" },
          { "Ref": "MomentsSUBNET2" },
          { "Ref": "MomentsSUBNET3" }
          ],
            "Tags": [ {"Key": "Name", "Value": stack_name + "MomentsELB"}]
    }
  )
)

cft.resources.add(Resource('MomentsScaleInAlarm', 'AWS::CloudWatch::Alarm',
  {
        "AlarmActions": [ { "Ref": "MomentsScaleInPolicy" } ],
        "ComparisonOperator": "LessThanOrEqualToThreshold",
        "Dimensions": [ { "Name": "AutoScalingGroupName", "Value": {"Ref": stack_name + "Momentsasg"}}],
        "EvaluationPeriods": 5,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Period": 60,
        "Statistic": "Average",
        "Threshold": 30,
        "Unit": "Percent"
  }
  )
)

cft.resources.add(Resource('MomentsScaleInPolicy', 'AWS::AutoScaling::ScalingPolicy',
  {
        "AdjustmentType": "ChangeInCapacity",
        "AutoScalingGroupName": { "Ref": stack_name + "Momentsasg" },
        "Cooldown": 300,
        "ScalingAdjustment": -1
  }
  )
)

cft.resources.add(Resource('MomentsScaleOutAlarm', 'AWS::CloudWatch::Alarm',
  {
        "AlarmActions": [ { "Ref": "MomentsScaleOutPolicy" } ],
        "ComparisonOperator": "GreaterThanThreshold",
        "Dimensions": [ { "Name": "AutoScalingGroupName", "Value": {"Ref": stack_name + "Momentsasg"}}],
        "EvaluationPeriods": 5,
        "MetricName": "CPUUtilization",
        "Namespace": "AWS/EC2",
        "Period": 60,
        "Statistic": "Average",
        "Threshold": 50,
        "Unit": "Percent"
  }
  )
)

cft.resources.add(Resource('MomentsScaleOutPolicy', 'AWS::AutoScaling::ScalingPolicy',
  {
        "AdjustmentType": "ChangeInCapacity",
        "AutoScalingGroupName": { "Ref": stack_name + "Momentsasg" },
        "Cooldown": 300,
        "ScalingAdjustment": 1
  }
  )
)

