# Installing Elasticsearch on macOS - Direct Installation

Direct installation method by downloading and configuring Elasticsearch manually.

**Prerequisites:**
- macOS (Intel or Apple Silicon)
- Java 11 or higher (OpenJDK or Oracle JDK)
- Terminal access
- ~2GB free disk space

---

## 📥 Download Elasticsearch

### Step 1: Download the macOS Binary

Go to [Elasticsearch Downloads](https://www.elastic.co/downloads/elasticsearch) and select macOS.

#### Option A: Using Command Line

```bash
# Create installation directory
mkdir -p ~/elasticsearch
cd ~/elasticsearch

# Download latest version (as of 2024)
# For Apple Silicon (M1/M2/M3)
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.0-darwin-aarch64.tar.gz

# For Intel Mac
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.0-darwin-x86_64.tar.gz

# Or use wget if available
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.0-darwin-aarch64.tar.gz
```

#### Option B: Web Browser

1. Visit https://www.elastic.co/downloads/elasticsearch
2. Select your OS (macOS)
3. Choose your architecture (Apple Silicon or Intel)
4. Click download button
5. Save to `~/elasticsearch` folder

### Step 2: Verify Download

```bash
# Check downloaded file
ls -lh ~/elasticsearch/elasticsearch-*.tar.gz

# Verify checksum (optional but recommended)
# Download the SHA512 file from the same location
shasum -a 512 -c elasticsearch-8.10.0-darwin-aarch64.tar.gz.sha512
```

---

## 📦 Extract and Install

### Step 1: Extract the Archive

```bash
cd ~/elasticsearch

# Extract the downloaded file
tar -xzf elasticsearch-8.10.0-darwin-aarch64.tar.gz

# Navigate to installation directory
cd elasticsearch-8.10.0

# Check the structure
ls -la
```

### Step 2: Directory Structure

```
elasticsearch-8.10.0/
├── bin/              # Executable files
├── config/           # Configuration files
├── lib/              # Java libraries
├── modules/          # Built-in modules
├── plugins/          # Plugin directory
├── LICENSE.txt
├── README.md
└── NOTICE.txt
```

---

## ▶️ Start Elasticsearch

### Method 1: Run in Foreground (Shows Logs)

```bash
# Navigate to Elasticsearch directory
cd ~/elasticsearch/elasticsearch-8.10.0

# Start Elasticsearch
./bin/elasticsearch

# You should see output like:
# ╔═════════════════════════════════════════════════════════════════════╗
# ║  WARNING: no JVM found on this system. Elasticsearch requires Java  ║
# │  11 or newer to run. Please download and install a JDK.            ║
# ╚═════════════════════════════════════════════════════════════════════╝

# OR if Java is installed:
# ╔═════════════════════════════════════════════════════════════════════╗
# ║  Elasticsearch built-in security features are enabled and configured║
# │  ...                                                                 ║
# │  -> created temporary folder at /var/folders/...                    ║
# │  -> mode [basic] - valid license required for additional features   ║
# │  ...                                                                 ║
# ╚═════════════════════════════════════════════════════════════════════╝
```

### Method 2: Run in Background

```bash
# Navigate to Elasticsearch directory
cd ~/elasticsearch/elasticsearch-8.10.0

# Start in background
./bin/elasticsearch &

# Or using nohup to keep running after terminal closes
nohup ./bin/elasticsearch > elasticsearch.log 2>&1 &

# Check if running
ps aux | grep elasticsearch
```

### Method 3: Create Alias for Easy Starting

```bash
# Add to your shell profile (~/.zshrc or ~/.bash_profile)
echo 'alias es-start="~/elasticsearch/elasticsearch-8.10.0/bin/elasticsearch"' >> ~/.zshrc

# Reload shell configuration
source ~/.zshrc

# Now you can start with just:
es-start
```

---

## ✅ Verify Installation

### Test Connection

```bash
# Wait 5-10 seconds for Elasticsearch to fully start

# Test basic connectivity
curl http://localhost:9200

# Expected response (without authentication if security is disabled):
# {
#   "name" : "your-machine-name",
#   "cluster_name" : "elasticsearch",
#   "cluster_uuid" : "...",
#   "version" : {
#     "number" : "8.10.0",
#     ...
#   },
#   ...
# }
```

### Pretty Print with jq

```bash
# Install jq if needed
brew install jq

# Pretty print the response
curl -s http://localhost:9200 | jq '.'

# Check cluster health
curl -s http://localhost:9200/_cluster/health | jq '.'
```

---

## 🔧 Configuration

### Configuration File Location

```bash
# Open configuration file
nano ~/elasticsearch/elasticsearch-8.10.0/config/elasticsearch.yml
```

### Important Configuration Options

```yaml
# Cluster name (must match on all nodes)
cluster.name: my-cluster

# Node name (unique for each node)
node.name: node-1

# Data directory
path.data: ./data

# Log directory
path.logs: ./logs

# Network binding
network.host: localhost
http.port: 9200

# Discovery settings (for single node)
discovery.type: single-node

# Security settings (Elasticsearch 8.0+)
xpack.security.enabled: false
```

### Apply Changes

```bash
# Stop Elasticsearch (Ctrl+C if running in foreground)
# Or kill the process
pkill -f elasticsearch

# Edit config
nano ~/elasticsearch/elasticsearch-8.10.0/config/elasticsearch.yml

# Restart
./bin/elasticsearch
```

---

## 🔐 Security (Elasticsearch 8.0+)

### Initial Security Setup

On first run, Elasticsearch generates:
- Temporary password for elastic user
- Enrollment token for new nodes

```
Security information
- All of the following credentials are generated fresh for this Elasticsearch instance and are unique.
- elastic password: [PASSWORD_HERE]
- Password for the 'kibana_system' user automatically generated:
- Enrollment token:
```

**Save these credentials!** They're shown only once.

### Disable Security (For Local Development Only)

```bash
# Edit config
nano ~/elasticsearch/elasticsearch-8.10.0/config/elasticsearch.yml

# Add or modify:
xpack.security.enabled: false
xpack.security.enrollment.enabled: false

# Restart Elasticsearch
```

### Set Elasticsearch Password

```bash
# If security is enabled
cd ~/elasticsearch/elasticsearch-8.10.0

# Reset elastic user password
./bin/elasticsearch-reset-password -u elastic

# Output:
# Password for the [elastic] user successfully reset.
# New value: [NEW_PASSWORD]
```

---

## 📝 Logging and Monitoring

### View Logs

```bash
# If running in foreground, logs display in terminal
# If running in background:

tail -f ~/elasticsearch/elasticsearch-8.10.0/logs/elasticsearch.log

# View last 50 lines
tail -50 ~/elasticsearch/elasticsearch-8.10.0/logs/elasticsearch.log

# Search for errors
grep ERROR ~/elasticsearch/elasticsearch-8.10.0/logs/elasticsearch.log
```

### Check Cluster Status

```bash
# Cluster health
curl http://localhost:9200/_cluster/health | jq '.'

# Node info
curl http://localhost:9200/_nodes | jq '.nodes'

# Indices info
curl http://localhost:9200/_cat/indices
```

---

## 🛑 Stop Elasticsearch

### If Running in Foreground

```bash
# Press Ctrl+C in the terminal
# Elasticsearch will shut down gracefully
```

### If Running in Background

```bash
# Find the process
ps aux | grep elasticsearch

# Kill by PID
kill -15 <PID>

# Or use pkill
pkill -f elasticsearch

# Force kill if necessary
pkill -9 -f elasticsearch
```

### Graceful Shutdown via API

```bash
curl -X POST "localhost:9200/_shutdown"
```

---

## 🚨 Troubleshooting

### Java Not Installed

```bash
# Check Java version
java -version

# If not installed, install Java
brew install java

# Add to PATH if needed
echo 'export PATH="/Library/Java/JavaVirtualMachines/openjdk-11.jdk/Contents/Home/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Port 9200 Already in Use

```bash
# Find process using port 9200
lsof -i :9200

# Kill the process
kill -9 <PID>

# Or use different port in config:
# http.port: 9201
```

### Elasticsearch Crashes on Startup

```bash
# Check logs for errors
tail -100 ~/elasticsearch/elasticsearch-8.10.0/logs/elasticsearch.log

# Common issues:
# 1. Not enough memory - increase heap size
# 2. Invalid configuration - check config file syntax
# 3. Port conflicts - change http.port
```

### Out of Memory Errors

```bash
# Edit JVM configuration
nano ~/elasticsearch/elasticsearch-8.10.0/config/jvm.options

# Look for these lines and adjust:
# -Xms1g  (initial heap size)
# -Xmx1g  (maximum heap size)

# For example, to allocate 2GB:
# -Xms2g
# -Xmx2g
```

### Connection Refused

```bash
# Make sure Elasticsearch is running
ps aux | grep elasticsearch

# Check if port is listening
lsof -i :9200

# Try connecting with verbose output
curl -v http://localhost:9200

# Check firewall
# System Preferences > Security & Privacy > Firewall
```

---

## 📊 Memory and Performance

### Check Current Memory Allocation

```bash
# View JVM settings
cat ~/elasticsearch/elasticsearch-8.10.0/config/jvm.options | grep "^-Xm"
```

### Adjust Memory (Important!)

```bash
# Edit JVM options
nano ~/elasticsearch/elasticsearch-8.10.0/config/jvm.options

# Find and modify:
# -Xms512m  (increase if needed, e.g., -Xms2g)
# -Xmx512m  (increase if needed, e.g., -Xmx2g)

# Rule of thumb: Set both to same value, ~50% of system RAM
# For 16GB system: -Xms8g and -Xmx8g
# For 8GB system: -Xms4g and -Xmx4g
# For 4GB system: -Xms2g and -Xmx2g
```

### Check System Memory

```bash
# View available RAM on Mac
system_profiler SPHardwareDataType | grep "Memory:"

# Or using vm_stat
vm_stat
```

---

## 🔄 Uninstall

### Complete Removal

```bash
# Stop Elasticsearch (if running)
pkill -f elasticsearch

# Remove installation directory
rm -rf ~/elasticsearch

# Remove any data files
rm -rf ~/elasticsearch-data

# Remove from aliases (if added)
# Edit ~/.zshrc or ~/.bash_profile and remove elasticsearch alias
```

---

## 📚 Next Steps

1. ✅ Elasticsearch installed and running
2. → Verify with `curl http://localhost:9200`
3. → Check [SETUP.md](SETUP.md) for indexing data
4. → Install Kibana for GUI (optional)
5. → Create indices and index documents

---

## 🔗 Related Files

- [INSTALL_ELASTICSEARCH_BREW.md](INSTALL_ELASTICSEARCH_BREW.md) - Homebrew installation
- [SETUP.md](SETUP.md) - Complete setup guide
- [README.md](README.md) - Project overview

---

## 📖 Official Resources

- [Elasticsearch Official Downloads](https://www.elastic.co/downloads/elasticsearch)
- [Elasticsearch macOS Installation](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
- [Elasticsearch Configuration](https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html)
- [Java Version Support](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html)

---

## ❓ FAQ

**Q: What's the difference between direct and Homebrew installation?**
- **Direct:** More control, easier to manage multiple versions
- **Homebrew:** Simpler installation, easier updates, integrated with system

**Q: How much memory does Elasticsearch need?**
- Minimum: 512MB heap size
- Recommended for local dev: 2GB
- Production: 50% of available RAM (up to 31GB)

**Q: Can I run multiple Elasticsearch instances?**
Yes, just use different ports and data directories.

**Q: Is this good for production?**
No, for production use Docker, Kubernetes, or Elasticsearch Cloud.

**Q: How do I upgrade Elasticsearch?**
1. Download new version
2. Stop current instance
3. Backup data
4. Replace with new version
5. Restart

**Q: Where is my data stored?**
By default in `./data` relative to Elasticsearch directory.
