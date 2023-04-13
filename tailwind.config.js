/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./static/**/*.css",
    "./node_modules/flowbite/**/*.js",
    "./node_modules/flowbite/**/*.css"
  ],
  theme: {
    extend: {},
  },
  darkMode: 'class',
  plugins: [
    require("flowbite/plugin"),
  ],
}

