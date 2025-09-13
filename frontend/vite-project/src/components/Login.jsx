import { useState } from 'react'

export default function Login({ onLogin }) {
  const [name, setName] = useState("")
  const [language, setLanguage] = useState("hi")
  const [phone, setPhone] = useState("")

  const isValidIndianPhone = phone => /^[6-9]\d{9}$/.test(phone)

  const handleSubmit = () => {
    if (!name.trim()) return alert("Please enter your name.")
    if (!isValidIndianPhone(phone)) return alert("Enter a valid Indian phone number.")

    fetch('http://localhost:8000/saathi/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, language, phone })
    })
      .then(res => res.json())
      .then(data => {
        if (data.error) return alert(data.error)
        onLogin(data.driver_id, data.language)
      })
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
          justify-content: center;
          align-items: center;
          background: linear-gradient(135deg, #c3dafe, #e0e7ff, #d8b4fe);
          background-image: url('/sample/Porter-bg.webp');
          background-size: cover;
          background-position: center;
          background-repeat: no-repeat;
        }

        .login-card {
          background: #fff;
          width: 350px;
          padding: 40px;
          border-radius: 20px;
          box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
          text-align: center;
        }

        .login-card h1 {
          font-size: 2rem;
          color: #4f46e5;
          margin-bottom: 10px;
        }

        .login-card p {
          font-size: 0.9rem;
          color: #6b7280;
          margin-bottom: 30px;
        }

        .login-card input,
        .login-card select {
          width: 100%;
          padding: 12px 15px;
          margin-bottom: 20px;
          border-radius: 10px;
          border: 1px solid #d1d5db;
          font-size: 1rem;
          outline: none;
          transition: 0.3s;
        }

        .login-card input:focus,
        .login-card select:focus {
          border-color: #4f46e5;
          box-shadow: 0 0 5px rgba(79, 70, 229, 0.5);
        }

        .login-card button {
          width: 100%;
          padding: 12px;
          background-color: #4f46e5;
          color: #fff;
          font-size: 1rem;
          font-weight: bold;
          border: none;
          border-radius: 10px;
          cursor: pointer;
          transition: 0.3s;
        }

        .login-card button:hover {
          background-color: #4338ca;
        }

        .login-card .footer {
          margin-top: 20px;
          font-size: 0.8rem;
          color: #9ca3af;
        }
      `}</style>

      <div className="page-bg">
        <div className="login-card">
          <h1>🎙️ Porter Saathi</h1>
          <p>Your voice-first assistant for earnings, growth, and guidance</p>

          <input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
          <input
            type="tel"
            placeholder="Enter your phone number"
            value={phone}
            onChange={e => setPhone(e.target.value)}
          />
          <select
            value={language}
            onChange={e => setLanguage(e.target.value)}
          >
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="kn">Kannada</option>
          </select>

          <button onClick={handleSubmit}>🚀 Login</button>

          <div className="footer">Powered by Porter</div>
        </div>
      </div>
    </div>
  )
}
