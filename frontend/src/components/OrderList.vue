<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps(["orders", "formatToEuros"]);
const emit = defineEmits(["remove-order"]);
</script>

<template>
  <ul class="list-group mt-3">
    <li v-for="(order, index) in orders" :key="index" class="list-group-item d-flex justify-content-between">
      <span>{{ order.name }}</span>
      <span class="fw-bold">{{ formatToEuros(order.price) }}</span>
      <button class="btn btn-danger btn-sm" @click="emit('remove-order', index)">Löschen</button>
    </li>
  </ul>
</template>
