/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["src/App.jsx", "src/components/*"],
  daisyui: {themes: ["sunset"]},
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
}

