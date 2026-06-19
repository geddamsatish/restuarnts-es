# Elasticsearch Installation Guide

Complete guide to installing Elasticsearch on macOS. Choose your preferred installation method.

---

## 🚀 Quick Comparison

| Method | Ease | Control | Maintenance | Best For |
|--------|------|---------|-------------|----------|
| **Homebrew** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | Local dev, beginners |
| **Direct** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Multiple versions, control |

---

## 📋 Installation Methods

### 🍺 Method 1: Using Homebrew (Recommended for Beginners)

**Pros:**
- ✅ Simplest installation
- ✅ Automatic updates with `brew upgrade`
- ✅ Integrated with macOS
- ✅ Easy service management
- ✅ Automatic Java installation

**Cons:**
- ❌ Less control over configuration
- ❌ Only one version at a time

**👉 [Complete Homebrew Installation Guide](INSTALL_ELASTICSEARCH_BREW.md)**

**Quick Start:**
```bash
brew tap elastic/tap
brew install elastic/tap/elasticsearch-full
brew services start elastic/tap/elasticsearch-full
curl http://localhost:9200
```

---

### 📥 Method 2: Direct Installation (Recommended for Control)

**Pros:**
- ✅ Full control over installation
- ✅ Can run multiple versions simultaneously
- ✅ Easy to manage configuration
- ✅ Can move installation anywhere
- ✅ Clear understanding of file structure

**Cons:**
- ❌ More manual steps
- ❌ Manual Java installation
- ❌ Manual updates required

**👉 [Complete Direct Installation Guide](INSTALL_ELASTICSEARCH_DIRECT.md)**

**Quick Start:**
```bash
mkdir -p ~/elasticsearch
cd ~/elasticsearch
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.0-darwin-aarch64.tar.gz
tar -xzf elasticsearch-8.10.0-darwin-aarch64.tar.gz
cd elasticsearch-8.10.0
./bin/elasticsearch
```

---

## 🎯 Which Method Should I Choose?

### Choose **Homebrew** if you:
- Are new to Elasticsearch
- Want the easiest setup
- Don't need multiple versions
- Want automatic updates
- Are using Elasticsearch for local development

### Choose **Direct Installation** if you:
- Want full control over installation
- Need to run multiple Elasticsearch versions
- Want to customize everything
- Are testing different configurations
- Have specific networking requirements

---

## ✅ System Requirements

### Hardware
- **CPU:** 2+ cores (4+ recommended)
- **RAM:** 4GB minimum (8GB+ recommended)
- **Disk:** 2GB for installation + space for data

### Software
- **macOS:** 10.12+
- **Java:** OpenJDK 11+ or Oracle JDK 11+
- **Terminal:** bash or zsh

### Check Your System

```bash
# Check macOS version
sw_vers

# Check Java installation
java -version

# Check available RAM
system_profiler SPHardwareDataType | grep "Memory:"

# Check available disk space
df -h
```

---

## 🔧 Pre-Installation Steps (Both Methods)

### 1. Install Java (if needed)

```bash
# Check if Java is installed
java -version

# If not installed:
brew install java

# Verify installation
java -version
```

### 2. Create Directory for Elasticsearch

```bash
# Create directory
mkdir -p ~/elasticsearch
cd ~/elasticsearch
```

### 3. Install jq (Optional, but Recommended)

```bash
# jq makes viewing JSON responses easier
brew install jq

# Usage:
curl -s http://localhost:9200 | jq '.'
```

---

## 📝 Installation Decision Tree

```
Do you want the easiest setup?
├─ YES → Use Homebrew [INSTALL_ELASTICSEARCH_BREW.md](INSTALL_ELASTICSEARCH_BREW.md)
└─ NO  → Do you need multiple versions?
         ├─ YES → Use Direct Installation [INSTALL_ELASTICSEARCH_DIRECT.md](INSTALL_ELASTICSEARCH_DIRECT.md)
         └─ NO  → Use Homebrew (it's still simpler)
```

---

## ✨ Post-Installation Checklist

After installation, verify everything works:

