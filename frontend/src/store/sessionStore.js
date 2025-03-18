import { defineStore } from "pinia";
import axios from "axios";

export const useSessionStore = defineStore("session", {
  state: () => ({
    isGuestAuthenticated: false, // Make sure you use the correct state property
    isAdminAuthenticated: false,
    orders: [], // Add orders to state if needed
  }),
  actions: {
    async checkGuestSession() {
      try {
        const response = await axios.get("/api/v1/guest-order", { withCredentials: true });
        if (response.status === 200) {
          this.isGuestAuthenticated = true; // Use the correct state property
          // this.orders = response.data; // Ensure 'orders' is defined in state
        }
      } catch (error) {
        this.isGuestAuthenticated = false;
      }
    },

    async checkAdminSession() {
      try {
        const response = await axios.get("/api/v1/orders", { withCredentials: true });
        if (response.status === 200) {
          this.isAdminAuthenticated = true; // Use the correct state property
          // this.orders = response.data; // Ensure 'orders' is defined in state
        }
      } catch (error) {
        this.isAdminAuthenticated = false;
      }
    },

    async login(userName, userEmail, orderCode) {
      try {
        await axios.post(
          "/api/v1/guest-login",
          { user_name: userName, user_email: userEmail, order_code: orderCode },
          { withCredentials: true }
        );
        this.isGuestAuthenticated = true;
        // await this.checkGuestSession();
      } catch (error) {
        console.log(error)
        alert("Login failed!");
      }
    },

    async adminLogin(userName, userEmail, adminToken) {
      try {
        await axios.post(
          "/api/v1/admin-login",
          { user_name: userName, user_email: userEmail, admin_token: adminToken },
          { withCredentials: true }
        );
        this.isAdminAuthenticated = true;
        // await this.checkGuestSession();
      } catch (error) {
        console.log(error)
        alert("Login failed!");
      }
    },
  },
});
