/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/*.html",
    "./static/src/**/*.js",    // any JS with classes
    "./**/*.py"                // if you have class names in Flask routes
  ],
  prefix: 'tw-',
  important: true,
  theme: {
    extend: {},
  },
  corePlugins: {
    preflight: false,
  },
  plugins: [],
}