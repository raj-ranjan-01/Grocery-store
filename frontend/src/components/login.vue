<template>
  <nav>
    <div class="nav-item">
      <a href="/" id="buyEasy"><b>buyEasy</b></a>
    </div>
    <div class="nav-item">
      <a href="/signup">Sign Up</a>
    </div>
  </nav>

  <div class="login">
    <h1 class="form-heading">Login</h1>
    <form>
      <div class="form-center">
        <div class="form-item">
          <label for="name">Email : </label>
        </div>
        <div class="form-item">
          <input type="text" name="email" v-model="input.email" placeholder="Enter your Username">
        </div>
        <div class="form-item">
          <label for="password">Password : </label>
        </div>
        <div class="form-item">
          <input type="password" name="password" v-model="input.password" placeholder="Enter your Password">
        </div>
        <div class="form-item">
          <button type="Submit" v-on:click.prevent="login">Login</button>
        </div>
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
  name: 'login',
  data() {
    return {
      input: {
        email: '',
        password: '',
      }
    }

  },
  mounted() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('token');
  },
  methods: {
    async login() {
      try {
        // sending the data through api
        const response = await axios.post('http://127.0.0.1:5000/userlogin', {
          email: this.input.email,
          password: this.input.password
        });
        const token = response.data;
        localStorage.setItem('user_id',token['user_id'])
        localStorage.setItem('token', token['access_token']);
        localStorage.setItem('role', token['role']);
        if (token['role'] == 'ADMIN') {
          this.$router.push({ name: 'admin' })
        }

        else if (token['role'] == 'Manager') {
          this.$router.push({ name: 'manager' })
        }

        else {
          this.$router.push({ name: 'index' });
        }
      }
      catch (error) {
        console.log('Login failed: ', error);
      }
    }
  }
}
</script>

<style scoped src="../assets/css/styles_login.css"></style>
<style scoped src="../assets/css/styles_template.css"></style>