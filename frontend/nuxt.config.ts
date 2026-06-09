export default defineNuxtConfig({
  modules: ["@nuxtjs/supabase", "@nuxtjs/tailwindcss"],

  supabase: {
    url: process.env.NUXT_PUBLIC_SUPABASE_URL ?? '',
    key: process.env.NUXT_PUBLIC_SUPABASE_ANON_KEY ?? '',
    redirect: false,
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || "http://localhost:5000",
    },
  },

  css: ["~/assets/css/main.css"],

  compatibilityDate: "2024-11-01",
});
