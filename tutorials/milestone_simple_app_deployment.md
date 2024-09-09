# Manual app deployment

In this tutorial, you will manually deploy the [NetflixMovieCatalog][NetflixMovieCatalog] service on an AWS virtual machine.

![][deployment_diagram]

1. In an AWS account, create an EC2 instance (if haven't done yet).
2. Run the NetflixMovieCatalog within your instance as a Linux service[^1] that starts automatically when the instance is starting. Create Python `venv` and install dependencies if needed.
3. In Route 53, configure a subdomain in the hosted zone of your domain to route traffic your instance IP.
4. Access the service domain via your browser and make sure it's accessible, [open relevant port in your instance's Security Group](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-security-group-rules.html). 
5. Now, configure your Flask application to accept **only HTTPS traffic** by generating a self-signed certificate:
   ```bash
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
   ```
   
   Then, update the Flask app code to use the certificate, as follows:

   ```diff
   - app.run(port=8080, host='0.0.0.0')
   + app.run(port=8080, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
   ```
   
   While `cert.pem` and `key.pem` are paths to your generated certificate and private key. 
6. Visit your service via your browser by: `https://your-subdomain.devops-days-upes.com:8080` (change `your-subdomain` accordingly).


[NetflixMovieCatalog]: https://github.com/exit-zero-academy/NetflixMovieCatalog.git
[deployment_diagram]: https://alonitac.github.io/DevOpsBootcampUPES24/img/deployment_diagram.png

[^1]: Linux services discussed [here](linux_processes.md#services)