'use client'

import { useEffect, useState, useRef } from 'react'
import { WebSocketClient, ChatMessage, WebSocketMessage } from '@/lib/websocket'
import { useAuthStore } from '@/lib/store/auth'
import { Send, Loader2, Bot, User as UserIcon } from 'lucide-react'

interface ChatInterfaceProps {
  onConnectionChange?: (connected: boolean) => void
}

export default function ChatInterface({ onConnectionChange }: ChatInterfaceProps) {
  const { token, user } = useAuthStore()
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const wsClient = useRef<WebSocketClient | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (!token) return

    // Initialize WebSocket
    wsClient.current = new WebSocketClient(token)
    
    // Handle connection
    wsClient.current.onConnect(() => {
      setIsConnected(true)
      onConnectionChange?.(true)
    })

    wsClient.current.onDisconnect(() => {
      setIsConnected(false)
      onConnectionChange?.(false)
    })

    // Handle messages
    wsClient.current.onMessage((wsMsg: WebSocketMessage) => {
      if (wsMsg.type === 'system') {
        const systemMsg: ChatMessage = {
          id: Date.now().toString(),
          role: 'system',
          content: wsMsg.message || '',
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, systemMsg])
      } else if (wsMsg.type === 'typing') {
        setIsTyping(true)
      } else if (wsMsg.type === 'message') {
        setIsTyping(false)
        setIsSending(false)
        const assistantMsg: ChatMessage = {
          id: Date.now().toString(),
          role: 'assistant',
          content: wsMsg.text || '',
          timestamp: new Date(),
          provider: wsMsg.provider,
          model: wsMsg.model,
        }
        setMessages((prev) => [...prev, assistantMsg])
      } else if (wsMsg.type === 'error') {
        setIsTyping(false)
        setIsSending(false)
        const errorMsg: ChatMessage = {
          id: Date.now().toString(),
          role: 'system',
          content: `Error: ${wsMsg.message || 'Unknown error'}`,
          timestamp: new Date(),
        }
        setMessages((prev) => [...prev, errorMsg])
      }
    })

    // Connect
    wsClient.current.connect()

    return () => {
      wsClient.current?.disconnect()
    }
  }, [token, onConnectionChange])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isTyping])

  const handleSend = () => {
    if (!input.trim() || !wsClient.current || isSending) return

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setIsSending(true)
    
    try {
      wsClient.current.sendMessage(input)
      setInput('')
    } catch (error) {
      console.error('Failed to send message:', error)
      setIsSending(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex flex-col h-full">
      {/* Connection Status */}
      <div className="px-4 py-2 border-b border-gray-200 bg-white">
        <div className="flex items-center gap-2">
          <div
            className={`w-2 h-2 rounded-full ${
              isConnected ? 'bg-green-500' : 'bg-red-500'
            }`}
          />
          <span className="text-sm text-gray-600">
            {isConnected ? 'Conectado' : 'Desconectado'}
          </span>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <Bot className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600 text-lg mb-2">
              ¡Hola {user?.name}! 👋
            </p>
            <p className="text-gray-500">
              Soy tu asistente médico inteligente. ¿En qué puedo ayudarte hoy?
            </p>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {message.role !== 'user' && (
              <div className="flex-shrink-0">
                <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                  <Bot className="w-5 h-5 text-primary-600" />
                </div>
              </div>
            )}

            <div
              className={`max-w-[70%] rounded-2xl px-4 py-3 ${
                message.role === 'user'
                  ? 'bg-primary-600 text-white'
                  : message.role === 'system'
                  ? 'bg-gray-200 text-gray-700 text-sm'
                  : 'bg-white text-gray-900 shadow-sm border border-gray-200'
              }`}
            >
              <p className="whitespace-pre-wrap">{message.content}</p>
              {message.provider && (
                <p className="text-xs mt-2 opacity-70">
                  {message.provider} • {message.model}
                </p>
              )}
            </div>

            {message.role === 'user' && (
              <div className="flex-shrink-0">
                <div className="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center">
                  <UserIcon className="w-5 h-5 text-white" />
                </div>
              </div>
            )}
          </div>
        ))}

        {isTyping && (
          <div className="flex gap-3 justify-start">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                <Bot className="w-5 h-5 text-primary-600" />
              </div>
            </div>
            <div className="max-w-[70%] rounded-2xl px-4 py-3 bg-white shadow-sm border border-gray-200">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="p-4 bg-white border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu mensaje..."
            disabled={!isConnected || isSending}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || !isConnected || isSending}
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            {isSending ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </button>
        </div>
      </div>
    </div>
  )
}
