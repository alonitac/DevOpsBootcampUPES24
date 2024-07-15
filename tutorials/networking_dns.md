# How DNS works?

The DNS service is complex.
The protocol that specifies how the DNS servers and querying hosts communicate consisting of a large number of DNS servers distributed around the globe.

A simple design for DNS would have one DNS server that contains all the mappings (which is a bad idea! why?). 

<details>
  <summary>Answer</summary>

- Single point of failure
- High traffic volume
- Distant centralized DB
- Maintenance

</details>

In fact, the DNS is a wonderful example of how a distributed database can be implemented in the Internet. Let's delve into details.
There are three classes of DNS servers: **root** DNS servers, **top-level domain** (TLD) DNS servers, and **authoritative** DNS servers.

![][networking_dns-levels]

- **Root DNS servers** - clients first contacts one of the root servers, which returns IP addresses for TLD servers for the top-level domain. As of 2012, there are 13 root DNS servers (actually 247 after replication).
- **Top-level domain (TLD) servers** - are responsible for top-level domains such as .com, .org, .net, .edu, and .gov, and all of the country top-level domains such as uk, fr etc... Look [here](https://www.iana.org/domains/root/db) for a full list. When client reaches TLD server in order to resolve a domain name, e.g. google.com, it is **not** responded with the desired IP address of the domain, but with a list of Authoritative Servers from which to request the desired IP address.
- **Authoritative DNS servers** - every organization with publicly accessible hosts must provide publicly accessible DNS records that map the names to an IP addresses. Authoritative name servers are the source of truth in the domain name system. An organization can choose to implement its own authoritative DNS server to hold these records, alternatively, to pay to have these records stored in an authoritative DNS server of some service provider, e.g. [AWS route53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/domain-register.html).


## Manually resolving google.com

We will resolve `google.com` step by step using the `dig` command.

2. First, get the list of the root-level DNS servers. You can get it too by:
```shell
dig . NS
```

3. Pick one of the root-level domain names. We will query this server to get the hostname of the *com* top-level domain by:
```shell
dig @<your-chosen-root-level-hostname> com NS
`````

4. Now that we have a list of *.com* TLD servers, pick one of them to query the hostname of the authoritative DNS of *google.com*:
```shell
dig @<your-chosen-TLD-hostname> google.com NS
```

5. Finally, as we know the hostname of the authoritative DNS servers of *google.com*, we can query one of them to retrieve the IP address of *google.com*:

```shell
dig @<your-chosen-authoritative-hostname> google.com A
```

## DNS record types

A resource record is a four-tuple that contains the following fields:

```text
(Name, Value, Type, TTL)
```

Below is common DNS records type

| Type         | Description                                          |
|--------------|------------------------------------------------------|
| A record     | maps a domain name to an IPv4 address.               |
| NS record    | specifies the authoritative DNS servers for a domain |
| CNAME record | maps a domain name to another domain name (alias)    |

## The local DNS server 

![][networking_resolve-google]

In real life, the actual hostname resolve is done by your ISP local DNS serve. 
Every ISP maintains its own local DNS server. When a host connects to an ISP, it provides the IP addresses of its local DNS server(s).
When a host makes a DNS query, the query is sent to the local DNS server, which acts a **proxy**, forwarding the query into the DNS server hierarchy.

The IP address of your local DNS server can be found in `/etc/resolv.conf`.

## DNS caching 

**Caching** is a mechanism used to store frequently accessed data in a local storage (cache) to reduce the time and resources required to retrieve the data from the original source.
When data is requested, it is first checked in the cache, and if it is found there, it is returned quickly without accessing the original source.
If the data is not in the cache, it is retrieved from the original source, stored in the cache, and returned to the requester.
This process can help to improve the performance and scalability of applications by reducing the load on the original data source and minimizing network latency.

When a DNS server receives a DNS record, it can cache the record in its local memory. Thus, the DNS server can provide the desired IP address, even if it is not authoritative for the hostname.
A local DNS server can also cache the IP addresses of TLD servers, thereby allowing the local DNS server to bypass the root DNS servers in a query chain (this often happens).
Because hosts and mappings between hostnames and IP addresses are by no means permanent, DNS servers discard cached information after a period of time, known as **Time to Live (TTL)**.

# Exercises

### :pencil2: Playing more with the `dig` command

Use `dig` to answer the below questions:

1. Resolve the IP address of `stanford.edu`.
2. How much did it take to resolve the query?
3. Resolve `stanford.edu` again, how much did it take now? Why?
4. How can you measure the time passed **between** the first resolution to the second one?
5. How many authoritative servers does `stanford.edu` have?
6. Does the above answer come from the cache of some server rather than from an authoritative Stanford DNS server?


[networking_dns-levels]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/networking_dns-levels.png
[networking_resolve-google]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/networking_resolve-google.png
