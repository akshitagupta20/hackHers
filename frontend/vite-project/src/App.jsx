import { useState } from 'react'
import Login from './components/Login.jsx'
import VoiceInput from './components/VoiceInput.jsx'

function App() {
  const [driverId, setDriverId] = useState(null)
  const [language, setLanguage] = useState("hi")

  return driverId ? (
    <VoiceInput driverId={driverId} language={language} />
  ) : (
    <Login onLogin={(id, lang) => {
      setDriverId(id)
      setLanguage(lang)
    }} />
  )
}

export default App

