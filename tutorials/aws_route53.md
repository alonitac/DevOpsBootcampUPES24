# The DNS Protocol

IP addresses are somewhat hard to remember. 
Names are much easier. google.com is much easier to remember than 16.42.0.9 but there must be some mechanism to convert the network names into an IP address.

## Route53

Amazon Route 53 is a scalable and highly available DNS web service that offers domain registration services and allows you to manage your domain by configuring DNS settings such as routing traffic to different endpoints. 

> [!NOTE]
> [Read here](networking_dns.md) about how the DNS protocol works

### Registering a domain 

Throughout the bootcamp, you'll be using a real registered domain to manage and access the services that you'll deploy in the cloud.

We've already registered a domain that will be shared by all students: `devops-days-upes.com`.
 

### Add records to registered domain

When registered your domain, Route 53 created a **Hosted Zone**. 

A hosted zone in Amazon Route 53 is a container for DNS records associated with a domain, effectively acting as the **authoritative server** for that domain.
It enables you to manage how traffic is routed to your resources by defining various record types, such as A and CNAME records.

1. In the navigation pane, choose **Hosted zones**\.

2. Choose the hosted zone associated our domain: `devops-days-upes.com`.

3. Choose **Create record**\.

4. Define an `A record` for a custom sub-domain of yours (e.g. `my-name.devops-days-upes.com`), the record value is an IP address of your EC2 instance created in a previous tutorial[^1]. 

5. Choose **Create records**\.   
   **Note**  
   Your new records take time to propagate to the Route 53 DNS servers.



[aws_route_53_dns]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/aws_route_53_dns.png


[^1]: EC2 instance deployed in [Intro to cloud computing](aws_intro.md).