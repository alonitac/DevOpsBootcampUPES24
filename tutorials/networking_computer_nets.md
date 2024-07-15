# Computer Networks

## The OSI model

In order to get data over the network, lots of different hard- and software needs to work and communicate together via a well-defined **protocol**.
A protocol is, simply put, a set of rules for communication. You've probably heard some of them: HTTP, SSH, TCP/IP etc...
All these different types of communication protocols are classified in 7 layers, which are known as the Open Systems Interconnection Reference Model, the OSI Model for short.

In this course we will discuss the 4-layer model, which is a simplified version of the OSI model that combines several of the OSI layers into four layers.

This model is commonly used in the TCP/IP protocol suite, which is the basis for the Internet.

The four layers of the TCP/IP model, in order from top to bottom, are:

| Layer Name              | Common used protocols |
|-------------------------|-----------------------|
| Application Layer       | HTTP, DNS, SMTP, SSH  |
| Transport Layer         | TCP, UDP              |
| Network Layer           | IP, ICMP              |
| Network Interface Layer | Ethernet              |

### Visiting google.com in the browser - it's really much more complicated than it looks!

What happen when you open up your web browser and type http://www.google.com/? We will try to examine it in terms of the OSI model.

#### Application layer

The browser uses HTTP protocol to form an HTTP request to Google's servers, to serve Google's home page. 
The HTTP request is merely a text in a well-defined form, it may look like:

```text
GET / HTTP/1.1
Host: google.com
User-Agent: Mozilla/5.0
```

Note that we literally want to transfer this text to Google's servers, as is.
In the server side, there is an application (called "webserver", obviously) that knows what to do and how to response to this text format.
Since web browser and web servers are applications that use the network, it resides in the Application layer.

The **Application layer** is where network applications and their corresponding protocols reside. Network applications may be web-browsers, web-server, mailing software, and every application that send or receive data over the Internet, in any kind and form.

Do your Firefox or Chrome browsers are responsible for the actual data transfer over the Internet? Hell no.
They both use the great service of the **Transport layer**.

#### Transport layer

