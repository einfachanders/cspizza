import { createApp } from 'vue';
import { createPinia } from "pinia";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap';
// import './style.css';
import App from './App.vue';
import router from './router';
import axios from "axios";

axios.defaults.baseURL = import.meta.env.VITE_API_HOST;
axios.defaults.withCredentials = true;

const app = createApp(App)
app.use(createPinia());
app.use(router)
app.mount('#app')
