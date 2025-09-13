import { useState } from 'react'

export default function VoiceInput() {
  const [listening, setListening] = useState(false)

  const startListening = () => {
    const recognition = new window.webkitSpeechRecognition()
    recognition.lang = 'hi-IN'
    recognition.interimResults = false
    recognition.continuous = false

    recognition.onstart = () => setListening(true)
    recognition.onend = () => setListening(false)
    recognition.onerror = (event) => alert(`Mic error: ${event.error}`)

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      console.log('🗣️ Transcript:', transcript)

      fetch('http://localhost:8000/saathi/respond', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ transcript })
      })
        .then((res) => res.json())
        .then((data) => {
          alert(data.message)
          const utterance = new SpeechSynthesisUtterance(data.message)
          utterance.lang = 'hi-IN'
          speechSynthesis.speak(utterance)
        })
    }

    recognition.start()
  }

  return (
    <div className="mt-4 text-center">
      <button onClick={startListening} className="px-4 py-2 bg-blue-600 text-white rounded">
        🎙️ Speak Now
      </button>
      {listening && <p className="text-green-600 mt-2">Listening...</p>}
    </div>
  )
}
