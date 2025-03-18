<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const orders = ref([]);
const orderName = ref("");
const orderPrice = ref("");
const submittedOrder = ref(null);
const apiBaseUrl = "http://172.30.1.4:8082/api/v1"; // Change if needed

onMounted(() => {
  fetchOrder();
})

// Convert Euro input to cents (100 * price), handling both comma and dot
const convertToCents = (value) => {
  if (!value) return 0;
  const normalizedValue = value.replace(",", "."); // Convert comma to dot
  const floatValue = parseFloat(normalizedValue);
  return Math.round(floatValue * 100); // Convert to cents
};

// Convert cents back to euros (€)
const formatToEuros = (cents) => {
  return (cents / 100).toFixed(2).replace(".", ",") + " €"; // Display with comma
};

// Compute the total sum in cents
const totalSum = computed(() => {
  return orders.value.reduce((sum, order) => sum + order.price, 0);
});

// Add an item to the order list
const addOrder = () => {
  if (orderName.value && orderPrice.value) {
    const priceInCents = convertToCents(orderPrice.value);
    orders.value.push({
      name: orderName.value,
      price: priceInCents,
    });
    orderName.value = "";
    orderPrice.value = "";
  }
};

// Remove an item from the order list
const removeOrder = (index) => {
  orders.value.splice(index, 1);
};

// Send the order to the backend
const submitOrder = async () => {
  try {
    console.log("Current submitted order:", submittedOrder.value);
    if (submittedOrder.value?.ordered) {
      alert("Deine Bestellung wurde bereits aufgenommen, du kannst diese nicht mehr ändern");
      orders.value = [];
      return; // Stop execution
    } else {
      const response = await axios.post(`${apiBaseUrl}/guest-order`, { orders: orders.value }, { withCredentials: true });
      submittedOrder.value = response.data;
      orders.value = []; // Clear the form after submission
    }
  } catch (error) {
    console.error("Order submission failed:", error.response?.data || error.message);
  }
};

// Fetch user's order
const fetchOrder = async () => {
  try {
    const response = await axios.get(`${apiBaseUrl}/guest-order`, { withCredentials: true });
    submittedOrder.value = response.data;
    await console.log(await submittedOrder)
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
        <div>
          <div class="input-group mb-3">
            <input type="text" class="form-control" placeholder="Item Name" v-model="orderName" />
          </div>
          <div class="input-group mb-3">
            <input type="text" class="form-control" placeholder="Price (€)" v-model="orderPrice" />
            <button class="btn btn-secondary" @click="addOrder">Add</button>
          </div>
        </div>

        <!-- Orders List -->
        <ul class="list-group mb-3">
          <li v-for="(order, index) in orders" :key="index" class="list-group-item d-flex justify-content-between">
            <span>{{ order.name }}</span>
            <span class="fw-bold">{{ formatToEuros(order.price) }}</span>
            <button class="btn btn-danger btn-sm" @click="removeOrder(index)">Löschen</button>
          </li>
        </ul>

        <!-- Total Price Before Submission -->
        <div v-if="orders.length > 0" class="d-flex justify-content-between fw-bold p-2">
          <span>Total:</span>
          <span>{{ formatToEuros(totalSum) }}</span>
        </div>

        <!-- Submit Order Button -->
        <button class="btn btn-primary w-100 rounded-pill mt-3" @click="submitOrder" :disabled="orders.length === 0">
          Submit Order
        </button>

        <!-- Display Submitted Order -->
        <div v-if="submittedOrder" class="mt-4">
          <h4 class="text-center">Your Order</h4>
          <ul class="list-group">
            <li v-for="(order, index) in submittedOrder.orders" :key="index"
              class="list-group-item d-flex justify-content-between">
              <span>{{ order.name }}</span>
              <span class="fw-bold">{{ formatToEuros(order.price) }}</span>
            </li>
          </ul>
          <p class="text-center mt-3 fw-bold">Total: {{ formatToEuros(submittedOrder.total_price) }}</p>
          <div class="row text-center">
            <div class="col-sm-6">
              <div class="alert"
                :class="{ 'alert-danger': !submittedOrder.payed, 'alert-sucess': submittedOrder.payed }" role="alert">
                Bezahlt
              </div>
            </div>
            <div class="col-sm-6">
              <div class="alert"
                :class="{ 'alert-danger': !submittedOrder.ordered, 'alert-success': submittedOrder.ordered }"
                role="alert">
                Bestellt
              </div>
            </div>
          </div>
          <div v-if="submittedOrder && !submittedOrder.payed">
            <a :href="paypalLink" target="_blank" class="btn btn-primary w-100 rounded-pill mt-3">
              <i class="fa-brands fa-paypal"></i> Pay Now
            </a>
          </div>
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
  display: flex;
  align-items: center;
}

.list-group-item:nth-child(even) {
  background-color: #e9ecef;
}

.btn-danger {
  font-size: 12px;
  padding: 4px 8px;
  margin-left: 10px;
}
</style>
