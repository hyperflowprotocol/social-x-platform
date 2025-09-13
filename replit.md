# Overview

This repository contains a comprehensive social trading platform that combines NFT marketplace functionality, cryptocurrency wallet management, and blockchain integration with HyperEVM. The platform provides users with Twitter/X authentication, wallet generation, NFT collection management, and trading capabilities. The system features real blockchain integration for HYPE token deployment and management, Google Sheets synchronization for user data, and AI-powered NFT artwork generation capabilities.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Web Server**: Python HTTP server with custom request handlers for different platform sections
- **UI Framework**: Vanilla HTML/CSS/JavaScript with responsive design patterns
- **Template System**: Server-side HTML generation with embedded data binding
- **Real-time Updates**: WebSocket-style connections for live market data and wallet balances

## Backend Architecture
- **Core Platform**: Python-based social trading platform with modular handler system
- **Authentication**: Twitter/X OAuth integration with session management via pickle storage
- **Wallet Management**: Ethereum-compatible wallet generation and management system
- **Trading Engine**: Support for token trading, NFT marketplace operations, and portfolio tracking

## Data Storage Solutions
- **User Sessions**: JSON file storage for session persistence (`session_storage.json`)
- **Wallet Data**: Pickle serialization for encrypted wallet storage (`user_wallets.pkl`)
- **NFT Metadata**: JSON format for NFT collection data and traits
- **Backup Systems**: Google Sheets integration for data redundancy and export capabilities

## Authentication and Authorization
- **OAuth Provider**: Twitter/X OAuth 1.0a flow for user authentication
- **Session Management**: Server-side session storage with token persistence
- **Wallet Security**: Private key generation using cryptographically secure methods
- **Rate Limiting**: Built-in handling for Twitter API rate limits with retry mechanisms

## External Dependencies

### Blockchain Networks
- **HyperEVM Mainnet**: Primary blockchain network (Chain ID: 999)
- **RPC Endpoints**: Multiple redundant RPC connections for reliability
- **Smart Contracts**: HYPE token contract deployment and management
- **Transaction Processing**: Raw transaction construction and submission

### Third-party APIs
- **Twitter/X API**: OAuth authentication and profile data retrieval
- **Google Sheets API**: Data synchronization and backup functionality
- **Blockscout API**: NFT metadata and transaction verification
- **IPFS Gateways**: Decentralized storage for NFT images and metadata

### AI Services
- **Google Gemini AI**: NFT artwork generation and image creation
- **Image Processing**: PIL (Python Imaging Library) for artwork manipulation
- **Content Generation**: AI-powered trait and metadata generation

### Development Tools
- **Web3 Libraries**: Ethereum transaction handling and address generation
- **Cryptography**: Secure private key generation and wallet management
- **HTTP Clients**: Requests library for API communication with fallback to curl/subprocess
- **Data Serialization**: JSON and Pickle for various data storage needs

### Marketplace Integration
- **Drip.Trade API**: Real NFT marketplace data fetching
- **Image Optimization**: WebP conversion and CDN integration
- **Price Discovery**: Real-time floor price and volume tracking
- **Collection Analytics**: Rarity ranking and trait distribution analysis