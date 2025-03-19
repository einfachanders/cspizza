<script setup>
import { defineProps } from "vue";

defineProps(["totalSum", "formatToEuros"]);
</script>

<template>
  <div v-if="totalSum > 0" class="d-flex justify-content-between fw-bold p-2 mt-2">
    <span>Total:</span>
    <span>{{ formatToEuros(totalSum) }}</span>
  </div>
</template>
