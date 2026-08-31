/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        trust: {
          white: '#FFFFFF',
          gray: '#E5E5E5',
          orange: '#FCA311',
          navy: '#14213D',
          black: '#000000',
        },
      },
    },
  },
  plugins: [],
}
