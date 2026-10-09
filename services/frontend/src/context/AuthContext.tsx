import React, { createContext, useContext, useState, useEffect } from 'react'
import {
  signInWithPopup,
  signOut as firebaseSignOut,
  onAuthStateChanged,
  User as FirebaseUser
} from 'firebase/auth'
import { auth, googleProvider } from '../config/firebase'
import { api, setAuthToken } from '../api/client'

export type AppRole = 'coder' | 'cdi' | 'manager' | 'admin'

export interface UserProfile {
  id: string
  email: string
  name: string
  role: AppRole
  photoURL?: string
}

interface AuthContextType {
  user: UserProfile | null
  loading: boolean
  error: string | null
  signInWithGoogle: (requestedRole?: AppRole) => Promise<void>
  demoLogin: (role: AppRole) => void
  logout: () => Promise<void>
  switchRole: (role: AppRole) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // Session restoration check
    const savedUser = localStorage.getItem('clincode_user_session')
    if (savedUser) {
      try {
        const parsed = JSON.parse(savedUser)
        setUser(parsed)
      } catch (err) {
        localStorage.removeItem('clincode_user_session')
      }
    }

    const unsubscribe = onAuthStateChanged(auth, async (fbUser: FirebaseUser | null) => {
      if (fbUser) {
        try {
          const token = await fbUser.getIdToken()
          setAuthToken(token)

          // Sync user with backend API
          try {
            const synced = await api.firebaseLogin(token)
            const profile: UserProfile = {
              id: synced.id,
              email: synced.email,
              name: fbUser.displayName || synced.username.split('@')[0],
              role: (synced.role as AppRole) || 'coder',
              photoURL: fbUser.photoURL || undefined
            }
            setUser(profile)
            localStorage.setItem('clincode_user_session', JSON.stringify(profile))
          } catch (syncErr) {
            // Fallback profile if backend unreachable during initial load
            const profile: UserProfile = {
              id: fbUser.uid,
              email: fbUser.email || 'user@clincode.ai',
              name: fbUser.displayName || 'Clinical Coder',
              role: 'coder',
              photoURL: fbUser.photoURL || undefined
            }
            setUser(profile)
            localStorage.setItem('clincode_user_session', JSON.stringify(profile))
          }
        } catch (err: any) {
          setError(err.message || 'Failed to authenticate with Firebase')
        }
      }
      setLoading(false)
    })

    return () => unsubscribe()
  }, [])

  const signInWithGoogle = async (requestedRole?: AppRole) => {
    setError(null)
    setLoading(true)
    try {
      const result = await signInWithPopup(auth, googleProvider)
      const token = await result.user.getIdToken()
      setAuthToken(token)

      let userRole: AppRole = requestedRole || 'coder'
      try {
        const synced = await api.firebaseLogin(token, requestedRole)
        userRole = (synced.role as AppRole) || userRole
      } catch (err) {
        // Fallback for demo environments
      }

      const profile: UserProfile = {
        id: result.user.uid,
        email: result.user.email || 'user@clincode.ai',
        name: result.user.displayName || 'ClinCode Specialist',
        role: userRole,
        photoURL: result.user.photoURL || undefined
      }
      setUser(profile)
      localStorage.setItem('clincode_user_session', JSON.stringify(profile))
    } catch (err: any) {
      if (err.code !== 'auth/popup-closed-by-user') {
        setError(err.message || 'Google Sign-In failed')
      }
    } finally {
      setLoading(false)
    }
  }

  const demoLogin = (role: AppRole) => {
    setError(null)
    const profile: UserProfile = {
      id: `demo-${role}-id`,
      email: `${role}@clincode.ai`,
      name: `${role.toUpperCase()} Specialist (Demo)`,
      role: role
    }
    setUser(profile)
    localStorage.setItem('clincode_user_session', JSON.stringify(profile))
  }

  const switchRole = async (newRole: AppRole) => {
    if (!user) return
    const updated = { ...user, role: newRole }
    setUser(updated)
    localStorage.setItem('clincode_user_session', JSON.stringify(updated))
  }

  const logout = async () => {
    try {
      await firebaseSignOut(auth)
    } catch {
      // Ignored
    }
    setAuthToken(null)
    setUser(null)
    localStorage.removeItem('clincode_user_session')
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        signInWithGoogle,
        demoLogin,
        logout,
        switchRole
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
