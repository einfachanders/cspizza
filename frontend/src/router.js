import { createRouter, createWebHistory } from 'vue-router'
import Guest from './views/Guest.vue'
import Admin from './views/Admin.vue'

const routes = [
  { path: '/', component: Guest },
  { path: '/admin', component: Admin },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router