After your browser formulated an HTTP text message (a.k.a. **HTTP request**), the message is transferred (by writing it to a file of type **socket** - will be discussed later), to another "piece of software" in the Linux kernel which is responsible for **controlling the transmission** of the Application layer messages to the other host.
The Transmission Control Protocol (TCP) forms the [set of rules](https://www.ietf.org/rfc/rfc793.txt) according which the message is being transferred to the other host, or received from another host. 

TCP breaks long **messages** into shorter **segments**, it guarantees that the data was indeed delivered to the destination and controls the order in which segments are being sent.
Note that TCP only controls **how** the data is being sent and received, but it does not responsible for the actual data transfer. 

Besides TCP, there is another common protocol in the Transport layer which is called **UDP**.

- TCP (Transmission Control Protocol): Reliable, connection-oriented, provides a guaranteed delivery of data and error detection mechanisms. 
- UDP (User Datagram Protocol): Lightweight, connectionless, used for fast, low-latency communication. Commonly used for video streaming, online gaming, and other real-time applications.

To send its data, TCP and UDP use the service of a very close friend - **Internet Protocol (IP)**.

#### Internet layer

We continue our journey to get Google.com's homepage. 
So we have a few segments, ready to be transferred to Google's servers. 

The IP protocol is responsible for moving the TCP segments from one host to another.
Just as you would give the postal service a letter with a destination address, IP protocol sends piece of data (a.k.a **Packets**) to an address (a.k.a **IP address**).
Like TCP and UDP, IP is a piece of software resides in the Linux kernel (so close to TCP, that they are frequently called TCP/IP).
In order to send packets over the Internet, IP communicates with a **Network Interface**, which is a software abstraction that represents a network physical (of virtual) device, such as an Ethernet card or a wireless adapter.

The Network layer routes packets through a series of routers between the source and destination hosts.

#### Network Interface layer

The Network Interface layer is the lower level component in our model. 
It provides an interface between the physical network and the higher-level networking protocols.
It handles the transmission and reception of data (a.k.a. **Frames**) over the network, and it is responsible for converting **digital signals** into **analog signals** for transmission over the physical network.

In this layer, every physical (or virtual) network device has a media access control (**MAC**) address, which is a unique identifier assigned to a network interface. 


Computers are often arranged into "groups", known as **Computer Networks**.
All machines under a given network can communicate with each other via different methods and physical devices.

Usually, a given computer network is divided into sub-network, also known as **Subnet**.  

In this tutorial we'll describe and investigate the components of **Computer Networks** and **Subnets**. 

## Subnets

As said, computer networks organize machines into **subnets**.
All machines on a given subnet are connected by a physical device called **switch** or **hub** and may exchange information directly.
Subnets are in turn linked to other subnets by machines acting as **routers**.

![][networking_subnets]

The above network consists of 3 subnets. Taking a closer look, we notice that computers under the same subnet have the same ip prefix.
For example, all computers under the leftmost subnet (and all computers that will join this subnet) have an IP address starting by `10.1.1.xxx`. 
Thus, they share the same **IP** prefix, more precisely, the same first **24 bits** in their IP address.

We will denote the IP boundaries of the leftmost subnet by:

```text
10.1.1.0/24
```

This method is known as **Classless Interdomain Routing (CIDR)**.

The CIDR `10.1.1.0/24` represents a network address in IPv4 format with the network prefix length of 24 bits. This means that the first 24 bits of the IP address, i.e., the first three octets, specify the **network portion**, and the remaining 8 bits, i.e., the fourth octet, represent the **host portion**. 
In this case, the network address is `10.1.1.0`, and there are 256 possible host addresses (2^8 = 256) within this network, ranging from `10.1.1.1` to `10.1.1.254` (the first and last IP addresses are reserved).

Another method to denote network subnet in **subnet mask**.
This format specifies the number of fixed octates of the IP as 255, and the free octates as 0. The equivalent subnet mask for `10.1.1.0/24` is `255.255.255.0`,  which means the first 3 octets are the network portion (fixed) and 4th octet is the hosts portion (change per machine in the subnet).

Use [this nice tool](https://cidr.xyz/) to familiarize yourself with CIDR notation.

The `ping` command can be used to confirm IP connectivity between two hosts:

```console
myuser@10.1.1.1:~$ ping 10.1.2.2
PING 10.1.2.2 56(84) bytes of data.
64 bytes from 10.1.2.2: icmp_seq=1 ttl=51 time=3.29 ms
64 bytes from 10.1.2.2: icmp_seq=2 ttl=51 time=3.27 ms
64 bytes from 10.1.2.2: icmp_seq=3 ttl=51 time=3.28 ms
...
```

In the above example, the computer identified by the IP `10.1.1.1` sends ping frames to `10.1.2.2`.

## IP Address for private subnets

There are three ranges of private IP addresses defined in [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918):

- 10.0.0.0/8
- 172.16.0.0/12
- 192.168.0.0/16

These addresses can be used for internal networks within an organization, but they are not routable on the public Internet.

Public IP addresses, on the other hand, are assigned by Internet authorities and are used to identify devices that are directly accessible from the Internet.

# Exercises

### :pencil2: Non-standard CIDR

Observe the `172.16.0.0/12` CIDR. This is an unconventional CIDR since it doesn't fix the whole octet, but only the first 4 bits of the second octet. Use https://cidr.xyz/ to answer the below questions:

1. How many bits can vary?
2. How many available addresses in this CIDR (host addresses)?
3. What does the 2nd octet bit representation look like?
4. What is the next decimal number in the 2nd octet (after 16?)
5. Is `172.32.0.0` part of the CIDR?


[networking_subnets]: https://exit-zero-academy.github.io/DevOpsTheHardWayAssets/img/networking_subnets.png