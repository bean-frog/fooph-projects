import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { themeChange } from 'theme-change'
import {
  BrowserRouter as Router,
  Routes,
  Link,
  Route,
  useNavigate,
} from 'react-router-dom'
import Dashboard from './components/Dashboard'
import Login from './components/Login'
import Register from './components/Register'
import Home from './components/Home'
import './index.css'
import OldApp from './App.old'

const App = () => {
  useEffect(() => {
    themeChange(false)
  }, [])

  const [auth, setAuth] = useState(null)

  // API endpoints
  const api = axios.create({
    baseURL: 'http://127.0.0.1:8080',
  })

  const Header = ({ auth, setAuth, api }) => {
    const navigate = useNavigate()
    return (
      <header className="flex fixed flex-row justify-between items-center px-4 py-2 w-screen h-fit bg-base-200">
        <h1 className="text-xl font-bold text-primary">
          Stock Trading Simulator
        </h1>
        <div className="ml-auto">
          {auth ? (
            <button
              onClick={async () => {
                await api.get('/logout').then(() => {
                  setAuth(null)
                  navigate('/')
                })
              }}
              className="btn btn-sm btn-primary"
            >
              Logout
            </button>
          ) : null}
          <select data-choose-theme className="select select-ghost select-sm">
            <option value="sunset">Sunset (Default)</option>
            <option value="forest">Forest</option>
            <option value="retro">Retro</option>
            <option value="light">Light</option>
            <option value="black">Black</option>
            <option value="nord">Nord</option>
            <option value="luxury">Luxury</option>
            <option value="pastel">Pastel</option>
          </select>
        </div>
      </header>
    )
  }

  const Layout = ({ children }) => {
    return (
      <>
        <Header auth={auth} setAuth={setAuth} api={api} />
        <div className="flex overflow-y-hidden flex-col justify-center items-center w-screen h-screen">
          {children}
        </div>
      </>
    )
  }

  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home Link={Link} api={api} />} />
          <Route path="/register" element={<Register api={api} />} />
          <Route
            path="/login"
            element={<Login auth={auth} setAuth={setAuth} api={api} />}
          />
          <Route
            path="/dashboard"
            element={<Dashboard auth={auth} api={api} />}
          />
          <Route path="/test" element={<OldApp />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
