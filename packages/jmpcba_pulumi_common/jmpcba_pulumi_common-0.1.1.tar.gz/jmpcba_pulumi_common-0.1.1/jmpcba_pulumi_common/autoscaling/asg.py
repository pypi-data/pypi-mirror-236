import pulumi
from pulumi_aws.autoscaling import Group, GroupLaunchTemplateArgs
from pulumi_aws.ec2 import LaunchTemplate, SecurityGroup, SecurityGroupIngressArgs, SecurityGroupEgressArgs
from pulumi_aws.lb import LoadBalancer
from pulumi_aws.iam import role


class ASGArgs:

    def __init__(self, asg_name: str, azs: [str], instance_profile: role, desired_capacity: int, min_size: int,
                 max_size: int, stack: str, ami: str, instance_type: str, lb_subnet_ids: [str], vpc_id: str):
        self.asg_name = asg_name
        self.azs = azs
        self.instance_profile = instance_profile
        self.desired_capacity = desired_capacity
        self.min_size = min_size
        self.max_size = max_size
        self.stack = stack
        self.ami = ami
        self.instance_type = instance_type
        self.lb_subnet_ids = lb_subnet_ids
        self.vpc_id = vpc_id


class ASG(pulumi.ComponentResource):
    def __init__(self, name, args: ASGArgs, opts=None):
        super().__init__("custom:ec2:ASG", name, {}, opts)

        child_opts = pulumi.ResourceOptions(parent=self)

        self._alb_sg = SecurityGroup(f"{args.stack}-alb_sg",
                                     description=f"{args.stack}-alb_sg",
                                     vpc_id=args.vpc_id,
                                     ingress=[SecurityGroupIngressArgs(
                                         description="TLS internet",
                                         from_port=443,
                                         to_port=443,
                                         protocol="tcp",
                                         cidr_blocks=["0.0.0.0/0", ],
                                     )],
                                     egress=[SecurityGroupEgressArgs(
                                         from_port=0,
                                         to_port=0,
                                         protocol="-1",
                                         cidr_blocks=["0.0.0.0/0"],
                                     )],
                                     tags={
                                         "Name": "allow_tls",
                                     })

        self._asg_sg = SecurityGroup(f"{args.stack}-asg_sg",
                                     description=f"{args.stack}-asg_sg",
                                     vpc_id=args.vpc_id,
                                     ingress=[SecurityGroupIngressArgs(
                                         description="TLS internet",
                                         from_port=443,
                                         to_port=443,
                                         protocol="tcp",
                                         security_groups=[self._alb_sg.id],
                                     )],
                                     egress=[SecurityGroupEgressArgs(
                                         from_port=0,
                                         to_port=0,
                                         protocol="-1",
                                         cidr_blocks=["0.0.0.0/0"],
                                     )],
                                     tags={
                                         "Name": "allow_tls",
                                     })

        self._launch_template = LaunchTemplate(f"{args.stack}Launch_template",
                                               name_prefix=args.stack,
                                               image_id=args.ami,
                                               instance_type=args.instance_type,
                                               iam_instance_profile=args.instance_profile,
                                               vpc_security_group_ids=[self._asg_sg.id])

        self._alb = LoadBalancer(f"{args.stack}-lb",
                                 internal=False,
                                 load_balancer_type="application",
                                 security_groups=self._alb_sg.id,
                                 subnets=args.lb_subnet_ids,
                                 enable_deletion_protection=True,
                                 tags={
                                     "Environment": args.stack,
                                 })

        self._asg = Group(args.asg_name,
                          availability_zones=args.azs,
                          desired_capacity=args.desired_capacity,
                          max_size=args.max_size,
                          min_size=args.min_size,
                          launch_template=GroupLaunchTemplateArgs(id=self._launch_template.id),
                          target_group_arns=[self._alb.arn]
                          )

        self.register_outputs({
            "ALB name": self._alb.name
        })
