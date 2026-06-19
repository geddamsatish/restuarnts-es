# Installing Elasticsearch on macOS using Homebrew

Quick and easy Elasticsearch installation using Homebrew package manager.

**Prerequisites:**
- macOS (Intel or Apple Silicon)
- Homebrew installed
- Terminal access

---

## 📦 Installation Steps

### Step 1: Add Elastic Homebrew Tap

```bash
brew tap elastic/tap
```

This adds the official Elastic repository to Homebrew.

### Step 2: Install Elasticsearch

#### Option A: Latest Stable Version

```bash
brew install elastic/tap/elasticsearch-full
```

#### Option B: Specific Version

```bash
# Install a specific version (e.g., 8.10.0)
brew install elastic/tap/elasticsearch-full@8.10
```

### Step 3: Start Elasticsearch

#### Option A: Start as a Service (Recommended)

```bash
# Start Elasticsearch service
brew services start elastic/tap/elasticsearch-full

# Stop the service
brew services stop elastic/tap/elasticsearch-full

# Restart the service
brew services restart elastic/tap/elasticsearch-full

# Check service status
brew services list
```

#### Option B: Start Manually

```bash
# Start in foreground (shows logs)
elasticsearch

# Start in background
elasticsearch &
```

### Step 4: Verify Installation

```bash
# Wait a few seconds for Elasticsearch to start, then test:
curl http://localhost:9200

# Expected response:
# {
#   "name" : "your-machine-name",
#   "cluster_name" : "elasticsearch",
#   "cluster_uuid" : "...",
#   "version" : {
#     "number" : "8.10.0",
#     "build_flavor" : "default",
#     "build_type" : "tar",
#     "build_hash" : "...",
#     "build_date" : "...",
#     "build_snapshot" : false,
#     "lucene_version" : "9.7.0",
#     "minimum_wire_compatibility_version" : "7.17.0",
#     "minimum_index_compatibility_version" : "7.0.0"
#   },
#   ...
# }
```

---

## ✅ Verify Installation with jq (Pretty Print)

If you have `jq` installed, get a cleaner output:

```bash
# Install jq (if needed)
brew install jq

# Test Elasticsearch with formatted output
curl -s http://localhost:9200 | jq '.'
```

---

## 🔧 Configuration

### View Configuration File

```bash
# Find the config file location
brew info elastic/tap/elasticsearch-full

# Or directly open the config
nano /opt/homebrew/etc/elasticsearch/elasticsearch.yml

# For Intel Macs:
nano /usr/local/etc/elasticsearch/elasticsearch.yml
```

### Common Configuration Changes

#### 1. Change Cluster Name

```yaml
# /opt/homebrew/etc/elasticsearch/elasticsearch.yml
cluster.name: my-cluster
```

#### 2. Change Node Name

```yaml
node.name: node-1
```

#### 3. Change Data Directory

```yaml
path.data: /var/lib/elasticsearch
```

#### 4. Change Log Directory

```yaml
path.logs: /var/log/elasticsearch
```

#### 5. Bind to Different Address

```yaml
# Default is localhost only
network.host: 0.0.0.0
http.port: 9200
```

### Apply Configuration Changes

```bash
# Stop the service
brew services stop elastic/tap/elasticsearch-full

# Edit the config file
nano /opt/homebrew/etc/elasticsearch/elasticsearch.yml

# Start the service again
brew services start elastic/tap/elasticsearch-full
```

---

## 📝 Checking Logs

### View Real-Time Logs

```bash
# For Apple Silicon (M1/M2/M3)
tail -f /opt/homebrew/var/log/elasticsearch/elasticsearch.log

# For Intel Macs
tail -f /usr/local/var/log/elasticsearch/elasticsearch.log
```

### View Error Logs

```bash
# Apple Silicon
grep ERROR /opt/homebrew/var/log/elasticsearch/elasticsearch.log

# Intel Macs
grep ERROR /usr/local/var/log/elasticsearch/elasticsearch.log
```

---

## 🚨 Troubleshooting

### Port 9200 Already in Use

```bash
# Find what's using port 9200
lsof -i :9200

# Kill the process (replace PID with the actual process ID)
kill -9 <PID>

# Or change Elasticsearch port in config
# http.port: 9201
```

### Elasticsearch Won't Start

