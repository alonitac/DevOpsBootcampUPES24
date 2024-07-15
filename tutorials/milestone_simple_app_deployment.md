# Simple app deployment

For this milestone, you will manually deploy the [NetflixMovieCatalog][NetflixMovieCatalog] service on an AWS virtual machine.

1. In an AWS account, create an EC2 instance.
2. Run the NetflixMovieCatalog within your instance as a Linux service[^1] that starts automatically when the instance is starting. Create Python venv and install dependencies if needed. 
3. In Route 53, configure a subdomain in the hosted zone of your domain to route traffic your instance IP.
4. Access the service domain via your browser and make sure it's accessible.


[NetflixMovieCatalog]: https://github.com/exit-zero-academy/NetflixMovieCatalog.git

[^1]: Linux services discussed [here](linux_processes.md#services)