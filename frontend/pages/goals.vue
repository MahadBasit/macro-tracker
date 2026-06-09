<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Daily Goals</h1>
    <form class="space-y-4 bg-white border border-gray-200 rounded-lg p-6" @submit.prevent="saveGoals">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Protein (g)</label>
          <input
            v-model.number="form.protein"
            type="number"
            min="0"
            step="any"
            required
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Carbs (g)</label>
          <input
            v-model.number="form.carbs"
            type="number"
            min="0"
            step="any"
            required
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Fat (g)</label>
          <input
            v-model.number="form.fat"
            type="number"
            min="0"
            step="any"
            required
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Calories</label>
          <input
            v-model.number="form.calories"
            type="number"
            min="0"
            step="any"
            required
            class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>
      <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
      <button
        type="submit"
        :disabled="loading"
        class="w-full bg-blue-600 text-white py-2 px-4 rounded-md text-sm font-medium hover:bg-blue-700 disabled:opacity-50"
      >
        {{ loading ? "Saving…" : "Save goals" }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
const { apiFetch } = useApi();
const error = ref("");
const loading = ref(false);

const form = reactive({ protein: 0, carbs: 0, fat: 0, calories: 0 });

onMounted(async () => {
  try {
    const res = await apiFetch<{ data: { protein: number; carbs: number; fat: number; calories: number } | null }>("/api/goals");
    if (res.data) {
      form.protein = res.data.protein;
      form.carbs = res.data.carbs;
      form.fat = res.data.fat;
      form.calories = res.data.calories;
    }
  } catch {
    // no existing goals — form stays at defaults
  }
});

async function saveGoals() {
  error.value = "";
  loading.value = true;
  try {
    await apiFetch("/api/goals", {
      method: "POST",
      body: { protein: form.protein, carbs: form.carbs, fat: form.fat, calories: form.calories },
    });
    await navigateTo("/");
  } catch (e: any) {
    error.value = e?.data?.error ?? "Failed to save goals";
  } finally {
    loading.value = false;
  }
}
</script>
