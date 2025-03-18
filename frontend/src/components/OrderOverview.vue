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
</script>

<template>
    <!-- <div class="row">
            <Order v-for="order in orders" :key="order.id" :order="order" />
        </div> -->
    <div class="card" style="width: 18rem;">
        <img class="card-img-top" src="..." alt="Card image cap">
        <div class="card-body">
            <h5 class="card-title">Card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's
                content.</p>
            <a href="#" class="btn btn-primary">Go somewhere</a>
        </div>
    </div>
</template>

<style>
.wrapper {
    width: 100%;
    max-width: 100%;
}

.card {
    width: 100%;
    max-width: 400px;
    border: none;
}
</style>