```bash
# Check logs for errors
tail -50 /opt/homebrew/var/log/elasticsearch/elasticsearch.log

# Check if it's already running
brew services list

# Force stop and start again
brew services stop elastic/tap/elasticsearch-full
brew services start elastic/tap/elasticsearch-full
```

### Connection Refused

```bash
# Check if service is running
brew services list

# Make sure port 9200 is open
curl http://localhost:9200

# If localhost doesn't work, try explicit IP
curl http://127.0.0.1:9200
```

### Check Java Version

```bash
# Elasticsearch requires Java 11+
java -version

# If Java is not installed, Homebrew will install it automatically
# But you can install/upgrade with:
brew install java
```

---

## 🔄 Uninstall Elasticsearch

### Complete Uninstall

```bash
# Stop the service
brew services stop elastic/tap/elasticsearch-full

# Uninstall
brew uninstall elastic/tap/elasticsearch-full

# Remove Homebrew tap (optional)
brew untap elastic/tap

# Remove configuration files (optional, be careful!)
rm -rf /opt/homebrew/etc/elasticsearch
rm -rf /opt/homebrew/var/log/elasticsearch
rm -rf /opt/homebrew/var/lib/elasticsearch
```

---

## 📊 Useful Commands

### Check Installation Path

```bash
# Apple Silicon
ls -la /opt/homebrew/Cellar/elasticsearch-full/

# Intel
ls -la /usr/local/Cellar/elasticsearch-full/
```

### Check Version

```bash
curl -s http://localhost:9200 | jq '.version.number'
```

### List Installed Elasticsearch Versions

```bash
brew list elastic/tap/elasticsearch-full
```

### Upgrade Elasticsearch

```bash
# Update Homebrew
brew update

# Upgrade Elasticsearch
brew upgrade elastic/tap/elasticsearch-full

# Restart service
brew services restart elastic/tap/elasticsearch-full
```

### View Service Status

```bash
# Check if running
brew services list | grep elasticsearch

# Detailed status
brew services info elastic/tap/elasticsearch-full
```

---

## 🔐 Security Notes

### Default Security Settings (Elasticsearch 8.0+)

By default, Elasticsearch 8.0+ comes with security enabled:

```bash
# Check if security is enabled
curl http://localhost:9200/_xpack/security

# You may need authentication
# The initial password is printed during first installation
```

### Disable Security (For Local Development Only)

```bash
# Edit configuration
nano /opt/homebrew/etc/elasticsearch/elasticsearch.yml

# Add these lines:
xpack.security.enabled: false
xpack.security.enrollment.enabled: false

# Restart
brew services restart elastic/tap/elasticsearch-full
```

---

## 📚 Next Steps

1. ✅ Elasticsearch is installed and running
2. → Create indices: `curl -X PUT http://localhost:9200/my-index`
3. → Index documents: Use Kibana or APIs
4. → Install Kibana (optional): `brew install elastic/tap/kibana-full`
5. → Check [SETUP.md](SETUP.md) for data indexing

---

## 🔗 Related Files

- [INSTALL_ELASTICSEARCH_DIRECT.md](INSTALL_ELASTICSEARCH_DIRECT.md) - Direct installation method
- [SETUP.md](../guides/SETUP.md) - Complete setup guide
- [README.md](../../README.md) - Project overview

---

## 📖 Official Resources

- [Elasticsearch Official Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Elasticsearch macOS Installation Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
- [Homebrew Elasticsearch Tap](https://github.com/elastic/homebrew-tap)

---

## ❓ FAQ

**Q: How do I know if Elasticsearch is running?**
```bash
brew services list
# or
curl http://localhost:9200
```

**Q: Where are my data files stored?**
```bash
# Apple Silicon
/opt/homebrew/var/lib/elasticsearch/

# Intel
/usr/local/var/lib/elasticsearch/
```

**Q: How do I upgrade Elasticsearch?**
```bash
brew update
brew upgrade elastic/tap/elasticsearch-full
brew services restart elastic/tap/elasticsearch-full
```

**Q: Can I run multiple Elasticsearch instances?**
Yes, but you need to configure different ports and data directories in the config files.

**Q: Is Homebrew installation good for production?**
No, Homebrew is recommended for local development only. For production, use official Docker images or binary installations.
