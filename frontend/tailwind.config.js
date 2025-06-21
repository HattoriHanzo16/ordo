/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0fdfc',
          100: '#ccfbf1',
          200: '#99f6e4',
          300: '#5eedd8',
          400: '#2dd4bf',
          500: '#25c5bb',
          600: '#0d9488',
          700: '#0f766e',
          800: '#115e59',
          900: '#134e4a',
        },
        secondary: {
          50: '#fefcf3',
          100: '#fef7e6',
          200: '#fdecc6',
          300: '#fbdc9d',
          400: '#f9cb72',
          500: '#f9f4e9',
          600: '#d69e2e',
          700: '#b7791f',
          800: '#975a16',
          900: '#744210',
        },
        dark: {
          50: '#f6f7f7',
          100: '#e1e5e5',
          200: '#c3cccd',
          300: '#9eabac',
          400: '#7a8a8c',
          500: '#5f7274',
          600: '#4a5a5c',
          700: '#3d4a4c',
          800: '#323e40',
          900: '#042428',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
} 