/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['src/App.jsx', 'src/components/*'],
  daisyui: {
    themes: [
      'sunset',
      'forest',
      'retro',
      'light',
      'black',
      'pastel',
      'luxury',
      'nord',
    ],
  },
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
}
