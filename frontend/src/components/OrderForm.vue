<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useSessionStore } from "../store/sessionStore";

const orders = ref([]);
const orderName = ref("");
const orderPrice = ref("");
const submittedOrder = ref(null);
const apiBaseUrl = "http://localhost:8000/api/v1"; // Change this if needed

// Add an item to the order list
const addOrder = () => {
  if (orderName.value && orderPrice.value) {
    orders.value.push({
      name: orderName.value,
      price: parseInt(orderPrice.value),
    });
    orderName.value = "";
    orderPrice.value = "";
  }
};

// Send the order to the backend
const submitOrder = async () => {
  try {
    const response = await axios.post(`${apiBaseUrl}/guest-order`, { orders: orders.value }, { withCredentials: true });
    submittedOrder.value = response.data;
    orders.value = []; // Clear the form after submission
  } catch (error) {
    console.error("Order submission failed:", error.response?.data || error.message);
  }
};

// Fetch user's order
const fetchOrder = async () => {
  try {
    const response = await axios.get(`${apiBaseUrl}/guest-order`, { withCredentials: true });
    submittedOrder.value = response.data;
  } catch (error) {
    console.error("Fetching order failed:", error.response?.data || error.message);
  }
};
</script>

<template>
  <div class="container d-flex align-items-center justify-content-center">
    <div class="card shadow-lg p-4 rounded">
      <div class="card-body">
        <h3 class="text-center mb-4">Place Your Order</h3>

        <!-- Order Input Fields -->
        <div class="input-group mb-3">
          <input type="text" class="form-control rounded-pill" placeholder="Item Name" v-model="orderName" />
          <input type="number" class="form-control rounded-pill" placeholder="Price (€)" v-model="orderPrice" />
          <button class="btn btn-secondary rounded-pill" @click="addOrder">Add</button>
        </div>

        <!-- Orders List -->
        <ul class="list-group mb-3">
          <li v-for="(order, index) in orders" :key="index" class="list-group-item d-flex justify-content-between">
            <span>{{ order.name }}</span>
            <span class="fw-bold">€{{ order.price }}</span>
          </li>
        </ul>

        <!-- Submit Order Button -->
        <button class="btn btn-primary w-100 rounded-pill" @click="submitOrder">Submit Order</button>

        <!-- Display Submitted Order -->
        <div v-if="submittedOrder" class="mt-4">
          <h4 class="text-center">Your Order</h4>
          <ul class="list-group">
            <li v-for="(order, index) in submittedOrder.orders" :key="index" class="list-group-item d-flex justify-content-between">
              <span>{{ order.name }}</span>
              <span class="fw-bold">€{{ order.price }}</span>
            </li>
          </ul>
          <p class="text-center mt-3 fw-bold">Total: €{{ submittedOrder.total_price }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  width: 100%;
  max-width: 500px;
  border: none;
}

.input-group input {
  max-width: 45%;
}

.btn-secondary {
  background-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.list-group-item {
  border: none;
  padding: 10px;
  background-color: #f8f9fa;
}

.list-group-item:nth-child(even) {
  background-color: #e9ecef;
}
</style>