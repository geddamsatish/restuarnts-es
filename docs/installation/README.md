# Elasticsearch Installation Guide

Choose your preferred Elasticsearch installation method for macOS.

## 🚀 Quick Comparison

| Aspect | Homebrew | Direct |
|--------|----------|--------|
| **Ease** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Time** | 2-3 min | 5-7 min |
| **Control** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **For Beginners** | ✅ Yes | ❌ No |
| **Multiple Versions** | ❌ No | ✅ Yes |
| **Updates** | Automatic | Manual |

---

## 📋 Which Method Should I Choose?

### Choose **Homebrew** if:
- ✅ You're new to Elasticsearch
- ✅ You want the easiest setup (5 minutes)
- ✅ You're using this for local development
- ✅ You want automatic updates

### Choose **Direct Installation** if:
- ✅ You want full control
- ✅ You need multiple versions
- ✅ You're testing different configurations
- ✅ You prefer understanding everything

---

## 📖 Installation Guides

### 🍺 [Homebrew Installation](INSTALL_ELASTICSEARCH_BREW.md) ⭐ **Recommended**

**Simplest method. Perfect for beginners.**

```bash
brew tap elastic/tap
brew install elastic/tap/elasticsearch-full
brew services start elastic/tap/elasticsearch-full
curl http://localhost:9200
```

Features:
- ✅ Automatic Java installation
- ✅ Service management built-in
- ✅ Automatic startup on boot
- ✅ Easy uninstall

**[Read Full Homebrew Guide](INSTALL_ELASTICSEARCH_BREW.md)**

---

### 📥 [Direct Installation](INSTALL_ELASTICSEARCH_DIRECT.md) **Advanced**

**Full control. For advanced users.**

```bash
mkdir -p ~/elasticsearch && cd ~/elasticsearch
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.10.0-darwin-aarch64.tar.gz
tar -xzf elasticsearch-8.10.0-darwin-aarch64.tar.gz
cd elasticsearch-8.10.0
./bin/elasticsearch
```

Features:
- ✅ Full customization
- ✅ Multiple versions
- ✅ Clear file structure
- ✅ Manual control

**[Read Full Direct Installation Guide](INSTALL_ELASTICSEARCH_DIRECT.md)**

---

## [📋 Detailed Comparison & Decision Tree](INSTALL_ELASTICSEARCH.md)

Comprehensive comparison with system requirements, FAQ, and troubleshooting.

---

## ✅ System Requirements

- **macOS** 10.12+
- **Java** 11+ (installed automatically with Homebrew)
- **RAM** 4GB minimum (8GB+ recommended)
- **Disk** 2GB+ for installation + data

---

## 🔧 Quick Test

After installation, verify it works:

```bash
curl http://localhost:9200 | jq '.'
```

---

## 🚀 Next Steps

1. **Choose a method above** → Homebrew or Direct
2. **Run installation** → Follow the guide
3. **Verify** → Run the test command
4. **Setup project** → [Read SETUP.md](../guides/SETUP.md)
5. **Start querying** → [Read README.md](../../README.md)

---

## ❓ Common Questions

**Q: Which is faster?**
A: Homebrew (2-3 min vs 5-7 min)

**Q: Can I switch later?**
A: Yes, uninstall one and install the other

**Q: Do I need both?**
A: No, choose one method

**Q: What about Docker?**
A: See [Elasticsearch Docker docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)

---

## 📖 Detailed Guides

- **[INSTALL_ELASTICSEARCH.md](INSTALL_ELASTICSEARCH.md)** - Full comparison & requirements
- **[INSTALL_ELASTICSEARCH_BREW.md](INSTALL_ELASTICSEARCH_BREW.md)** - Homebrew method
- **[INSTALL_ELASTICSEARCH_DIRECT.md](INSTALL_ELASTICSEARCH_DIRECT.md)** - Direct method

---

**[← Back to Documentation Index](../INDEX.md)**
