<script setup>
import { ref } from "vue";
import { useSessionStore } from "../store/sessionStore";
import OrderForm from "../components/OrderForm.vue";
import GuestLogin from "../components/GuestLogin.vue";

const sessionStore = useSessionStore();

// Guest Login
const userName = ref("");
const userEmail = ref("");
const orderCode = ref("");

const handleLogin = async (event) => {
  event.preventDefault(); // Prevent form submission default behavior
  console.log("Login function triggered");
  console.log("Name:", userName.value);
  console.log("Email:", userEmail.value);
  console.log("Order Code:", orderCode.value);

  await sessionStore.login(userName.value, userEmail.value, orderCode.value);
};
</script>

<template>
  <div class="guest-container d-flex align-items-center justify-content-center">
    <GuestLogin v-if="!sessionStore.isGuestAuthenticated"/>
    <OrderForm v-if="sessionStore.isGuestAuthenticated"/>
  </div>
</template>

<style scoped>
.guest-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  /* Light gradient background */
}

.card {
  width: 100%;
  max-width: 400px;
  border: none;
}

.form-control {
  transition: all 0.3s ease-in-out;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 10px rgba(0, 123, 255, 0.3);
}

.btn-primary {
  background-color: #007bff;
  border: none;
  transition: 0.3s;
}

.btn-primary:hover {
  background-color: #0056b3;
}
</style>
