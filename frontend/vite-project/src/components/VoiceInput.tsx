import { useState } from 'react'

export default function VoiceInput({ driverId, language }) {
  const [listening, setListening] = useState(false)

  const startListening = () => {
    const recognition = new window.webkitSpeechRecognition()
    recognition.lang = language === "kn" ? "kn-IN" : language === "en" ? "en-IN" : "hi-IN"
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
        body: JSON.stringify({ transcript, driver_id: driverId })
      })
        .then((res) => res.json())
        .then((data) => {
          alert(data.message)
          const utterance = new SpeechSynthesisUtterance(data.message)
          utterance.lang = recognition.lang
          speechSynthesis.speak(utterance)
        })
    }

    recognition.start()
  }

  return (
    <div>
      <style>{`
        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
          font-family: 'Arial', sans-serif;
        }

        body, html, #root {
          height: 100%;
        }

        .page-bg {
          height: 100vh;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          background: linear-gradient(135deg, #c3dafe, #e0e7ff, #d8b4fe);
        }

        h1 {
          font-size: 2rem;
          color: #4f46e5;
          margin-bottom: 50px;
          text-align: center;
        }

        .mic-btn {
          width: 120px;
          height: 120px;
          background-color: #4f46e5;
          border-radius: 50%;
          display: flex;
          justify-content: center;
          align-items: center;
          cursor: pointer;
          transition: 0.3s;
          position: relative;
          box-shadow: 0 8px 20px rgba(0,0,0,0.2);
        }

        .mic-btn:hover {
          transform: scale(1.1);
        }

        .mic-btn svg {
          width: 50px;
          height: 50px;
          fill: white;
        }

        .listening {
          animation: pulse 1s infinite;
        }

        @keyframes pulse {
          0% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.5); }
          50% { box-shadow: 0 0 0 20px rgba(79, 70, 229, 0); }
          100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
        }

        .status {
          margin-top: 30px;
          font-size: 1.2rem;
          color: #4f46e5;
        }
      `}</style>

      <div className="page-bg">
        <h1>How can I help you?</h1>

        <div
          className={`mic-btn ${listening ? 'listening' : ''}`}
          onClick={startListening}
        >
          <svg viewBox="0 0 24 24">
            <path d="M12 14c1.654 0 3-1.346 3-3V5c0-1.654-1.346-3-3-3S9 3.346 9 5v6c0 1.654 1.346 3 3 3z"/>
            <path d="M19 11c0 3.309-2.691 6-6 6s-6-2.691-6-6H5c0 3.866 3.134 7 7 7v3h2v-3c3.866 0 7-3.134 7-7h-2z"/>
          </svg>
        </div>

        <div className="status">
          {listening ? "Listening..." : "Click the mic to start listening"}
        </div>
      </div>
    </div>
  )
}
