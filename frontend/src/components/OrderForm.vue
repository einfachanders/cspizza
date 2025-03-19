<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";

const orders = ref([]);
const orderName = ref("");
const orderPrice = ref("");
const submittedOrder = ref(null);

onMounted(async () => {
  await fetchOrder();
});

// Convert Euro input to cents (100 * price), handling both comma and dot
const convertToCents = (value) => {
  if (!value) return 0;
  const normalizedValue = value.replace(",", "."); // Convert comma to dot
  const floatValue = parseFloat(normalizedValue);
  return Math.round(floatValue * 100); // Convert to cents
};

// Convert cents back to euros (€)
const formatToEuros = (cents) => {
  return new Intl.NumberFormat("de-DE", {
    style: "currency",
    currency: "EUR",
  }).format(cents / 100);
};

// Compute the total sum in cents
const totalSum = computed(() => {
  return orders.value.reduce((sum, order) => sum + order.price, 0);
});

// Add an item to the order list
const addOrder = () => {
  if (!orderName.value.trim()) {
    alert("Item name cannot be empty!");
    return;
  }

  const priceInCents = convertToCents(orderPrice.value);
  if (isNaN(priceInCents) || priceInCents <= 0) {
    alert("Please enter a valid price!");
    return;
  }

  orders.value.push({
    name: orderName.value.trim(),
    price: priceInCents,
  });

  orderName.value = "";
  orderPrice.value = "";
};

// Remove an item from the order list
const removeOrder = (index) => {
  orders.value.splice(index, 1);
};

// Send the order to the backend
const submitOrder = async () => {
  try {
    if (submittedOrder.value?.ordered) {
      alert("You cannot modify an already submitted order.");
      return;
    }
    const response = await axios.post("/api/v1/guest-order", { orders: orders.value }, { withCredentials: true });
    submittedOrder.value = response.data;
    orders.value = [];
  } catch (error) {
    alert("Failed to submit order. Please try again.");
    console.error("Order submission error:", error);
  }
};

// Fetch user's order
const fetchOrder = async () => {
  try {
    const response = await axios.get("/api/v1/guest-order", { withCredentials: true });
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
        <div v-if="!submittedOrder">
          <h3 class="text-center mb-4">Bestellung aufgeben</h3>

          <!-- Order Input Fields -->
          <div>
            <div class="input-group mb-3">
              <input type="text" class="form-control" placeholder="Item Name" v-model="orderName" />
            </div>
            <div class="input-group mb-3">
              <input type="text" class="form-control" placeholder="Price (€)" v-model="orderPrice" />
              <button class="btn btn-secondary" @click="addOrder" :disabled="!orderName || !orderPrice">Add</button>
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
        </div>

        <!-- Display Submitted Order -->
        <div v-if="submittedOrder" class="mt-4">
          <h4 class="text-center">Deine Bestellung</h4>
          <ul class="list-group">
            <li v-for="(order, index) in submittedOrder.orders" :key="index"
              class="list-group-item d-flex justify-content-between">
              <span>{{ order.name }}</span>
              <span class="fw-bold">{{ formatToEuros(order.price) }}</span>
            </li>
          </ul>
          <p class="text-center mt-3 fw-bold">Gesamt: {{ formatToEuros(submittedOrder.total_price) }}</p>
          <div class="row text-center">
            <div class="col-sm-6">
              <div class="alert"
                :class="{ 'alert-danger': !submittedOrder.ordered, 'alert-success': submittedOrder.ordered }"
                role="alert">
                {{ submittedOrder.ordered ? 'Bestellt' : 'Noch nicht bestellt' }}
              </div>
            </div>
            <div class="col-sm-6">
              <div class="alert"
                :class="{ 'alert-danger': !submittedOrder.payed, 'alert-success': submittedOrder.payed }">
                {{ submittedOrder.payed ? 'Bezahlt' : 'Nicht bezahlt' }}
              </div>
            </div>
          </div>
          <div v-if="submittedOrder && !submittedOrder.payed">
            <a :href="`https://www.paypal.com/paypalme/b1tsheep/${(submittedOrder.total_price / 100).toFixed(2).replace('.', ',')}`"
              target="_blank" class="btn btn-primary w-100 rounded-pill mt-3">
              <i class="bi bi-paypal"></i> Mit Paypal bezahlen
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
