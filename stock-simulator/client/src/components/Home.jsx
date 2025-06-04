import { useState, useEffect } from 'react'

const Home = ({ Link, api }) => {
  const [serverStatus, setServerStatus] = useState(null)

  useEffect(() => {
    const checkServerStatus = async () => {
      try {
        const response = await api.get('/ping')
        if (response.status === 200) {
          setServerStatus('online')
        } else {
          setServerStatus('offline')
        }
      } catch (error) {
        setServerStatus('offline')
      }
    }

    checkServerStatus()
  }, [api])

  if (serverStatus === 'offline') {
    return (
      <div className="min-h-screen hero bg-base-200">
        <div className="text-center hero-content">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold text-primary">Server Offline</h1>
            <p className="py-6 text-lg text-secondary">
              The server is currently offline. Please try again later.
            </p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen hero bg-base-200">
      <div className="text-center hero-content">
        <div className="max-w-md">
          <h1 className="text-5xl font-bold">Welcome</h1>
          <p className="py-6">Stock market simulator</p>
          <div className="flex flex-col space-y-2">
            <Link
              to="/login"
              className="text-lg btn btn-primary text-primary-content"
            >
              Log In
            </Link>
            <h1 className="text-2xl font-bold text-primary">or</h1>
            <Link
              to="/register"
              className="text-lg btn btn-primary text-primary-content"
            >
              Create Account
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home
