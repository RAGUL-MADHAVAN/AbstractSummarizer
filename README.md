# 🤖 GenAI Academic Abstract Summarizer

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![AI](https://img.shields.io/badge/AI-HuggingFace-orange.svg)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An intelligent full-stack web application that leverages state-of-the-art Generative AI to summarize academic abstracts, built with modern Python technologies and production-ready architecture.**

## 🚀 Key Features

### 🎯 **AI-Powered Summarization**
- **Advanced NLP**: Uses Facebook's BART-large-CNN model via Hugging Face Transformers
- **Contextual Understanding**: Generates coherent, semantically accurate summaries
- **Configurable Output**: Adjustable summary length (30-130 tokens) with deterministic results
- **Real-time Processing**: Sub-second inference for academic text analysis

### 🔐 **Enterprise-Grade Security**
- **Secure Authentication**: bcrypt password hashing with salt generation
- **Session Management**: Flask-Login with persistent sessions and auto-logout
- **CSRF Protection**: Flask-WTF integration preventing cross-site request forgery
- **Input Validation**: Comprehensive form validation with WTForms
- **SQL Injection Prevention**: Parameterized queries via SQLAlchemy ORM

### 📊 **Batch Processing & Analytics**
- **CSV Upload Support**: Process hundreds of abstracts simultaneously
- **Downloadable Results**: Export summaries in structured CSV format
- **Progress Tracking**: Real-time batch processing with UUID-based job management
- **User Activity History**: Complete audit trail of all summarization activities
- **Template Downloads**: Pre-formatted CSV templates for easy data preparation

### 🏗️ **Modern Architecture**
- **Blueprint Pattern**: Modular Flask architecture with clean separation of concerns
- **Factory Pattern**: App factory with configurable environments (development/production)
- **ORM Integration**: SQLAlchemy with relationship modeling and migrations
- **Error Handling**: Comprehensive error pages (404/500) with graceful degradation
- **Responsive Design**: Bootstrap 5 UI with mobile-first approach

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | Flask 2.3.3 | Web framework with blueprint architecture |
| **Database** | SQLite + SQLAlchemy | ORM with relationship modeling |
| **AI/ML** | Hugging Face Transformers | BART-large-CNN for summarization |
| **Authentication** | Flask-Login + bcrypt | Secure user management |
| **Forms** | Flask-WTF + WTForms | Secure form handling with validation |
| **Data Processing** | Pandas + NumPy | CSV processing and numerical operations |
| **Frontend** | Bootstrap 5 + Jinja2 | Responsive UI with template inheritance |

## 📈 Performance & Scalability

- **Model Caching**: Singleton pattern loads AI model once at startup
- **Database Optimization**: Indexed queries with lazy loading relationships
- **Memory Management**: Efficient handling of large batch operations
- **Async Ready**: Blueprint architecture supports easy async migration
- **Production Configurable**: Environment-based configuration management

## 🎯 Use Cases

### **Academic Research**
- **Literature Reviews**: Rapid screening of conference papers and journals
- **Research Planning**: Quick assessment of paper relevance and contributions
- **Conference Management**: Automated abstract screening for review committees

### **Industry Applications**
- **Patent Analysis**: Summarization of technical patent abstracts
- **Content Curation**: Automated processing of research publications
- **Knowledge Management**: Intelligent document summarization systems

### **Educational Tools**
- **Student Research**: Assistance with academic paper analysis
- **Teaching Support**: Automated content summarization for course materials
- **Learning Analytics**: Track reading patterns and comprehension

## 🚀 Quick Start

### Prerequisites
- **Python 3.9+**
- **pip package manager**
- **4GB+ RAM** (for AI model loading)
- **2GB+ disk space** (for model storage)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd genai-abstract-summarizer

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -r genai_abstract_summarizer/requirements.txt

# Run the application
python app.py
```

**🌐 Access at:** http://127.0.0.1:5000

### First Run Notes
- AI model downloads automatically (~500MB, may take 3-5 minutes)
- Database initializes automatically with required tables
- Registration required for accessing summarization features

## 📋 API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/login` | GET/POST | User authentication | ❌ |
| `/register` | GET/POST | User registration | ❌ |
| `/summarizer/single` | GET/POST | Single abstract summarization | ✅ |
| `/summarizer/batch` | GET/POST | Batch CSV processing | ✅ |
| `/summarizer/api/summarize` | POST | REST API for summarization | ✅ |
| `/profile` | GET/POST | User profile management | ✅ |
| `/dashboard` | GET | User activity dashboard | ✅ |

## 🔒 Security Features

- **Password Security**: bcrypt hashing with unique salt per user
- **Session Management**: Secure cookie-based sessions with expiration
- **CSRF Protection**: Token-based request validation
- **Input Sanitization**: Comprehensive validation pipeline
- **SQL Injection Prevention**: ORM-based parameterized queries
- **File Upload Security**: Extension validation and secure filename handling

## 📊 Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique, Indexed)
- `email` (Unique, Indexed)
- `password_hash` (bcrypt hashed)
- `bio` (User profile text)
- `member_since` (Registration timestamp)
- `last_seen` (Activity tracking)

### Summaries Table
- `id` (Primary Key)
- `original_text` (Source abstract)
- `summary` (Generated summary)
- `timestamp` (Creation time, Indexed)
- `user_id` (Foreign Key to Users)
- `is_batch` (Processing type flag)
- `batch_id` (UUID for batch grouping)

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** with proper documentation
4. **Add tests** for new functionality
5. **Submit a pull request** with detailed description

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for the Transformers library and BART model
- **Facebook Research** for the BART-large-CNN architecture
- **Flask Community** for the excellent web framework
- **Open Source Contributors** for various dependencies

## 📞 Support

For questions, issues, or contributions, please open an issue in the repository or contact the maintainers.

---

**⭐ If you find this project useful, please give it a star!**

*Built with ❤️ and lots of ☕ by aspiring AI engineers*
