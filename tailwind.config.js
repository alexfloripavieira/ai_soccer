/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './**/*.py'
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#10b981',
          500: '#10b981',
          600: '#059669'
        },
        secondary: {
          DEFAULT: '#3b82f6',
          500: '#3b82f6',
          600: '#2563eb'
        }
      }
    }
  },
  darkMode: 'class',
  plugins: []
}
