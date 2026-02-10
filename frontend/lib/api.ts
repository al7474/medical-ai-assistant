import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const authStorage = localStorage.getItem('auth-storage')
    if (authStorage) {
      const { state } = JSON.parse(authStorage)
      if (state?.token) {
        config.headers.Authorization = `Bearer ${state.token}`
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth and redirect to login
      localStorage.removeItem('auth-storage')
      if (typeof window !== 'undefined') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  register: async (data: { name: string; email: string; password: string }) => {
    const response = await api.post('/auth/register', data)
    return response.data
  },

  login: async (email: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await api.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  getMe: async (token?: string) => {
    const headers: any = {}
    if (token) {
      headers.Authorization = `Bearer ${token}`
    }
    const response = await api.get('/auth/me', { headers })
    return response.data
  },

  logout: async () => {
    await api.post('/auth/logout').catch(() => {})
  },
}

// Chat API
export const chatAPI = {
  sendMessage: async (message: string, conversationId?: string) => {
    const response = await api.post('/chat', {
      message,
      conversation_id: conversationId,
    })
    return response.data
  },
}

// Users API
export const usersAPI = {
  getAll: async () => {
    const response = await api.get('/users')
    return response.data
  },

  getById: async (id: number) => {
    const response = await api.get(`/users/${id}`)
    return response.data
  },

  create: async (data: { name: string; email: string }) => {
    const response = await api.post('/users', data)
    return response.data
  },

  update: async (id: number, data: { name?: string; email?: string }) => {
    const response = await api.put(`/users/${id}`, data)
    return response.data
  },

  delete: async (id: number) => {
    const response = await api.delete(`/users/${id}`)
    return response.data
  },
}
