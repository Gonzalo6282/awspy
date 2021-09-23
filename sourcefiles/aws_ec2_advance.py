"""
Grep VPCID and subnet Id
Create security group
create Ec2 instance using security group
"""
import boto3
from botocore.exceptions import ClientError

class CreateInstanceEc2(object):
    def __init__(self, ec2_client):
        self.ec2_client = ec2_client
        
    def grep_vpc_subnet_id(self):
        vpc_id = ''
        response = self.ec2_client.describe_vpcs()
        
        for vpc in response['Vpcs']:
            if vpc['Tags'][0]['Value'].__contains__('Default'):
                vpc_id = vpc['VpcId']
                break
            print('The default VPC', vpc_id) 
            response = self.ec2_client.describe_subnets(Filters = [{'Name': 'vpc-id', 'Values': [vpc_id]}]) 
            subnet_id = response['Subnets'][0]['SubnetId']   
            print('The default VPC Subnet Id', subnet_id) 
            return vpc_id, subnet_id
        
    def create_security_group(self):
        sg_name = 'awspy_security_goup'
        try:
            vpc_id, subnet_id = self.grep_vpc_subnet_id()
            response = self.ec2_client.create_security_group(
                GroupName = sg_name,
                Description = 'This SG is created using Python',
                VpcId = vpc_id   
            )
            sg_id = response['GroupId']
            sg_config = self.ec2_client.authorize_security_group_ingress(
                GroupId = sg_id,
                IpPermissions = [
                    {
                    'IpProtocol':'top',
                    'FromPort':22,
                    'ToPort':22,
                    'IpRanges':[{'CirdIp':'0.0.0.0/0'}]
                    }    
                ]   
            )  
            return sg_id, sg_name  
        except Exception as e:
            if str(e).__contains__('already exists'):
                response = self.ec2_client.describe_security_groups(GroupNames= [sg_name])
                print(response)
                sg_id = response['SecurityGroups'][0]['GroupId']
                print(sg_id,sg_name)
                return sg_id, sg_name  
                
    def create_ec2_instance(self):
        vpc_id, subnet_id = self.grep_vpc_subnet_id()
        sg_id, sg_name = self.create_security_group()
        print('Creating Ec2 instance')
        self.ec2_client.run_instances(
            ImageId = 'ami-08e0ca9924195beba',
            MinCount = 1,
            MaxCount = 1,
            IntanceType = 't2.micro',
            KeyName = 'ec2-key',
            SecurityGroupIds = [sg_id],
            SubnetId = subnet_id
        )
        
                                                          
    
# Executions start here
try:
    ec2_client = boto3.client('ec2')
    call_obj = CreateInstanceEc2(ec2_client)
    call_obj.grep_vpc_subnet_id()  
    call_obj.create_security_group()
    call_obj.create_ec2_instance()
    
except  ClientError as e:
    print (e)
