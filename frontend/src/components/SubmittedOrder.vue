<script setup>
import { defineProps } from "vue";
import OrderStatus from "./OrderStatus.vue";

const props = defineProps(["submittedOrder", "formatToEuros"]);
</script>

<template>
  <div v-if="submittedOrder" class="mt-4">
    <h4 class="text-center">Deine Bestellung</h4>
    <ul class="list-group mt-3">
      <li v-for="(order, index) in submittedOrder.orders" :key="index" class="list-group-item d-flex justify-content-between">
        <span>{{ order.name }}</span>
        <span class="fw-bold">{{ formatToEuros(order.price) }}</span>
      </li>
    </ul>
    <p class="text-center mt-2 fw-bold">Gesamt: {{ formatToEuros(submittedOrder.total_price) }}</p>

    <OrderStatus :ordered="submittedOrder.ordered" :payed="submittedOrder.payed" />

    <div v-if="!submittedOrder.payed">
      <a :href="`https://www.paypal.com/paypalme/b1tsheep/${(submittedOrder.total_price / 100).toFixed(2).replace('.', ',')}`"
        target="_blank" class="btn btn-primary w-100 rounded-pill mt-3">
        <i class="bi bi-paypal"></i> Mit Paypal bezahlen
      </a>
    </div>
  </div>
</template>
