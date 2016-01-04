_default_sqs_access_policy_01 = {"name":"AmazonSQSSendMessage",
                                 "policy_content":"""{"Version": "2012-10-17",
                                                   "Statement": [{"Action":["sqs:SendMessage",
                                                                            "sqs:GetQueueUrl"],
                                                                  "Effect": "Allow",
                                                                  "Resource": "arn:aws:sqs:*"}]}"""}
_default_sqs_access_policy_02 = {"name":"AmazonSQSReceiveMessage",
                                 "policy_content":"""{"Version": "2012-10-17",
                                                   "Statement": [{"Action":["sqs:ReceiveMessage",
                                                                            "sqs:DeleteMessage",
                                                                            "sqs:GetQueueUrl"],
                                                                  "Effect": "Allow",
                                                                  "Resource": "arn:aws:sqs:*"}]}"""}

default_SQS_IAM_policies = [_default_sqs_access_policy_01, _default_sqs_access_policy_02]


_default_sqs_user_01 = {"name":"sqs_publisher",
                        "iam_policy":"AmazonSQSSendMessage"}

_default_sqs_user_02 = {"name":"sqs_subscriber",
                        "iam_policy":"AmazonSQSReceiveMessage"}

default_SQS_Users = [_default_sqs_user_01, _default_sqs_user_02]



def createDefaultSQSPolicies(client):
    try:
        for policy in default_SQS_IAM_policies:
            # Fail if policy exists
            policy_list = client.list_policies()
            for existing_policy in policy_list['Policies']:
                if existing_policy['PolicyName'] == policy['name']:
                    return False

            # Create policy
            response = client.create_policy(PolicyName=policy['name'],
                                            PolicyDocument=str(policy['policy_content']))

            policy['arn'] = response['Policy']['Arn']

        return True

    except:
        return False


def createDefaultSQSUsers(client, attach_policies=True):
    try:
        for user in default_SQS_Users:
            # Fail if user exists
            user_list = client.list_users()
            for existing_user in user_list['Users']:
                if existing_user['UserName'] == user['name']:
                    return False

            # Create user
            client.create_user(UserName=user['name'])

            # Attach policy
            if attach_policies is True:
                policies = client.list_policies()
                for policy in policies['Policies']:
                    if policy['PolicyName'] == user['iam_policy']:
                        client.attach_user_policy(UserName=user['name'], PolicyArn=policy['Arn'])

        return True

    except:
        return False
