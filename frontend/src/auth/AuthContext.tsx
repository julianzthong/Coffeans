import { createContext, useContext, useState, useCallback, ReactNode } from 'react'
import { api } from '../api/client'

interface AuthContextValue {
  token: string | null
  login: (email: string, password: string) => Promise<void>
  signup: (email: string, password: string, displayName: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('coffeans_token'))

  const login = useCallback(async (email: string, password: string) => {
    const { access_token } = await api.login(email, password)
    localStorage.setItem('coffeans_token', access_token)
    setToken(access_token)
  }, [])

  const signup = useCallback(
    async (email: string, password: string, displayName: string) => {
      await api.signup(email, password, displayName)
      await login(email, password)
    },
    [login],
  )

  const logout = useCallback(() => {
    localStorage.removeItem('coffeans_token')
    setToken(null)
  }, [])

  return <AuthContext.Provider value={{ token, login, signup, logout }}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
