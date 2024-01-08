<template>
  <nav>
    <div class="nav-item">
      <a href="/" id="buyEasy"><b>buyEasy</b></a>
    </div>
    <div class="nav-item right">
      <a href="/">Login</a>
    </div>    
  </nav>
  <div class="login">
        <h1 class="form-heading">Sign Up</h1>
        <!--<div class="alert alert-danger" role="alert" v-if="error">
            {{ error_message }}
        </div>-->
            <form method="post">
                <div class="form-center">
                    <div class="form-item">
                        <label for="email">Email : </label>
                    </div>
                    <div class="form-item">
                        <input  type="email" name="email" v-model="email" placeholder="Enter your Email">
                    </div>
                    <div class="form-item">
                        <label for="name">Name : </label>
                    </div>
                    <div class="form-item">
                        <input v-model="name" type="text" name="name" placeholder="Enter your Name">
                    </div>
                    <div class="form-item">
                        <label for="city">City : </label>
                    </div>
                    <div class="form-item">
                        <input v-model="city" type="text" name="place" placeholder="Enter your City">
                    </div>
                    <div class="form-item">
                        <label for="name">Age : </label>
                    </div>
                    <div class="form-item">
                        <input v-model="age" type="number" name="age" placeholder="Enter your Age">
                    </div>
                    <div class="form-item">
                        <label for="name">Password : </label>
                    </div>
                    <div class="form-item">
                        <input v-model="password" type="password" name="password" placeholder="Enter your Password">
                    </div>
                    <div class="form-item">
                      <label >Role : </label>
                        <select v-model="role">
                          <option value="END_USER" >User</option>
                          <option value="Manager" >Manager</option>
                        </select>
                    </div>
                    <div class="form-item">
                        <button type="Submit" v-on:click.prevent="signup">Register</button>
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
  name: 'signup',
  data(){
    return{
      email:'',
      password:'',
      name:'',
      city:'',
      age:'',
      role:'',
    }
  },
  methods:{
      async signup(){
        try{
          if(this.role=='END_USER'){
            const result=await axios.post("http://127.0.0.1:5000/register",{
            email:this.email,
            password:this.password,
            role:this.role,
            approved:true});
            console.log(result);
            this.$router.push("/");
          }
          else{
            const result=await axios.post("http://127.0.0.1:5000/register",{
            email:this.email,
            password:this.password,
            role:this.role,
            approved:false});
            console.log(result);
            this.$router.push("/");
          }
      
    }
        catch (error){
         console.log("error",error)
    }
  }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
@import '../assets/css/styles_template.css';
@import '../assets/css/styles_signup.css';
</style>