```bash
# 1. Check Elasticsearch is running
curl http://localhost:9200

# 2. Check cluster health
curl http://localhost:9200/_cluster/health | jq '.'

# 3. List indices (should be empty initially)
curl http://localhost:9200/_cat/indices

# 4. Create a test index
curl -X PUT http://localhost:9200/test-index

# 5. Verify index was created
curl http://localhost:9200/_cat/indices

# 6. Delete test index
curl -X DELETE http://localhost:9200/test-index
```

---

## 🚀 Next Steps

After successful installation:

1. **Read Setup Guide:** [SETUP.md](SETUP.md)
2. **Learn Basic Queries:** [README.md](README.md)
3. **Index Restaurant Data:** [restaurants/README.md](restaurants/README.md)
4. **Index Ramayana Data:** [ramayana/README.md](ramayana/README.md)

---

## 🆘 Troubleshooting

### Elasticsearch Won't Start

```bash
# Check if port 9200 is in use
lsof -i :9200

# Check error logs
tail -50 ~/elasticsearch/elasticsearch-8.10.0/logs/elasticsearch.log

# See full guide for your method:
# Homebrew: INSTALL_ELASTICSEARCH_BREW.md
# Direct: INSTALL_ELASTICSEARCH_DIRECT.md
```

### Java Not Found

```bash
# Install Java
brew install java

# Add to PATH if needed
echo 'export PATH="/opt/homebrew/opt/java/libexec/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Need Help?

Refer to the detailed guide for your chosen method:
- **Homebrew Issues:** See [INSTALL_ELASTICSEARCH_BREW.md](INSTALL_ELASTICSEARCH_BREW.md)(INSTALL_ELASTICSEARCH_BREW.md)
- **Direct Issues:** See [INSTALL_ELASTICSEARCH_DIRECT.md](INSTALL_ELASTICSEARCH_DIRECT.md)(INSTALL_ELASTICSEARCH_DIRECT.md)

---

## 📊 Comparison Table: Full Details

| Feature | Homebrew | Direct |
|---------|----------|--------|
| Installation Time | 2-3 minutes | 5-7 minutes |
| Configuration | Automatic | Manual |
| Updates | `brew upgrade` | Manual download |
| Multiple Versions | ❌ No | ✅ Yes |
| Service Management | `brew services` | Manual/Script |
| Uninstall | `brew uninstall` | `rm -rf` |
| File Locations | `/opt/homebrew/` | Any directory |
| Customization | Limited | Full |
| Learning Curve | Easy | Medium |
| Recommended For | Beginners | Advanced |

---

## 🔗 Related Documentation

- [SETUP.md](SETUP.md) - Complete setup after installation
- [README.md](README.md) - Project overview
- [restaurants/README.md](restaurants/README.md) - Restaurant dataset guide
- [ramayana/README.md](ramayana/README.md) - Ramayana dataset guide

---

## 📖 Official Resources

- [Elasticsearch Official Website](https://www.elastic.co/)
- [Elasticsearch Downloads](https://www.elastic.co/downloads/elasticsearch)
- [Elasticsearch Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [System Requirements](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html)
- [Homebrew Elasticsearch Tap](https://github.com/elastic/homebrew-tap)

---

## ❓ Common Questions

**Q: Which installation method is faster?**
A: Homebrew is faster overall (2-3 minutes vs 5-7 minutes).

**Q: Can I switch from Homebrew to Direct Installation?**
A: Yes, just uninstall Homebrew version and install Direct version separately.

**Q: Do I need to configure anything special?**
A: Default configuration works for local development. No special setup needed.

**Q: How do I keep Elasticsearch running after closing Terminal?**
A: With Homebrew, it auto-starts with `brew services start`. With Direct, use `nohup` or create a launch script.

**Q: What if I already have Elasticsearch installed?**
A: You can keep it or upgrade/switch to a new version using the relevant guide.

**Q: Is there a Docker option?**
A: Yes, but it's not covered in this guide. See [Elasticsearch Docker Documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html).

---

## 📞 Support

If you encounter issues:

1. Check the **Troubleshooting** section of your chosen guide
2. Review the **FAQ** section
3. Check official [Elasticsearch Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
4. Check logs: `tail -f <logfile>`

---

**Ready to get started?**
- 👉 [Homebrew Installation](INSTALL_ELASTICSEARCH_BREW.md)
- 👉 [Direct Installation](INSTALL_ELASTICSEARCH_DIRECT.md)
