import { useNavigate } from 'react-router'
const Login = ({ api, auth, setAuth }) => {
  let navigate = useNavigate()
  return (
    <div className="p-4 rounded-lg border w-fit h-fit border-base-300 bg-neutral text-neutral-content">
      <h2 className="mb-2 text-xl font-bold">Login</h2>
      <form
        onSubmit={async (e) => {
          e.preventDefault()
          const { name, pass } = e.target.elements
          try {
            const res = await api.post('/login', {
              name: name.value,
              pass: pass.value,
            })
            console.log(res)
            if (res.status === 200) {
              setAuth(name.value)
              console.log('auth set' + name.value)
              navigate('/dashboard')
            } else {
              setAuth(null)
              console.log(res.status)
            }
          } catch (err) {
            console.log(err)
          }
        }}
      >
        <input
          required
          type="text"
          name="name"
          placeholder="Username"
          className="mb-2 w-full input input-bordered"
        />
        <input
          required
          type="password"
          name="pass"
          placeholder="Password"
          className="mb-2 w-full input input-bordered"
        />
        <button className="w-full btn btn-primary">Login</button>
      </form>
    </div>
  )
}

export default Login
