<template>
  <div class="max-w-sm mx-auto mt-16">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Create account</h1>
    <div v-if="success" class="bg-green-50 border border-green-200 rounded-md p-4 text-sm text-green-800">
      Account created! <NuxtLink to="/login" class="underline font-medium">Sign in</NuxtLink>
    </div>
    <form v-else class="space-y-4" @submit.prevent="signup">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
        <input
          v-model="email"
          type="email"
          required
          class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          required
          minlength="6"
          class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
      <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-blue-600 text-white py-2 px-4 rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {{ loading ? "Creating account…" : "Create account" }}
      </button>
    </form>
    <p class="mt-4 text-sm text-gray-600">
      Already have an account?
      <NuxtLink to="/login" class="text-blue-600 hover:underline">Sign in</NuxtLink>
    </p>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "default" });

const supabase = useSupabaseClient();
const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const success = ref(false);

async function signup() {
  error.value = "";
  loading.value = true;
  const { error: authError } = await supabase.auth.signUp({
    email: email.value,
    password: password.value,
  });
  loading.value = false;
  if (authError) {
    error.value = authError.message;
  } else {
    success.value = true;
  }
}
</script>
