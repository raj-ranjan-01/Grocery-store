<template>
  <nav>
    <div class="nav-item">
      <a href="/index" id="buyEasy"><b>buyEasy</b></a>
    </div>
    <div class="nav-item">
      <a href="/cart">Cart</a>
    </div>
    <div class="nav-item right">
      <form method="post">
        <input type="search" v-model="searchQuery" placeholder="Search" aria-label="Search" name="input">
        <button type="submit" v-on:click.prevent="searchProducts(searchQuery)">Search</button>
      </form>
    </div>
    <div class="nav-item">
      <a href="/">Logout</a>
    </div>
  </nav>


  <main>
    <div v-if="showSearchResults">
      <h2 id="category-name">Search Results</h2>
      <div v-for="result in searchResults" :key="result.id" class="card-whole">
        <!-- Display search results here -->
        <h5>Name: {{ result.name }}</h5>
        <h5>Price: Rs {{ result.rate }}/{{ result.unit }}</h5>
        <h5>Quantity: {{ result.quantity }}</h5>
        <div>
          <button class="update-button" type="Submit" @click="add_cart(result.id)">Add to Cart</button>
        </div>
      </div>
    </div>


    <div v-for="i in index.categories" :key="i.id">
      <h2 id="category-name">{{ i.name }}</h2>

      <section class="category">
        <div v-for="j in index.products" :key="j.id">
          <div v-if="j.category_id == i.id" class="card-whole">
            <img src="../assets/pngwing.com.png" alt="">
            <h5>Name: {{ j.name }}</h5>
            <h5>Price: Rs {{ j.rate }}/{{ j.unit }}</h5>
            <h5>Quatity: {{ j.quantity }}</h5>
            <div>
              <button class="update-button" type="Submit" @click="add_cart(j.id)">Add to Cart</button>
            </div>
          </div>
        </div>
      </section>

    </div>
  </main>

  <footer class="footer-div">
    @copyright 2023
  </footer>
</template>

<script>
import axios from 'axios'


export default {
  name: 'index',
  data() {
    return {
      index: {
        name: '',
        rate: '',
        quantity: '',
        unit: '',
        category: '',
        products: [],
        categories: [],
        cart: '',
      },
      searchQuery: null,
      showSearchResults: false,
      searchResults: [],
    }
  },
  mounted() {
    this.fetch_data();
  },
  methods: {
    async fetch_data() {
      try {
        const token = localStorage.getItem('token');
        const [productsResponse, categoriesResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/product',{ headers: { Authorization: `Bearer ${token}` }}),
          axios.get('http://127.0.0.1:5000/category',{ headers: { Authorization: `Bearer ${token}` }})
        ]);

        this.index.products = productsResponse.data;
        this.index.categories = categoriesResponse.data;
        console.log('Products:', this.index.products);
        console.log('Categories:', this.index.categories);
      }
      catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async add_cart(productId) {
      this.$router.push({ name: 'add_cart', params: { productId } })
    },
    async searchProducts() {
      try {
        const searchNumber = Number(this.searchQuery);
        if(isNaN(searchNumber)){
          const query = this.searchQuery.toLowerCase();
        this.searchResults = this.index.products.filter(product =>
          product.name.toLowerCase().includes(query)
        );
        this.showSearchResults = true;
        console.log(this.searchResults);

        }
        else{
          this.searchResults = this.index.products.filter(product =>
          product.rate == searchNumber
        );
        this.showSearchResults = true;
        console.log(this.searchQuery);

        }
      } catch (error) {
        console.error('Error searching products:', error);
      }
    },
  }
}
</script>

<style scoped src="../assets/css/styles_home.css"></style>
<style scoped src="../assets/css/styles_template.css"></style>