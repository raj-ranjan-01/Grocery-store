<template>
    <nav>
    <div class="nav-item">
      <a href="/index" id="buyEasy"><b>buyEasy</b></a>
    </div>
    <div class="nav-item">
      <a href="/cart">Cart</a>
    </div>
    <div class="nav-item right">
      <form method="post" action="/index">
        <input type="search" placeholder="Search" aria-label="Search" name="input">
        <button type="submit">Search</button>
      </form>
    </div>
    <div class="nav-item">
      <a href="/">Logout</a>
    </div>
  </nav>
  <main>
      <div class="update-form">
        <h1 class="form-heading">Add to Cart</h1>

        <form @submit.prevent="addToCart">

          <div class="form-item">
            <label for="name">Item name : {{ show.item_name }}</label>
          </div>

          <div class="form-item">
            <label for="rate">Rate : {{ show.rate }}</label>
          </div>

          <template v-if="show.stock == 0">
            <div class="form-item">
              <h3>Out of stock</h3>
            </div>
          </template>

          <template v-else>
            <div class="form-item">
              <label for="quantity">In stock : {{ show.stock }} </label>
            </div>
            <div class="form-item">
              <label for="unit">Buy(In {{ show.unit }}): </label>
              <input type="number" v-model="show.buy" name="quantity" />
            </div>
            <div class="form-item">
                <button class="update-button" type="Submit" @click="send_cart()">Add</button>
            </div>
          </template>

        </form>
      </div>
    </main>
</template>

<script>
import axios from 'axios';

export default{
    name:'add_cart',
    data() {
    return {
      show: {
        item_name:'',
        rate:0,
        stock:0,
        unit:'',
        buy:0,
        product_id:0
    }
    }
    },
    mounted(){
        const productId = this.$route.params.productId;
        this.show.product_id=productId
        this.fetchProductDetails(productId);
    },
    methods: {
    fetchProductDetails(productId) {
         axios.get(`http://127.0.0.1:5000/add_cart?id=${productId}`)
        .then(response => {
            this.show.item_name=response.data.name;
            this.show.rate=response.data.rate;
            this.show.stock=response.data.quantity;
            this.show.unit=response.data.unit;
            console.log(this.show.product)
          })
          .catch(error => {
            console.error('Error fetching categories:', error);
          });
    },
    send_cart(){
      const customerId = localStorage.getItem('user_id')
        const response=axios.post('http://127.0.0.1:5000/add_cart',{
            customer_id:customerId,
            product_id:this.show.product_id,
            item_name:this.show.item_name,
            quantity:this.show.buy,
            rate:this.show.rate
        })
        if(response){
            this.$router.push({ name :'index'})
        }
        else{
            console.log("error")
        }
    }
}
};
</script>
<style scoped src="../assets/css/styles_home.css"></style>
<style scoped src="../assets/css/styles_template.css"></style>
