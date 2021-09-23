 import boto3
 
 # Create Ec2
 
def create_ec2_instance():
    try:
        print('Creating Ec2 instance')
        resource_ec2 = boto3.client('ec2')
        resource_ec2.run_instances(
            ImageId = 'ami-08e0ca9924195beba',
            MinCount = 1,
            MaxCount = 1,
            IntanceType = 't2.micro',
            KeyName = 'ec2-key'
        )
    except  Exception as e:
        print(e)
        
        
def describe_ec2_instance():
    try:
        print('Describing Ec2 instance')
        resource_ec2 = boto3.client('ec2')
        print(resource_ec2.describe_ec2_instances["Reservations"][0]["Instances"][0]["InstanceId"]) 
        return str(resource_ec2.describe_ec2_instances()['Reservations'][0]['Instances'][0]['InstanceId'])
        
    except Exception as e:
        print(e)
        
def reboot_ec2_instance():
    try:
        print('Reboot Ec2 instance')
        instance_id = describe_ec2_instance()
        resource_ec2 = boto3.client('ec2')
        print(resource_ec2.stop_instances(InstanceIds=[instance_id]))
        
    except Exception as e:
        print(e)
        
        
def stop_ec2_instance():
    try:
        print('Stop Ec2 instance')
        instance_id = describe_ec2_instance()
        resource_ec2 = boto3.client('ec2')
        print(resource_ec2.reboot_instances(InstanceIds=[instance_id]))
        
    except Exception as e:
        print(e)
        
def start_ec2_instance():
    try:
        print('Start Ec2 instance')
        instance_id = describe_ec2_instance()
        resource_ec2 = boto3.client('ec2')
        print(resource_ec2.start_instances(InstanceIds=[instance_id]))
        
    except Exception as e:
        print(e)
        
def terminate_ec2_instance():
    try:
        print('Terminate Ec2 instance')
        instance_id = describe_ec2_instance()
        resource_ec2 = boto3.client('ec2')
        print(resource_ec2.terminate_instances(InstanceIds=[instance_id]))
        
    except Exception as e:
        print(e)        

#create_ec2_instance()
#describe_ec2_instance()
#reboot_ec2_instance()
#stop_ec2_instance()
#start_ec2_instance()
#terminate_ec2_instance()
