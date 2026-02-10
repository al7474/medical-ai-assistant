'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store/auth'
import { authAPI } from '@/lib/api'
import ChatInterface from '@/components/ChatInterface'
import { Stethoscope, LogOut, User, MessageSquare } from 'lucide-react'

export default function DashboardPage() {
  const router = useRouter()
  const { user, token, isAuthenticated, logout } = useAuthStore()
  const [isConnected, setIsConnected] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!isAuthenticated || !token) {
      router.push('/login')
      return
    }

    // Verify token is still valid
    authAPI
      .getMe()
      .then(() => {
        setLoading(false)
      })
      .catch(() => {
        logout()
        router.push('/login')
      })
  }, [isAuthenticated, token, router, logout])

  const handleLogout = async () => {
    await authAPI.logout()
    logout()
    router.push('/')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Stethoscope className="w-12 h-12 text-primary-600 mx-auto mb-4 animate-pulse" />
          <p className="text-gray-600">Cargando...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <Stethoscope className="w-8 h-8 text-primary-600" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">MediAI</h1>
                <p className="text-xs text-gray-500">Asistente Médico Inteligente</p>
              </div>
            </div>

            {/* Status */}
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2 px-3 py-1.5 bg-gray-50 rounded-lg">
                <div
                  className={`w-2 h-2 rounded-full ${
                    isConnected ? 'bg-green-500' : 'bg-gray-400'
                  }`}
                />
                <span className="text-sm text-gray-600">
                  {isConnected ? 'En línea' : 'Desconectado'}
                </span>
              </div>

              {/* User Menu */}
              <div className="flex items-center gap-3 px-4 py-2 bg-gray-50 rounded-lg">
                <User className="w-5 h-5 text-gray-600" />
                <div className="text-left">
                  <p className="text-sm font-medium text-gray-900">{user?.name}</p>
                  <p className="text-xs text-gray-500">{user?.email}</p>
                </div>
              </div>

              <button
                onClick={handleLogout}
                className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                title="Cerrar sesión"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 container mx-auto px-4 py-6 overflow-hidden">
        <div className="h-full max-w-5xl mx-auto">
          {/* Chat Card */}
          <div className="bg-white rounded-2xl shadow-lg h-full flex flex-col overflow-hidden">
            {/* Chat Header */}
            <div className="px-6 py-4 border-b border-gray-200 bg-gradient-to-r from-primary-50 to-blue-50">
              <div className="flex items-center gap-3">
                <MessageSquare className="w-6 h-6 text-primary-600" />
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">
                    Chat con Asistente Médico
                  </h2>
                  <p className="text-sm text-gray-600">
                    Consulta tus dudas médicas en tiempo real
                  </p>
                </div>
              </div>
            </div>

            {/* Chat Interface */}
            <div className="flex-1 overflow-hidden">
              <ChatInterface onConnectionChange={setIsConnected} />
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-4">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          <p>
            🔒 Tus conversaciones son privadas y seguras • WebSocket en tiempo real
          </p>
        </div>
      </footer>
    </div>
  )
}
