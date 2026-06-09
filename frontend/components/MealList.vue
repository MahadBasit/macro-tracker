<template>
  <div class="bg-white border border-gray-200 rounded-lg p-6">
    <h2 class="text-lg font-semibold text-gray-900 mb-4">Today's Meals</h2>
    <p v-if="meals.length === 0" class="text-sm text-gray-500">No meals logged yet.</p>
    <ul v-else class="divide-y divide-gray-100">
      <li v-for="meal in meals" :key="meal.id" class="py-3 flex justify-between items-start">
        <div>
          <p class="text-sm font-medium text-gray-900">{{ meal.name }}</p>
          <p class="text-xs text-gray-500 mt-0.5">
            P: {{ meal.protein }}g · C: {{ meal.carbs }}g · F: {{ meal.fat }}g
          </p>
        </div>
        <span class="text-sm font-medium text-gray-700">{{ meal.calories }} kcal</span>
      </li>
    </ul>
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

defineProps<{ meals: Meal[] }>();
</script>
