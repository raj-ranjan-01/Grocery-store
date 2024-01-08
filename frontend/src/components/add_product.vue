<template>
  <nav>
    <div class="nav-item">
      <a href="#" id="buyEasy"><b>buyEasy</b></a>
    </div>
    <div class="nav-item">
      <a href="/manager">Categories</a>
    </div>
    <div class="nav-item right">
      <a href="/">Logout</a>
    </div>
  </nav>
  

    <div class="update-form">
      <h1 class="form-heading">Add Product</h1>

      <form enctype="multipart/form-data">

        <div class="form-item">
          <label for="name">Item name : </label>
          <input type="text" name="name" v-model="product.name">
        </div>

        <div class="form-item">
          <label for="rate">Rate : </label>
          <input type="number" name="rate" v-model="product.rate">
        </div>

        <div class="form-item">
          <label for="quantity">Quantity : </label>
          <input type="number" name="quantity" v-model="product.quantity" />
        </div>
        <div class="form-item">
          <label for="unit">Units: </label>
          <select name="unit" v-model="product.unit">
            <option value="Kg">Kg</option>
            <option value="Piece">Piece</option>
          </select>
        </div>


        <div class="form-item">
          <label for="category">Category :</label>

          <select name="category" v-model="product.category">
            <!-- eslint-disable vue/valid-v-for -->
            <option v-for="approvedCategory in approvedCategories" :value="approvedCategory.id" :key="approvedCategory.id">
              {{ approvedCategory.name }}
            </option>
          </select>
        </div>
        <div class="form-item">
          <button class="update-button" type="Submit" @click="send_data()">Add</button>
        </div>
      </form>
  </div>

  <div class="update-form">
    <div v-if="isEditing" class="edit-form">
      <h1 class="form-heading">Edit Product</h1>
      <form enctype="multipart/form-data">
        <div class="form-item">
          <label for="name">Item name : </label>
          <input type="text" name="name" v-model="edit.name">
        </div>

        <div class="form-item">
          <label for="rate">Rate : </label>
          <input type="number" name="rate" v-model="edit.rate">
        </div>

        <div class="form-item">
          <label for="quantity">Quantity : </label>
          <input type="number" name="quantity" v-model="edit.quantity" />
        </div>
        <div class="form-item">
          <label for="unit">Units: </label>
          <select name="unit" v-model="edit.unit">
            <option value="Kg">Kg</option>
            <option value="Piece">Piece</option>
          </select>
        </div>


        <div class="form-item">
          <label for="category">Category :</label>
          <select name="category" v-model="edit.category">
            <!-- eslint-disable vue/valid-v-for -->
            <option v-for="i in product.categories" :value="i.id" :key="i.id">
              {{ i.name }}
            </option>
          </select>
        </div>
        <div class="form-item">
          <button class="update-button" type="Submit" @click="updateData()">Update</button>
        </div>
      </form>
    </div>
</div>
<a href="http://127.0.0.1:5000/download_products_csv" target="_blank">Download Products</a>
  <table class="table">
        <thead>
            <th scope="col">Id</th>
            <th>Name</th>
            <th>Rate</th>
            <th>Quantity</th>
            <th>To do</th>
        </thead>
        <tbody>
            <tr v-for="i in product.products" :key="i.id" scope="row">
                <td scope="row">{{i.id}}</td>
                <td>{{i.name}}</td>
                <td>{{i.rate}}</td>
                <td>{{i.quantity}}</td>
                <td><button @click="delete_product(i.id)">Delete</button> |  
                  <button @click="edit_product(i)">Edit</button>
                </td>
            </tr>
        </tbody>
    </table>
  <footer class="footer-div">
    @copyright 2023
  </footer>
</template>
  
<script>
import axios from 'axios'
export default {
  name: 'add_product',
  data() {
    return {
      product: {
        name: '',
        rate: '',
        quantity: '',
        unit: '',
        category: '',
        products: [],
        categories: [],
      },
      isEditing: false,
      edit:{
        id:'',
        name: '',
        rate: '',
        quantity: '',
        unit: '',
        category: ''
      }
    }
  },
  mounted() {
    this.fetch_data();
  },
  computed: {
    approvedCategories() {
      return this.product.categories.filter(category => category.approved);
    },
  },
  methods: {
    async fetch_data() {
      try {
        const token = localStorage.getItem('token');
        const [productsResponse, categoriesResponse] = await Promise.all([
          axios.get('http://127.0.0.1:5000/product',{ headers: { Authorization: `Bearer ${token}` }}),
          axios.get('http://127.0.0.1:5000/category',{ headers: { Authorization: `Bearer ${token}` }})
        ]);

        this.product.products = productsResponse.data;
        this.product.categories = categoriesResponse.data;
        console.log('Products:', this.product.products);
        console.log('Categories:', this.product.categories);
      }
      catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async send_data() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/product', {
          name: this.product.name,
          rate: this.product.rate,
          quantity: this.product.quantity,
          unit: this.product.unit,
          category_id: this.product.category,
        });
        if (response) {
          window.location.reload();
        }
        else {
          console.log('failed');
        }
      }
      catch (error) {
        console.error('error to adding product', error)
      }
    },
    async delete_product(id) {
      axios.delete(`http://127.0.0.1:5000/product?id=${id}`)
        .then(response => {
          if (response.status === 200) {
            window.location.reload();
          }
        })
        .catch(error => {
          console.error('Error deleting item:', error);
        });
    },
    async edit_product(i) {
      this.isEditing = true;
      this.edit = {id:i.id,name:i.name,rate:i.rate,quantity:i.quantity,category:i.category_id,unit:i.unit};
    },
    async updateData(){
      axios.put(`http://127.0.0.1:5000/product`,{
        id:this.edit.id,
        name: this.edit.name,
          rate: this.edit.rate,
          quantity: this.edit.quantity,
          unit: this.edit.unit,
          category_id: this.edit.category,
      })
        .then(response => {
          if (response.status === 200) {
            window.location.reload();
          }
        })
        .catch(error => {
          console.error('Error Updating product item:', error);
        });
    }

  }
};
</script>
  
<style scoped>
@import '../assets/css/styles_add_product.css';
@import '../assets/css/styles_signup.css';
</style>