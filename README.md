# netflow_ddos_mitigation_api
Basic example of scaling netflow collectors behind NGINX load balancer and being able to configure policies based on certain thresholds for ICMP/TCP/UDP traffic and automatically mitigate potential DDoS attacks using nfacctd and exabgp + BGP Flowspec.

The blog can be found at bspendlove.github.io called `Auto DDoS mitigation using BGP Flowspec and Netflow`. This repository holds all the data as per the blog, if you are to use this in production (which I don't advise) then please ensure you change all credentials in the relevant .env files under the `envs` directory. These are lab credentials and are certainly not considered secure.
