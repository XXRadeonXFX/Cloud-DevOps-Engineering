### Docker Networking 

Docker networking enables containers to communicate with each other, the host machine, and external networks. It uses Linux kernel features like namespaces for isolation, bridges for virtual networks, and NAT for external access. Containers can make outbound connections by default; inbound requires port publishing.

#### Key Concepts
- **Network Namespace**: Each container gets its own isolated network stack (interfaces, routing table, etc.).
- **Default Behavior**: Containers on the same user-defined network can communicate via container names (built-in DNS).
- **Commands**:
  - `docker network ls`: List networks.
  - `docker network create <name> --driver <driver>`: Create a network.
  - `docker network inspect <name>`: View details.
  - `docker run --network <name>`: Attach container to network.












#### Main Network Drivers Comparison

| Driver    | Scope     | Isolation                          | Use Case                                      | Key Features/Notes                          |
|-----------|-----------|------------------------------------|-----------------------------------------------|---------------------------------------------|
| **Bridge** (default) | Single host | Containers isolated from host; communicate on same bridge | Multi-container apps on one host (e.g., web + DB) | User-defined bridges support name resolution; default bridge is limited. |
| **Host**  | Single host | No isolation (shares host network) | Performance-critical apps (e.g., monitoring, proxies) | Direct host ports; no port mapping needed. |
| **None**  | Single host | Complete isolation                 | Tasks needing no network (e.g., batch jobs, security) | Only loopback interface. |
| **Overlay** | Multi-host | Isolated across hosts              | Swarm/Kubernetes clusters; multi-host communication | Uses VXLAN; supports encryption and service discovery. |
| **Macvlan** | Single host | Minimal (direct physical access)   | Legacy apps needing own MAC/IP on LAN         | Containers appear as physical devices; no host communication by default. |
| **IPvlan** (advanced) | Single host | Layer 3 control                    | VLAN routing scenarios                        | Shares parent MAC; focuses on IP routing. |












#### Docker Compose Networking
- By default, Compose creates a bridge network for the project.
- Services communicate using service names as hostnames.
- Custom networks: Define under `networks:` top-level key.
- Example diagram of multi-service setup:

