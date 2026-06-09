<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
      <NuxtLink to="/" class="text-lg font-semibold text-gray-900">Macro Tracker</NuxtLink>
      <div v-if="user" class="flex items-center gap-4">
        <span class="text-sm text-gray-600">{{ user.email }}</span>
        <button
          class="text-sm text-red-600 hover:text-red-800 font-medium"
          @click="logout"
        >
          Logout
        </button>
      </div>
    </nav>
    <main class="max-w-2xl mx-auto px-4 py-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
const supabase = useSupabaseClient();
const user = useSupabaseUser();

async function logout() {
  await supabase.auth.signOut();
  await navigateTo("/login");
}
</script>
