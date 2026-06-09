<template>
  <div class="bg-white border border-gray-200 rounded-lg p-6 space-y-4">
    <h2 class="text-lg font-semibold text-gray-900">Today's Progress</h2>
    <div v-for="macro in macros" :key="macro.key" class="space-y-1">
      <div class="flex justify-between text-sm">
        <span class="font-medium text-gray-700">{{ macro.label }}</span>
        <span class="text-gray-500">{{ macro.consumed }} / {{ macro.goal }}{{ macro.unit }}</span>
      </div>
      <div class="w-full bg-gray-100 rounded-full h-2">
        <div
          class="h-2 rounded-full transition-all"
          :class="macro.pct >= 100 ? 'bg-green-500' : 'bg-blue-500'"
          :style="{ width: Math.min(macro.pct, 100) + '%' }"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface MacroTotals {
  protein: number;
  carbs: number;
  fat: number;
  calories: number;
}

const props = defineProps<{
  totals: MacroTotals;
  goals: MacroTotals;
}>();

const macros = computed(() => [
  { key: "protein", label: "Protein", unit: "g", consumed: props.totals.protein.toFixed(1), goal: props.goals.protein, pct: props.goals.protein > 0 ? (props.totals.protein / props.goals.protein) * 100 : 0 },
  { key: "carbs",   label: "Carbs",   unit: "g", consumed: props.totals.carbs.toFixed(1),   goal: props.goals.carbs,   pct: props.goals.carbs   > 0 ? (props.totals.carbs   / props.goals.carbs)   * 100 : 0 },
  { key: "fat",     label: "Fat",     unit: "g", consumed: props.totals.fat.toFixed(1),     goal: props.goals.fat,     pct: props.goals.fat     > 0 ? (props.totals.fat     / props.goals.fat)     * 100 : 0 },
  { key: "calories",label: "Calories",unit: "",  consumed: props.totals.calories.toFixed(0), goal: props.goals.calories, pct: props.goals.calories > 0 ? (props.totals.calories / props.goals.calories) * 100 : 0 },
]);
</script>
