# Appointly

## Overview

Appointly is a web application that allows users to book appointments online.

## Installation

### Prerequisites
- Python 3.11+
- NPM 11+
- docker-compose

1. **Clone the repository**
```bash
git clone https://github.com/lytexdev/Appointly.git
cd Appointly
```

2. **Copy and rename the `.env.example` file to `.env`**
```bash
cp env.example .env
```

3. **Install dependencies**
```bash
cd frontend
npm install
npm run build
cd ..
```

5. **Run docker-compose**
```bash
docker-compose up -d --build
```

## License
This project is licensed under the GNU General Public License v2. See the [LICENSE](LICENSE) file for details.