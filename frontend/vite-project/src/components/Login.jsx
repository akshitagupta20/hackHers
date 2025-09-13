import { useState } from 'react'

export default function Login({ onLogin }) {
  const [name, setName] = useState("")
  const [language, setLanguage] = useState("hi")

  const handleSubmit = () => {
    fetch('http://localhost:8000/saathi/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, language })
    })
      .then(res => res.json())
      .then(data => {
        onLogin(data.driver_id, language)
      })
  }

  return (
    <div className="p-4 text-center">
      <h2 className="text-lg font-bold">🚪 Login to Porter Saathi</h2>
      <input value={name} onChange={e => setName(e.target.value)} placeholder="Your name" className="mt-2 p-2 border" />
      <select value={language} onChange={e => setLanguage(e.target.value)} className="mt-2 p-2 border">
        <option value="en">English</option>
        <option value="hi">Hindi</option>
        <option value="kn">Kannada</option>
      </select>
      <button onClick={handleSubmit} className="mt-4 px-4 py-2 bg-green-600 text-white rounded">Login</button>
    </div>
  )
}
