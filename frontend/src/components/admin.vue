<template>
  <nav>
    <div class="nav-item">
      <a href="#" id="buyEasy"><b>buyEasy</b></a>
    </div>
    <div class="nav-item">
      <a href="/add_manager">Managers</a>
    </div>
    <div class="nav-item right">
      <a href="/">Logout</a>
    </div>
  </nav>
  <div class="update-form">

    <h1 class="form-heading">Categories</h1>
    <table class="table">
      <thead>
        <th scope="col">ID</th>
        <th>Name</th>
        <th>Status</th>
        <th> Action</th>
        <th>Delete/Edit</th>
      </thead>
      <tbody>
        <tr v-for="i in input.category" :key="i.id" scope="row">
          <td>{{ i.id }}</td>
          <td>{{ i.name }}</td>
          <td>{{ i.approved }}</td>
          <td>
            <button @click="change_status(i)">{{ i.approved ? 'Disapprove' : 'Approve' }}</button>
          </td>
          <td>
            <button @click="delete_category(i.id)">Delete</button>
            <button @click="edit_(i)">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
    <div v-if="isEditing" class="update-form">
      <h2 class="form-heading">Edit Category</h2>
      <form @submit.prevent="saveEdit">
        <label for="editName">Name:</label>
        <input type="text" v-model="editCategory.name" required>
        <button type="submit" class="update-button" @click="change_status(editCategory.id)">Save</button>
        <button class="update-button" @click="cancelEdit">Cancel</button>
      </form>
    </div>
  
  <div class="update-form">

    <h1 class="form-heading">Add Category</h1>

    <form method="post" enctype="multipart/form-data">

      <div class="form-item">
        <label for="name">Category name : </label>
        <input type="text" name="name" v-model="input.category_name">
      </div>
      <div class="form-item">
        <button class="update-button" type="Submit" v-on:click.prevent="add_">Add</button>
      </div>
    </form>

  </div>
  <footer class="footer-div">
    @copyright 2023
  </footer>
</template>

<script>
import axios from 'axios'
export default {
  name: 'admin',
  data() {
    return {
      input: {
        category: [],
      },
      isEditing: false,
      editCategory: { id: null, name: '' }
    }

  },
  mounted() {
    let user = localStorage.getItem('token');
    if (!user) {
      this.$router.push({ name: 'login' });
    }
    else {
      this.fetch_category();
    }

  },
  methods: {
    // Retriving all the data
    async fetch_category() {
      const token = localStorage.getItem('token');
      axios.get('http://127.0.0.1:5000/category',{ headers: { Authorization: `Bearer ${token}` }})
        .then(response => {
          this.input.category = response.data;
          console.log(this.input.category)
        })
        .catch(error => {
          console.error('Error fetching categories:', error);
        });

    },

    // category approval 
    async change_status(i) {
      const token = localStorage.getItem('token');
      if (this.isEditing==false){
        const response = await axios.put('http://127.0.0.1:5000/category', {
        name: i.name, approved: i.approved,id:i.id},{ headers: { Authorization: `Bearer ${token}` }});
      if (response) {
        window.location.reload();
      }
      else {
        console.log('failed');
      }
      }
      else{
        const response = await axios.put('http://127.0.0.1:5000/category', {
        name: this.editCategory.name, approved: i.approved,id:this.editCategory.id

      },{ headers: { Authorization: `Bearer ${token}` }});
      if (response) {
        window.location.reload();
      }
      else {
        console.log('failed');
      }
      }
      
    },

    // delete function for category
    async delete_category(id) {
      axios.delete(`http://127.0.0.1:5000/category?id=${id}`)
        .then(response => {
          if (response.status === 201) {
            window.location.reload();
          }
        })
        .catch(error => {
          console.error('Error deleting item:', error);
        });
    },
    edit_(category) {
      // Enter edit mode and populate the editCategory data
      this.isEditing = true;
      this.editCategory = { id: category.id, name: category.name };
    },
    cancelEdit() {
      // Reset edit state
      this.isEditing = false;
      this.editCategory = { id: null, name: '' };
    },
    async add_(){
      try {
        const response = await axios.post('http://127.0.0.1:5000/category', {
          name: this.input.category_name
        });
        console.log(response);
        window.location.reload();
      }
      catch (error) {
        console.log("something is wrong")
      }
    }
  }
};
</script>

<style scoped>
@import '../assets/css/styles_add_product.css';
@import '../assets/css/styles_signup.css';
</style>