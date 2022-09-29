/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./downloader/templates/**/*.html",
    "./downloader/static/src/**/*.js"
  ],
  theme: {
    extend: {
      fontFamily:{
        'bebas-neue': ["Bebas Neue", 'cursive'],
      },
    },
  },
  plugins: [],
}
