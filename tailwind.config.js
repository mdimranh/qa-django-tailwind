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
        'alqalam': ['solaimanlipi', 'alqalam', 'allah'],
        'noorehidayat': ['solaimanlipi', 'noorehidayat'],
        'noorehira': ['solaimanlipi', 'noorehira'],
        'pdms': ['solaimanlipi','pdms'],
        'solaimanlipi': ['solaimanlipi'],
        "ayano": ['kfgq'],
        'amiri': ['solaimanlipi', 'amiri', 'allah'],
        "arabic": ['kfgq', 'qur_std', 'alqalam', 'noorehidayat', 'noorehira', 'pdms', 'solaimanlipi', 'amiri', 'allah'],
      },
    },
  },
  darkMode: 'class',
  plugins: [
    require("flowbite/plugin"),
  ],
}

