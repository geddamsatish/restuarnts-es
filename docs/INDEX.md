# Documentation Index

Complete documentation for the Elasticsearch Restaurants & Ramayana project.

## 📚 Getting Started

- **[README.md](../README.md)** - Project overview and quick start
- **[installation/README.md](installation/README.md)** - Choose your Elasticsearch installation method

## 🛠️ Installation Guides

### [installation/](installation/)

- **[INSTALL_ELASTICSEARCH.md](installation/INSTALL_ELASTICSEARCH.md)** ⭐ **Start here**
  - Compare Homebrew vs Direct installation
  - System requirements checklist
  - Decision tree to choose your method

- **[INSTALL_ELASTICSEARCH_BREW.md](installation/INSTALL_ELASTICSEARCH_BREW.md)**
  - Quick & easy Homebrew installation
  - Perfect for beginners
  - Automatic updates and service management

- **[INSTALL_ELASTICSEARCH_DIRECT.md](installation/INSTALL_ELASTICSEARCH_DIRECT.md)**
  - Full control direct installation
  - For advanced users
  - Multiple versions support

## 📖 Setup & Configuration

### [guides/](guides/)

- **[SETUP.md](guides/SETUP.md)**
  - Complete post-installation setup
  - Create indices with schema
  - Convert and index data
  - Verify installation

## 🔍 Dataset Documentation

### Restaurants Dataset
- **[restaurants/README.md](../restaurants/README.md)**
  - Schema and field descriptions
  - 8+ sample queries
  - Common use cases
  - Troubleshooting

### Ramayana Dataset
- **[ramayana/README.md](../ramayana/README.md)**
  - Schema and field descriptions
  - 10+ sample queries
  - Kanda (book) navigation
  - Common use cases

## 📋 Quick Navigation

### By Task

**I want to install Elasticsearch**
→ [installation/INSTALL_ELASTICSEARCH.md](installation/INSTALL_ELASTICSEARCH.md)

**I want to set up the project**
→ [guides/SETUP.md](guides/SETUP.md)

**I want to query restaurants**
→ [restaurants/README.md](../restaurants/README.md)

**I want to query Ramayana**
→ [ramayana/README.md](../ramayana/README.md)

**I need help with a specific issue**
→ See troubleshooting sections in respective guides

## 📊 File Structure

```
docs/
├── INDEX.md (this file)
├── installation/
│   ├── INSTALL_ELASTICSEARCH.md (Decision guide)
│   ├── INSTALL_ELASTICSEARCH_BREW.md (Easy method)
│   └── INSTALL_ELASTICSEARCH_DIRECT.md (Advanced method)
└── guides/
    └── SETUP.md (Post-installation)

restaurants/
├── README.md (Complete guide)
├── restaurants_converter.py
├── schema.json
├── sample_queries.sh
└── data/
    ├── Bengaluru_Restaurants.csv
    └── README.md

ramayana/
├── README.md (Complete guide)
├── ramayana_converter.py
├── schema.json
├── sample_queries.sh
└── data/
    ├── ramayana.json
    └── README.md
```

## 🔗 External Resources

- [Elasticsearch Official Docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)
- [Elasticsearch Query DSL](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html)
- [Elasticsearch on GitHub](https://github.com/elastic/elasticsearch)

---

**📖 [Back to README](../README.md)**
