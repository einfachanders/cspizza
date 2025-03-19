<script setup>
import { ref, onMounted } from 'vue';
import axios from "axios";
import Order from './Order.vue';

const orders = ref([]);

onMounted(() => {
    fetchOrders();
});

const fetchOrders = async () => {
    try {
        const response = await axios.get("/api/v1/orders", { withCredentials: true });
        orders.value = response.data;
    } catch (error) {
        console.error("Fetching orders failed:", error.response?.data || error.message);
    }
};

const updateOrder = (updatedOrder) => {
    const index = orders.value.findIndex(order => order.order_id === updatedOrder.order_id);
    if (index !== -1) {
        orders.value[index] = updatedOrder; // Update the order in the list
    }
};
</script>

<template>
    <div class="wrapper shadow-lg p-4 rounded">
        <div class="row">
            <Order 
                v-for="order in orders" 
                :key="order.order_id" 
                :order="order"
                @update-order="updateOrder" 
            />
        </div>
    </div>
</template>

<style>
.card {
    width: 100%;
    max-width: 400px;
    border: none;
}
</style>
