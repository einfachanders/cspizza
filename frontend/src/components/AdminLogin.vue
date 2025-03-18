<script setup>
import { ref, onMounted } from "vue";
import { useSessionStore } from "../store/sessionStore";

const sessionStore = useSessionStore();

// Admin Login
const userName = ref("");
const userEmail = ref("");
const adminToken = ref("");

onMounted(() => {
  sessionStore.checkAdminSession();
})

const handleLogin = async (event) => {
  event.preventDefault(); // Prevent form submission default behavior
  console.log("Login function triggered");
  console.log("Name:", userName.value);
  console.log("Email:", userEmail.value);
  console.log("Admin Token:", adminToken.value);

  await sessionStore.adminLogin(userName.value, userEmail.value, adminToken.value);
};
</script>

<template>
    <div class="card shadow-lg p-4 rounded">
      <div class="card-body">
        <h3 class="text-center mb-4">Admin Login</h3>
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
            <label for="inputCode" class="form-label">Admin Token</label>
            <input type="password" class="form-control rounded-pill" id="inputCode" v-model="adminToken" required>
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
