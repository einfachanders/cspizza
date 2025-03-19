<script setup>
import { ref, defineEmits } from "vue";

const orderName = ref("");
const orderPrice = ref("");

const emit = defineEmits(["add-order"]);

const addOrder = () => {
  if (!orderName.value.trim()) {
    alert("Item name cannot be empty!");
    return;
  }

  const priceInCents = parseFloat(orderPrice.value.replace(",", ".")) * 100;
  if (isNaN(priceInCents) || priceInCents <= 0) {
    alert("Please enter a valid price!");
    return;
  }

  emit("add-order", { name: orderName.value.trim(), price: priceInCents });

  orderName.value = "";
  orderPrice.value = "";
};
</script>

<template>
  <div>
    <h3 class="text-center mb-4">Bestellung aufgeben</h3>
    <div class="input-group">
      <input type="text" class="form-control" placeholder="Item Name" v-model="orderName" />
    </div>
    <div class="input-group mt-3">
      <input type="text" class="form-control" placeholder="Price (€)" v-model="orderPrice" />
      <button class="btn btn-secondary" @click="addOrder" :disabled="!orderName || !orderPrice">Add</button>
    </div>
  </div>
</template>
