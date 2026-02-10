'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store/auth'
import { Stethoscope, ArrowRight } from 'lucide-react'

export default function Home() {
  const router = useRouter()
  const { user, isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, router])

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <nav className="flex justify-between items-center mb-20">
          <div className="flex items-center gap-2">
            <Stethoscope className="w-8 h-8 text-primary-600" />
            <span className="text-2xl font-bold text-gray-900">MediAI</span>
          </div>
          <div className="flex gap-4">
            <a
              href="/login"
              className="px-4 py-2 text-primary-600 hover:text-primary-700 font-medium"
            >
              Iniciar Sesión
            </a>
            <a
              href="/register"
              className="px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition-colors"
            >
              Registrarse
            </a>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Tu Asistente Médico
            <span className="block text-primary-600 mt-2">Inteligente</span>
          </h1>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">
            Conversa naturalmente con nuestra IA médica. Obtén información sobre
            síntomas, agenda citas y recibe orientación profesional en tiempo real.
          </p>

          <div className="flex gap-4 justify-center mb-20">
            <a
              href="/register"
              className="group px-8 py-4 bg-primary-600 text-white rounded-lg hover:bg-primary-700 font-medium transition-all flex items-center gap-2 text-lg shadow-lg hover:shadow-xl"
            >
              Comenzar Ahora
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </a>
            <a
              href="/login"
              className="px-8 py-4 bg-white text-gray-900 rounded-lg hover:bg-gray-50 font-medium transition-colors text-lg border-2 border-gray-200"
            >
              Iniciar Sesión
            </a>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-4l-4 4z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Chat en Tiempo Real</h3>
              <p className="text-gray-600">
                Conversa con la IA médica instantáneamente con WebSocket
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Seguro y Privado</h3>
              <p className="text-gray-600">
                Autenticación JWT y encriptación de datos
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold mb-2">Gestión de Citas</h3>
              <p className="text-gray-600">
                Agenda y administra tus citas médicas fácilmente
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
