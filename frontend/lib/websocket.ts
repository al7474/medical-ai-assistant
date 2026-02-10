type MessageType = 'message' | 'system' | 'typing' | 'error'

export interface WebSocketMessage {
  type: MessageType
  text?: string
  message?: string
  timestamp?: string
  provider?: string
  model?: string
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  timestamp: Date
  provider?: string
  model?: string
}

type MessageHandler = (message: WebSocketMessage) => void
type ConnectionHandler = () => void
type ErrorHandler = (error: Event) => void

export class WebSocketClient {
  private ws: WebSocket | null = null
  private url: string
  private token: string
  private reconnectAttempts = 0
  private maxReconnectAttempts = 5
  private reconnectDelay = 1000
  private messageHandlers: MessageHandler[] = []
  private connectHandlers: ConnectionHandler[] = []
  private disconnectHandlers: ConnectionHandler[] = []
  private errorHandlers: ErrorHandler[] = []

  constructor(token: string, url?: string) {
    this.token = token
    this.url = url || 'ws://localhost:8000/ws/chat'
  }

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log('WebSocket already connected')
      return
    }

    try {
      const wsUrl = `${this.url}?token=${this.token}`
      this.ws = new WebSocket(wsUrl)

      this.ws.onopen = () => {
        console.log('✅ WebSocket connected')
        this.reconnectAttempts = 0
        this.connectHandlers.forEach((handler) => handler())
      }

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data)
          this.messageHandlers.forEach((handler) => handler(message))
        } catch (error) {
          console.error('Error parsing WebSocket message:', error)
        }
      }

      this.ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
        this.errorHandlers.forEach((handler) => handler(error))
      }

      this.ws.onclose = () => {
        console.log('🔌 WebSocket disconnected')
        this.disconnectHandlers.forEach((handler) => handler())
        this.attemptReconnect()
      }
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
      this.attemptReconnect()
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++
      const delay = this.reconnectDelay * this.reconnectAttempts

      console.log(
        `🔄 Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms`
      )

      setTimeout(() => {
        this.connect()
      }, delay)
    } else {
      console.error('❌ Max reconnection attempts reached')
    }
  }

  sendMessage(text: string, context?: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      const message = {
        type: 'message',
        text,
        context,
      }
      this.ws.send(JSON.stringify(message))
    } else {
      console.error('WebSocket is not connected')
      throw new Error('WebSocket not connected')
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  onMessage(handler: MessageHandler) {
    this.messageHandlers.push(handler)
    return () => {
      this.messageHandlers = this.messageHandlers.filter((h) => h !== handler)
    }
  }

  onConnect(handler: ConnectionHandler) {
    this.connectHandlers.push(handler)
    return () => {
      this.connectHandlers = this.connectHandlers.filter((h) => h !== handler)
    }
  }

  onDisconnect(handler: ConnectionHandler) {
    this.disconnectHandlers.push(handler)
    return () => {
      this.disconnectHandlers = this.disconnectHandlers.filter(
        (h) => h !== handler
      )
    }
  }

  onError(handler: ErrorHandler) {
    this.errorHandlers.push(handler)
    return () => {
      this.errorHandlers = this.errorHandlers.filter((h) => h !== handler)
    }
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }
}
