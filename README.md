# 🔗 Python Blockchain Implementation

A fully functional blockchain cryptocurrency system built with Python and Flask, featuring proof-of-work consensus, digital wallets, and peer-to-peer networking.

## 🚀 Live Demo

**[Try the live blockchain app →](https://blockchain-project-5vkm.onrender.com/)**

## ✨ Features

### Core Blockchain Functionality
- **Proof-of-Work Consensus**: Secure mining with adjustable difficulty
- **Digital Wallets**: RSA key pair generation and management
- **Transaction System**: Cryptographically signed transactions
- **Peer-to-Peer Network**: Multi-node blockchain synchronization
- **Conflict Resolution**: Longest chain rule implementation

### Web Interface
- **Interactive Dashboard**: Real-time blockchain monitoring
- **Wallet Management**: Create/load wallets with balance tracking
- **Transaction Processing**: Send/receive cryptocurrency
- **Network Visualization**: View connected peer nodes
- **Mining Interface**: Mine new blocks and earn rewards

### Technical Highlights
- RESTful API with comprehensive endpoints
- Persistent data storage (JSON-based)
- Bootstrap-responsive web UI
- Modular architecture with proper separation of concerns
- Production-ready with Heroku deployment configuration

## 🛠️ Technology Stack

- **Backend**: Python 3.9, Flask, Flask-CORS
- **Cryptography**: PyCrypto (RSA signatures, SHA-256 hashing)
- **Frontend**: HTML5, CSS3, Bootstrap 4, Vanilla JavaScript
- **Deployment**: Gunicorn WSGI server
- **Networking**: HTTP REST API, JSON data exchange

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.9+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/blockchain-project.git
   cd blockchain-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run a single node**
   ```bash
   python node.py
   ```
   Access the web interface at `http://localhost:5000`

### Multi-Node Network

Run multiple nodes to test peer-to-peer functionality:

```bash
# Terminal 1 - Node on port 5000
python node.py --port 5000

# Terminal 2 - Node on port 5001  
python node.py --port 5001

# Terminal 3 - Node on port 5002
python node.py --port 5002
```

Connect nodes via the web interface to create a distributed network.

## 📊 API Documentation

### Wallet Operations
- `POST /wallet` - Create new wallet keys
- `GET /wallet` - Load existing wallet

### Transaction Management
- `POST /transaction` - Submit new transaction
- `GET /transactions` - Get pending transactions

### Blockchain Operations
- `GET /chain` - Retrieve full blockchain
- `POST /mine` - Mine a new block
- `POST /resolve-conflicts` - Synchronize with network

### Network Management
- `POST /node` - Add peer node
- `GET /nodes` - List connected peers
- `DELETE /node/<node_id>` - Remove peer node

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web UI        │    │   Flask API     │    │   Blockchain    │
│   (Bootstrap)   │◄──►│   (REST)        │◄──►│   Core Logic    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   Utilities     │
                       │   - Hash Utils  │
                       │   - Verification│
                       │   - Crypto      │
                       └─────────────────┘
```

### Key Components

- **`blockchain.py`**: Core blockchain logic and consensus algorithm
- **`node.py`**: Flask REST API server and routing
- **`wallet.py`**: RSA cryptography and key management
- **`transaction.py`**: Transaction data structures
- **`block.py`**: Block data structures
- **`utility/`**: Hashing, verification, and helper functions

## 🧪 Testing the Application

1. **Create a wallet** - Generate RSA key pairs
2. **Mine blocks** - Earn initial cryptocurrency
3. **Send transactions** - Transfer funds between wallets
4. **Add peer nodes** - Test network synchronization
5. **Resolve conflicts** - Verify longest chain consensus

## 🚀 Deployment

The application is configured for production deployment with:

- **Heroku**: Ready-to-deploy with `Procfile` and `runtime.txt`
- **Railway/Render**: Modern cloud platforms with Git integration
- **Environment Variables**: Configurable port and settings

### Deploy to Heroku

```bash
heroku create your-blockchain-app
git push heroku main
```

## 🔐 Security Features

- **Digital Signatures**: All transactions cryptographically signed
- **Hash Verification**: Block integrity through SHA-256 chaining
- **Proof-of-Work**: Prevents double-spending and spam
- **Input Validation**: Comprehensive request validation
- **Key Security**: Private keys stored locally, never transmitted

## 📈 Performance Considerations

- **Mining Difficulty**: Adjustable proof-of-work complexity
- **Data Persistence**: Efficient JSON-based storage
- **Network Optimization**: Minimal bandwidth peer communication
- **Scalability**: Modular design supports feature expansion

## 🤝 Contributing

This project demonstrates core blockchain concepts and is open for improvements:

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

*Built to demonstrate blockchain technology, cryptographic principles, and full-stack development skills.*