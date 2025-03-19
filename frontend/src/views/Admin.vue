<script setup>
import { useSessionStore } from "../store/sessionStore";
import AdminLogin from "../components/AdminLogin.vue";
import OrderOverview from "../components/OrderOverview.vue";

const sessionStore = useSessionStore();
</script>

<template>
  <div class="guest-container d-flex align-items-center justify-content-center">
    <AdminLogin v-if="!sessionStore.isAdminAuthenticated"/>
    <OrderOverview v-if="sessionStore.isAdminAuthenticated"/>
  </div>
</template>

<style scoped>
.guest-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  /* Light gradient background */
}
</style>
