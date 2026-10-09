import { initializeApp, getApps, FirebaseApp } from 'firebase/app'
import { getAuth, GoogleAuthProvider, Auth } from 'firebase/auth'

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || 'AIzaSyDbCp38sr8TFerh4hslJLBgV2zyMStLzYs',
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || 'clincode-medical-ai.firebaseapp.com',
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || 'clincode-medical-ai',
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || 'clincode-medical-ai.firebasestorage.app',
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || '1063673668366',
  appId: import.meta.env.VITE_FIREBASE_APP_ID || '1:1063673668366:web:cce2f1741ad9950d192d5f'
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
  return Boolean(import.meta.env.VITE_FIREBASE_API_KEY || firebaseConfig.apiKey)
}
