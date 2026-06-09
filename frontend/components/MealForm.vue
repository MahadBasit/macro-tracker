<template>
  <div class="bg-white border border-gray-200 rounded-lg p-6">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Log a Meal</h2>
    <form class="space-y-4" @submit.prevent="submit">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Meal name</label>
        <input
          v-model="form.name"
          type="text"
          required
          placeholder="e.g. Chicken and rice"
          class="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>
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
        {{ loading ? "Logging…" : "Log meal" }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{ logged: [] }>();
const { apiFetch } = useApi();
const error = ref("");
const loading = ref(false);

const form = reactive({ name: "", protein: 0, carbs: 0, fat: 0, calories: 0 });

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await apiFetch("/api/meals", {
      method: "POST",
      body: { ...form },
    });
    form.name = "";
    form.protein = 0;
    form.carbs = 0;
    form.fat = 0;
    form.calories = 0;
    emit("logged");
  } catch (e: any) {
    error.value = e?.data?.error ?? "Failed to log meal";
  } finally {
    loading.value = false;
  }
}
</script>
