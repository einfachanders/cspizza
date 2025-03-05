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
  },
});

    // async login(userName, userEmail, orderCode) {
    //   try {
    //     await axios.post(
    //       "/api/v1/guest-login",
    //       { user_name: userName, user_email: userEmail, order_code: orderCode },
    //       { withCredentials: true }
    //     );
    //     this.isAuthenticated = true;
    //     await this.checkSession();
    //   } catch (error) {
    //     alert("Login failed!");
    //   }
    // },

    // async submitOrder(orderItems) {
    //   const orders = orderItems.map((item) => ({
    //     name: item.name,
    //     price: Math.round(item.price * 100), // Convert to cents
    //   }));

    //   try {
    //     const response = await axios.post(
    //       "/api/v1/guest-order",
    //       { orders },
    //       { withCredentials: true }
    //     );
    //     this.orders = response.data.orders;
    //     this.totalPrice = response.data.total_price / 100;
    //   } catch (error) {
    //     alert("Order submission failed!");
    //   }
    // },
//   },
// });