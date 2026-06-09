<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
      <NuxtLink to="/goals" class="text-sm text-blue-600 hover:underline">Edit goals</NuxtLink>
    </div>

    <template v-if="!pending">
      <MacroSummary v-if="goals" :totals="totals" :goals="goals" />
      <MealForm @logged="refresh" />
      <MealList :meals="meals" />
    </template>

    <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
interface Meal {
  id: string;
  name: string;
  protein: number;
  carbs: number;
  fat: number;
  calories: number;
  logged_at: string;
}

interface Goals {
  protein: number;
  carbs: number;
  fat: number;
  calories: number;
}

const { apiFetch } = useApi();
const error = ref("");

const { data, pending, refresh } = await useAsyncData(
  "dashboard",
  async () => {
    const [goalsRes, mealsRes] = await Promise.all([
      apiFetch<{ data: Goals | null }>("/api/goals"),
      apiFetch<{ data: Meal[] }>("/api/meals/today"),
    ]);
    return { goals: goalsRes.data, meals: mealsRes.data };
  },
  { server: false }
);

const goals = computed(() => data.value?.goals ?? null);
const meals = computed(() => data.value?.meals ?? []);

const totals = computed(() => {
  return meals.value.reduce(
    (acc, m) => ({
      protein: acc.protein + Number(m.protein),
      carbs: acc.carbs + Number(m.carbs),
      fat: acc.fat + Number(m.fat),
      calories: acc.calories + Number(m.calories),
    }),
    { protein: 0, carbs: 0, fat: 0, calories: 0 }
  );
});

watch(
  [data, pending],
  () => {
    if (!pending.value && data.value !== null && goals.value === null) {
      navigateTo("/goals");
    }
  },
  { immediate: true }
);
</script>
