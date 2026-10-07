# dns_app — Dante Pruitt, CSE3300 Lab 3
US (8080/tcp), FS (9090/tcp), AS (53533/udp)
Build: docker build -t danterpruitt/us:latest US 
Build: docker build -t danterpruitt/fs:latest FS 
Build: docker build -t danterpruitt/as:latest AS

Extra credit: kubectl apply -f deploy_dns.yml
