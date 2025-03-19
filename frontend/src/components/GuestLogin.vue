<script setup>
import { ref, onMounted } from "vue";
import { useSessionStore } from "../store/sessionStore";

const sessionStore = useSessionStore();

// Guest Login
const userName = ref("");
const userEmail = ref("");
const orderCode = ref("");

onMounted(() => {
  sessionStore.checkGuestSession();
})

const handleLogin = async (event) => {
  event.preventDefault(); // Prevent form submission default behavior

  await sessionStore.login(userName.value, userEmail.value, orderCode.value);
};
</script>

<template>
  <div class="card shadow-lg p-4 rounded">
    <div class="card-body">
      <h3 class="text-center mb-4">Gast Login</h3>
      <form @submit="handleLogin">
        <div class="mb-3">
          <label for="inputName" class="form-label">Name</label>
          <input type="text" class="form-control rounded-pill" id="inputName" v-model="userName" required>
        </div>
        <div class="mb-3">
          <label for="inputEmail" class="form-label">Email Adresse</label>
          <input type="email" class="form-control rounded-pill" id="inputEmail" v-model="userEmail" required>
        </div>
        <div class="mb-3">
          <label for="inputCode" class="form-label">Bestellcode</label>
          <input type="password" class="form-control rounded-pill" id="inputCode" v-model="orderCode" required>
        </div>
        <button type="submit" class="btn btn-primary w-100 rounded-pill">Login</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.card {
  width: 100%;
  max-width: 400px;
  border: none;
}
</style>
