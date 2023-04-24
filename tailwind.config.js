/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./static/**/*.css",
    "./node_modules/flowbite/**/*.js",
    "./node_modules/flowbite/**/*.css"
  ],
  theme: {
    extend: {
      fontFamily: {
        'suraname' : ['suraname'],
        'suraname-color' : ['suraname-color'],
        'bismillah': ['bismillah'],
        'allah': ['allah'],
        'kfgq': ['solaimanlipi', 'kfgq', 'allah'],
        'qur_std': ['solaimanlipi', 'qur_std', 'allah'],
        'alqalam': ['alqalam', 'allah'],
        'noorehidayat': ['noorehidayat'],
        'noorehira': ['noorehira'],
        'pdms': ['pdms'],
        'solaimanlipi': ['solaimanlipi', 'kfgq'],
        'amiri': ['amiri', 'allah'],
        "arabic": ['kfgq', 'qur_std', 'alqalam', 'noorehidayat', 'noorehira', 'pdms', 'solaimanlipi', 'amiri', 'allah'],
      },
    },
  },
  darkMode: 'class',
  plugins: [
    require("flowbite/plugin"),
  ],
}

