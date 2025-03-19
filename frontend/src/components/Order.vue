<script setup>
import { computed } from 'vue';

const props = defineProps({
    order: {
        type: Object,
        required: true,
        default: () => ({
            orders: [],
            total_price: 0,
            payed: false,
            ordered: false
        })
    }
});

const formatToEuros = (cents) => {
    return (cents / 100).toFixed(2).replace(".", ",") + " €";
};

const totalPrice = computed(() => formatToEuros(props.order?.total_price || 0));
</script>

<template>
    <div class="col-xl">
        <div class="card">
            <div class="card-body">
                <h4 id="order-title" class="text-center">{{ order.user_name }}</h4>
                <ul v-if="order?.orders?.length" class="list-group mt-3">
                    <li v-for="(item, index) in order.orders" :key="index"
                        class="list-group-item d-flex justify-content-between">
                        <span>{{ item.name }}</span>
                        <span class="fw-bold">{{ formatToEuros(item.price) }}</span>
                    </li>
                </ul>
                <p class="text-center m-3 fw-bold">Total: {{ totalPrice }}</p>
                <div class="row text-center m-3">
                    <div class="col-6">
                        <div class="alert" :class="{ 'alert-danger': !order.payed, 'alert-success': order.payed }"
                            role="status">
                            {{ order.payed ? 'Paid' : 'Not Paid' }}
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="alert" :class="{ 'alert-danger': !order.ordered, 'alert-success': order.ordered }"
                            role="status">
                            {{ order.ordered ? 'Ordered' : 'Not Ordered' }}
                        </div>
                    </div>
                </div>
            </div>
            <!-- <div class="m-3">
                <section aria-labelledby="order-title">
                    <h4 id="order-title" class="text-center">{{ order.user_name}}</h4>
                </section>
                <ul v-if="order?.orders?.length" class="list-group mt-3">
                    <li v-for="(item, index) in order.orders" :key="index"
                        class="list-group-item d-flex justify-content-between">
                        <span>{{ item.name }}</span>
                        <span class="fw-bold">{{ formatToEuros(item.price) }}</span>
                    </li>
                </ul>
                <p v-else class="text-center text-muted">No items in the order.</p>
            </div>
            <p class="text-center mb-3 fw-bold">Total: {{ totalPrice }}</p>
            <div class="row text-center m-3">
                <div class="col-sm-6">
                    <div class="alert" :class="{ 'alert-danger': !order.payed, 'alert-success': order.payed }"
                        role="status">
                        {{ order.payed ? 'Paid' : 'Not Paid' }}
                    </div>
                </div>
                <div class="col-sm-6">
                    <div class="alert" :class="{ 'alert-danger': !order.ordered, 'alert-success': order.ordered }"
                        role="status">
                        {{ order.ordered ? 'Ordered' : 'Not Ordered' }}
                    </div>
                </div>
            </div> -->
        </div>
    </div>
</template>

<style>
.card {
    min-width: 400px;
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