import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const message = error.response?.data?.detail || error.message || 'Request failed'
    return Promise.reject(new Error(message))
  }
)

export const apiClient = {
  get: <T = any>(path: string) => api.get<T, T>(path),
  post: <T = any>(path: string, body: any) => api.post<T, T>(path, body),
}
