import { useNavigate } from 'react-router'

const Register = ({ api, setAuth }) => {
  let navigate = useNavigate()

  return (
    <div className="p-4 rounded-lg border w-fit h-fit border-base-300 bg-neutral text-neutral-content">
      <h2 className="mb-2 text-xl font-bold">Register</h2>
      <form
        onSubmit={async (e) => {
          e.preventDefault()
          const { name, pass } = e.target.elements

          try {
            const res = await api.post('/createAccount', {
              name: name.value,
              pass: pass.value,
            })

            console.log(res)
            if (res.status === 200) {
              console.log('Account created for ' + name.value)
              navigate('/login')
            } else {
              console.log(res.data)
            }
          } catch (err) {
            console.log('Registration failed:', err)
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
        <button className="w-full btn btn-primary">Register</button>
      </form>
    </div>
  )
}

export default Register
