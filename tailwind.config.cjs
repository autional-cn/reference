/** @type {import('tailwindcss').Config} */
// 原先这里内联了 primary/sky/amber 三套色阶、fontFamily 与 boxShadow，
// 与设计系统各写一份（ui 仓库 KI-010）。现改用内置的权威 preset：
//   packages/tailwind-preset/index.js，由 pnpm sync:consumers 生成，与权威逐字节一致。
// 调色板由 global.css 里 import 的 profile.css（profiles/docs.css）提供，与原先内联的一致。
module.exports = {
  content: ['./src/**/*.{astro,html,js,ts,jsx,tsx}'],
  presets: [require('./packages/tailwind-preset/index.js')],
  plugins: [],
};
