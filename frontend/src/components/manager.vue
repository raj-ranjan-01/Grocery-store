<template>
  <nav>
    <div class="nav-item">
      <a href="#" id="buyEasy"><b>buyEasy</b></a>
    </div>
    <div class="nav-item">
      <a href="/add_product">Add Products</a>
    </div>
    <div class="nav-item right">
      <a href="/">Logout</a>
    </div>
  </nav>
  <div class="update-form">

    <h1 class="form-heading">Add Category</h1>

    <form method="post" enctype="multipart/form-data">

      <div class="form-item"> 
        <label for="name">Category name : </label>
        <input type="text" name="name" v-model="input.category_name">
      </div>
      <div class="form-item">
        <button class="update-button" type="Submit" v-on:click.prevent="add_category">Add</button>
      </div>
    </form>
    <table class="table">
      <thead>
        <th scope="col">ID</th>
        <th>Name</th>
        <th>Status</th>
      </thead>
      <tbody>
        <tr v-for="i in input.category" :key="i.id" scope="row">
          <td>{{ i.id }}</td>
          <td>{{ i.name }}</td>
          <td>{{ i.approved }}</td>
        </tr>
      </tbody>
    </table>
  </div>
  <footer class="footer-div">
    @copyright 2023
  </footer>
</template>

<script>
import axios from 'axios'
export default {
  name: 'manager',
  data() {
    return {
      input: {
        category_name: '',
        category:[]
      }
    }

  },
  mounted(){
    this.fetch_category();
  },
  methods: {
    async add_category() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/category', {
          name: this.input.category_name
        });
        console.log(response)
        window.location.reload();
      }
      catch (error) {
        console.log("something is wrong")
      }
    },
    async fetch_category() {
      const token = localStorage.getItem('token');
      axios.get('http://127.0.0.1:5000/category',{ headers: { Authorization: `Bearer ${token}` }})
        .then(response => {
          this.input.category = response.data;
          console.log(response.data)
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });

    }
  }
};
</script>
<style scoped>
@import '../assets/css/styles_add_product.css';
@import '../assets/css/styles_signup.css';
</style>
