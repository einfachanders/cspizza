<script setup>
import { computed } from 'vue';
import axios from 'axios';

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

const emit = defineEmits(["update-order"]);

const formatToEuros = (cents) => {
    return (cents / 100).toFixed(2).replace(".", ",") + " €";
};

const totalPrice = computed(() => formatToEuros(props.order?.total_price || 0));

const toggleStatus = async (field) => {
    try {
        const updatedValue = !props.order[field];
        const response = await axios.patch(
            `/api/v1/orders/${props.order.order_id}`,
            { [field]: updatedValue },
            { withCredentials: true }
        );

        emit("update-order", { ...props.order, [field]: updatedValue });
    } catch (error) {
        console.error("Error updating order:", error);
    }
};
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
                        <button @click="toggleStatus('payed')" class="btn w-100"
                            :class="{ 'btn-danger': !order.payed, 'btn-success': order.payed }">
                            {{ order.payed ? 'Bezahlt' : 'Nicht bezahlt' }}
                        </button>
                    </div>
                    <div class="col-6">
                        <button @click="toggleStatus('ordered')" class="btn w-100"
                            :class="{ 'btn-danger': !order.ordered, 'btn-success': order.ordered }">
                            {{ order.ordered ? 'Bestellt' : 'Noch nicht bestellt' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.card {
    min-width: 400px;
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

.btn {
    font-size: 14px;
    padding: 8px 12px;
    border-radius: 5px;
}
</style>
