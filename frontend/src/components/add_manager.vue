<template>
    <nav>
      <div class="nav-item">
        <a href="#" id="buyEasy"><b>buyEasy</b></a>
      </div>
      <div class="nav-item">
        <a href="/admin">Categories</a>
      </div>
      <div class="nav-item right">
        <a href="/">Logout</a>
      </div>
    </nav>
    <div class="update-form">
  
      <h1 class="form-heading">Managers</h1>
      <table class="table">
        <thead>
          <th scope="col">ID</th>
          <th>Name</th>
          <th>Status</th>
          <th> Action</th>
        </thead>
        <tbody>
          <tr v-for="i in input.managers" :key="i.id" scope="row">
            <td>{{ i.id }}</td>
            <td>{{ i.name }}</td>
            <td>{{ i.approved }}</td>
            <td>
              <button @click="change_status(i)">{{ i.approved ? 'Disapprove' : 'Approve' }}</button>
            </td>
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
    name: 'add_manager',
    data() {
      return {
        input: {
          managers: [],
        }
      }
  
    },
    mounted() {
      let user=localStorage.getItem('token');
      if(!user){
        this.$router.push({ name :'login'});
      }
      else{
        this.fetch_category();
      }
      
    },
    methods: {
      // Retriving all the data
      async fetch_category() {
        axios.get('http://127.0.0.1:5000/managers')
          .then(response => {
            this.input.managers = response.data;
            console.log(this.input.category)
          })
          .catch(error => {
            console.error('Error fetching categories:', error);
          });
  
      },
  
      // category approval 
      async change_status(i) {
        const token = localStorage.getItem('token');
        const response = await axios.put('http://127.0.0.1:5000/managers', {
          id: i.id, approved: i.approved
  
        },{ headers: { Authorization: `Bearer ${token}` }});
        if (response) {
          window.location.reload();
        }
        else {
          console.log('failed');
        }
      },
    }
  };
  </script>
  
  <style scoped>
  @import '../assets/css/styles_add_product.css';
  @import '../assets/css/styles_signup.css';
  </style>