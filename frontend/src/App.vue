<script setup>
import { ref } from "vue";
import axios from "axios";

const backendUrl = "http://127.0.0.1:8082/api"; // Change this if needed

// Guest Login
const userName = ref("");
const userEmail = ref("");
const isLoggedIn = ref(false);
const orderSubmitted = ref(false);

const loginAsGuest = async () => {
  try {
    await axios.post(`${backendUrl}/v1/guest-login`, {
      user_name: userName.value,
      user_email: userEmail.value,
    }, { withCredentials: true });

    isLoggedIn.value = true;
    alert("Guest login successful!");
  } catch (error) {
    console.error("Login failed:", error);
    alert("Login failed!");
  }
};

// Ordering
const orderName = ref("");
const orderPrice = ref("");
const orders = ref([]);
const submittedOrder = ref(null);

const addOrder = () => {
  if (!orderName.value || !orderPrice.value || orderSubmitted.value) return;
  
  // Replace comma with dot for decimal parsing
  const normalizedPrice = orderPrice.value.replace(",", ".");
  
  if (isNaN(normalizedPrice)) return;
  
  orders.value.push({ name: orderName.value, price: Math.round(parseFloat(normalizedPrice) * 100) });
  orderName.value = "";
  orderPrice.value = "";
};

const placeOrder = async () => {
  try {
    const response = await axios.post(`${backendUrl}/v1/guest-order`, {
      orders: orders.value,
    }, { withCredentials: true });

    submittedOrder.value = {
      order_id: response.data.order_id,
      orders: response.data.orders,
      total_price: (response.data.total_price / 100).toFixed(2), // Convert cents to euros
      ordered: response.data.ordered,
      payed: response.data.payed,
    };
    orders.value = [];
    orderSubmitted.value = true;
  } catch (error) {
    console.error("Order failed:", error);
    alert("Order submission failed!");
  }
};
</script>

<template>
  <div class="container">
    <h1>🍕 Bitsheep Pizza Delivery</h1>

    <div v-if="!isLoggedIn">
      <h2>Guest Login</h2>
      <input v-model="userName" placeholder="Your Name" />
      <input v-model="userEmail" placeholder="Your Email" type="email" />
      <button @click="loginAsGuest">Login as Guest</button>
    </div>

    <div v-else>
      <div v-if="!orderSubmitted">
        <h2>Place Your Order</h2>
        <input v-model="orderName" placeholder="Pizza Name" />
        <input v-model="orderPrice" placeholder="Price (EUR)" type="text" />
        <button @click="addOrder">Add Pizza</button>

        <h3>Current Order</h3>
        <ul>
          <li v-for="(order, index) in orders" :key="index">
            {{ order.name }} - €{{ (order.price / 100).toFixed(2) }}
          </li>
        </ul>

        <button @click="placeOrder" :disabled="orders.length === 0">
          Submit Order
        </button>
      </div>

      <div v-if="submittedOrder">
        <h3>Order Confirmation</h3>
        <p>Order ID: {{ submittedOrder.order_id }}</p>
        <p>Total Price: €{{ submittedOrder.total_price }}</p>
        <p>Status: {{ submittedOrder.ordered ? 'Ordered' : 'Not Ordered' }}</p>
        <p>Payment: {{ submittedOrder.payed ? 'Paid' : 'Not Paid' }}</p>
        <h4>Ordered Items:</h4>
        <ul>
          <li v-for="(order, index) in submittedOrder.orders" :key="index">
            {{ order.name }} - €{{ (order.price / 100).toFixed(2) }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 500px;
  margin: 20px auto;
  text-align: center;
  font-family: Arial, sans-serif;
}

input {
  display: block;
  width: 100%;
  padding: 8px;
  margin: 5px 0;
}

button {
  padding: 8px 12px;
  margin: 10px 0;
  cursor: pointer;
}
</style>