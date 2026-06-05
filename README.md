# ddns-ipv64

This is a DDNS Updater for the free DynDNS service [IPv64.net](https://ipv64.net/).
This project was completely ported to Python and is heavily inspired by [alcapone1933/docker-ddns-ipv64](https://github.com/alcapone1933/docker-ddns-ipv64).

It periodically checks for IPv4 and IPv6 address changes and updates your A/AAAA records on ipv64.net.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Configuration

The configuration is managed via TOML files located in the `config/` directory.

### 1. Copy Settings and Secrets

First, copy the example configuration files to create your own local active configuration:

```bash
cp config/settings.example.toml config/settings.toml
cp config/.secrets.example.toml config/.secrets.toml
```

### 2. Get Secrets from IPv64

To authenticate with the IPv64 API, you need your Domain Key or Account Update Token:
1. Log in to your account at [https://ipv64.net/dyndns](https://ipv64.net/dyndns).
2. Look for the **Account Update Token** or the specific **Domain Key** (e.g., `1234567890abcdefghijklmnopqrstuvwxyz`).

Edit `config/.secrets.toml` and insert your token:

```toml
[api]
key = "your_actual_domain_key_here"
```

### 3. Configure the Project

Edit `config/settings.toml` to define your domain settings and service behavior:

```toml
[service]
update_interval = 15
max_updates = 5
rate_limit_window = 60
dry_run = false # Change to false to enable actual IP updates
user_agent = "ddns-ipv64/0.0.1 (https://github.com/Strice91/ddns-ipv64)"

[api]
baseurl = "https://ipv64.net/nic/update"
domain = "your-domain.ipv64.net" # Change to your actual domain
prefix = "" # Set a prefix (subdomain) if needed, e.g., "ddns"
```

*Note: The `prefix` is optional and corresponds to the subdomain you have set up in ipv64.net. If you use multiple domains separated by commas, the same prefix applies to all.*

### Settings Variables

Here is a complete list of the variables you can configure in `settings.toml`:

| Section | Variable | Default | Description |
| ------- | -------- | ------- | ----------- |
| `[service]` | `update_interval` | `15` | Interval in minutes between IP checks. |
| `[service]` | `max_updates` | `5` | Maximum number of updates allowed within the rate limit window. |
| `[service]` | `rate_limit_window` | `60` | Time window in minutes for rate limiting (prevents abuse). |
| `[service]` | `dry_run` | `true` | If true, simulates the API calls. Change to `false` to actually update records. |
| `[service]` | `user_agent` | `"ddns-ipv64/0.0.1..."` | The HTTP User-Agent string sent during requests to the IPv64 API. |
| `[api]` | `baseurl` | `"https://ipv64.net/nic/update"` | The IPv64 DDNS API endpoint. |
| `[api]` | `domain` | `"deine-domain.ipv64.net"` | Your domain or domains (comma-separated) registered at IPv64. |
| `[api]` | `prefix` | `""` | Optional subdomain prefix (e.g., `ddns`). Applies to all domains. |
| `[logging]` | `level` | `"DEBUG"` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). |
| `[network]` | `nameserver` | `"ns1.ipv64.net"` | The nameserver used to verify current DNS records for your domain. |
| `[network]` | `ipv4_sources` | `[list of URLs]` | Fallback list of services used to query your current public IPv4 address. |
| `[network]` | `ipv6_sources` | `[list of URLs]` | Fallback list of services used to query your current public IPv6 address. |

## Starting the Container

Once you have configured both `settings.toml` and `.secrets.toml`, you can start the Docker container in the background using Docker Compose:

```bash
docker compose up -d
```

To view the logs and ensure the updater is working properly:

```bash
docker compose logs -f
```

To stop the container:

```bash
docker compose down
```