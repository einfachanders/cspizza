<script setup>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import OrderForm from "./OrderForm.vue";
import OrderList from "./OrderList.vue";
import OrderSummary from "./OrderSummary.vue";
import SubmittedOrder from "./SubmittedOrder.vue";

const orders = ref([]);
const submittedOrder = ref(null);

onMounted(async () => {
    await fetchOrder();
});

const formatToEuros = (cents) => {
    return new Intl.NumberFormat("de-DE", { style: "currency", currency: "EUR" }).format(cents / 100);
};

const totalSum = computed(() => orders.value.reduce((sum, order) => sum + order.price, 0));

const addOrder = (order) => {
    orders.value.push(order);
};

const removeOrder = (index) => {
    orders.value.splice(index, 1);
};

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
    }
};

const fetchOrder = async () => {
    try {
        const response = await axios.get("/api/v1/guest-order", { withCredentials: true });
        submittedOrder.value = response.data;
    } catch (error) {
        console.error("Fetching order failed:", error);
    }
};
</script>

<template>
    <div class="container d-flex align-items-center justify-content-center">
        <div class="card shadow-lg p-4 rounded">
            <div class="card-body">
                <OrderForm v-if="!submittedOrder" @add-order="addOrder" />
                <OrderList v-if="!submittedOrder" :orders="orders" :formatToEuros="formatToEuros"
                    @remove-order="removeOrder" />
                <OrderSummary v-if="!submittedOrder" :totalSum="totalSum" :formatToEuros="formatToEuros" />
                <button v-if="!submittedOrder" class="btn btn-primary w-100 rounded-pill mt-2" @click="submitOrder"
                    :disabled="orders.length === 0">Bestellung aufgeben</button>
                <SubmittedOrder v-if="submittedOrder" :submittedOrder="submittedOrder" :formatToEuros="formatToEuros" />
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
</style>