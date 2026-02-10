# Medical AI Assistant - Frontend

Frontend application built with Next.js 14, TypeScript, and Tailwind CSS.

## 🚀 Features

- ✅ **Modern UI** - Beautiful interface with Tailwind CSS
- ✅ **Authentication** - Login and registration with JWT
- ✅ **Real-time Chat** - WebSocket integration for instant messaging
- ✅ **Type Safety** - Full TypeScript support
- ✅ **State Management** - Zustand for simple and effective state management
- ✅ **Protected Routes** - Automatic authentication checks

## 📦 Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework
- **Zustand** - State management
- **Axios** - HTTP client
- **Lucide React** - Beautiful icons
- **WebSocket** - Real-time bidirectional communication

## 🏃 Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend running on `http://localhost:8000`

### Installation

1. **Install dependencies:**

```bash
npm install
```

2. **Create environment file:**

```bash
cp .env.example .env.local
```

Edit `.env.local` if needed:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

3. **Run development server:**

```bash
npm run dev
```

4. **Open your browser:**

```
http://localhost:3000
```

## 📁 Project Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page
│   ├── login/                   # Login page
│   ├── register/                # Register page
│   └── dashboard/               # Dashboard (protected)
│
├── components/                   # React components
│   └── ChatInterface.tsx        # WebSocket chat component
│
├── lib/                         # Utilities and helpers
│   ├── api.ts                   # API client (Axios)
│   ├── websocket.ts             # WebSocket client
│   └── store/                   # State management
│       └── auth.ts              # Auth store (Zustand)
│
└── public/                      # Static assets
```

## 🔑 Authentication Flow

1. **Register** → Creates account via `/auth/register`
2. **Login** → Gets JWT token via `/auth/login`
3. **Token Storage** → Saved in localStorage (via Zustand persist)
4. **Protected Routes** → Dashboard redirects to login if not authenticated
5. **API Requests** → Token automatically added to headers
6. **Logout** → Clears token and redirects to home

## 💬 Chat Features

- **Real-time messaging** with WebSocket
- **Typing indicators** when AI is responding
- **Connection status** display
- **Message history** during session
- **Auto-scroll** to latest message
- **Error handling** with reconnection logic

## 🎨 UI Components

### Pages

- **Home** (`/`) - Landing page with features
- **Login** (`/login`) - User authentication
- **Register** (`/register`) - New user signup
- **Dashboard** (`/dashboard`) - Main chat interface (protected)

### Components

- **ChatInterface** - Real-time chat with WebSocket
- **Layout** - Responsive header and navigation

## 🔧 Configuration

### API Client (`lib/api.ts`)

Axios instance configured with:
- Base URL from environment
- Auto token injection in headers
- 401 error handling (auto-logout)
- Request/response interceptors

### WebSocket Client (`lib/websocket.ts`)

Features:
- Token-based authentication
- Auto-reconnection (up to 5 attempts)
- Event handlers for message, connect, disconnect, error
- Message type handling (message, system, typing, error)

### State Management (`lib/store/auth.ts`)

Zustand store with:
- User data
- JWT token
- Auth status
- Persisted to localStorage

## 🚀 Building for Production

```bash
# Build
npm run build

# Start production server
npm start
```

## 📝 Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint

## 🌐 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `NEXT_PUBLIC_WS_URL` | WebSocket URL | `ws://localhost:8000` |

## 🐛 Troubleshooting

### WebSocket won't connect

1. Check backend is running on port 8000
2. Check you're logged in (have valid token)
3. Check WebSocket URL in `.env.local`
4. Check browser console for errors

### API requests failing

1. Check backend is running
2. Check API URL in `.env.local`
3. Check CORS is configured in backend
4. Check token is valid (not expired)

### Build errors

```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Try build again
npm run build
```

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Zustand](https://github.com/pmndrs/zustand)
- [Axios](https://axios-http.com/docs/intro)

## 🤝 Integration with Backend

Make sure the backend is running with:

- ✅ PostgreSQL database
- ✅ Authentication endpoints (`/auth/register`, `/auth/login`, `/auth/me`)
- ✅ WebSocket endpoint (`/ws/chat?token=JWT`)
- ✅ CORS enabled for `http://localhost:3000`

See [backend/README.md](../backend/README.md) for backend setup.

---

**Happy coding! 🎉**
