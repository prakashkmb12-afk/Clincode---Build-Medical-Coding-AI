import { initializeApp, getApps, FirebaseApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider, Auth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'AIzaSyDemoKeyForClinCodeTesting12345',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'clincode-medical-ai.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'clincode-medical-ai',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'clincode-medical-ai.appspot.com',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '123456789012',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:123456789012:web:demo123456789'
}

let app: FirebaseApp
if (!getApps().length) {
  app = initializeApp(firebaseConfig)
} else {
  app = getApps()[0]
}

export const auth: Auth = getAuth(app)
export const googleProvider = new GoogleAuthProvider()
googleProvider.setCustomParameters({ prompt: 'select_account' })

export const isFirebaseConfigured = () => {
  return Boolean(import.meta.env.VITE_FIREBASE_API_KEY)
}
