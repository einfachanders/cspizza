import { createApp } from 'vue';
import { createPinia } from "pinia";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap';
// import './style.css';
import App from './App.vue';
import router from './router';
import axios from "axios";

axios.defaults.baseURL = "http://172.30.1.4:8082";
axios.defaults.withCredentials = true;

const app = createApp(App)
app.use(createPinia());
app.use(router)
app.mount('#app')
