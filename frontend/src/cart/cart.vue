<template>
  <nav>
    <div class="nav-item">
      <a href="/index" id="buyEasy"><b>buyEasy</b></a>
    </div>
    <div class="nav-item">
      <a href="/cart">Cart</a>
    </div>
    <div class="nav-item">
      <a href="/">Logout</a>
    </div>
  </nav>
  <main>
    <div class="cart">
      <table class="table">
        <thead>
          <th scope="col">Item Name</th>
          <th>Quantity</th>
          <th>Price</th>
          <th>Total</th>
          <th>To Do</th>
        </thead>
        <tbody>
          <tr v-for="i in cart.items" :key="i.id" scope="row">
            <td>{{ i.name }}</td>
            <td>{{ i.quantity }}</td>
            <td>{{ i.rate }}</td>
            <td>{{ i.quantity * i.rate }}</td>
            <td>
              <button @click="delete_cart(i.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div style="text-align: center;">
      <div class="total buy-all">Total Amount:{{ cartTotal }}
      </div>
      <button @click="purchased_cart()">Buy</button>
    </div>

  </main>
</template>

<script>
import axios from 'axios';
export default {
  name: 'cart',
  data() {
    return {
      cart: {
        items: [],
        sum: 0,
      }
    }
  },
  mounted() {
    this.fetch_cart();
  },

  methods: {
    async fetch_cart() {
      const user_id = localStorage.getItem('user_id')
      axios.get(`http://127.0.0.1:5000/cart?id=${user_id}`)
        .then(response => {
          this.cart.items = response.data;
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });
    },
    async delete_cart(id) {
      axios.delete(`http://127.0.0.1:5000/cart?id=${id}`)
        .then(response => {
          if (response.status === 200) {
            this.fetch_cart();
          }
        })
        .catch(error => {
          console.error('Error deleting item:', error);
        });
    },
    async purchased_cart() {
      try {
        const customerId = localStorage.getItem('user_id')
        const response = await axios.post('http://127.0.0.1:5000/cart', {
          amount:this.cartTotal,customer_id:customerId
        });
        console.log('Purchase successful:', response.data);
        window.location.reload();
      } 
      catch(error) {
      console.error('Error purchasing cart:', error);
    }
  }
},
computed: {
  cartTotal() {
    // Calculate the total sum of the cart
    return this.cart.items.reduce((sum, item) => sum + item.quantity * item.rate, 0);
  }
}
};
</script>
<style scoped>
@import '../assets/css/styles_add_product.css';
@import '../assets/css/styles_signup.css';
</style>
