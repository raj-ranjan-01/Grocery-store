import { createRouter, createWebHistory } from 'vue-router';
import login from '../components/login.vue';
import signup from '../components/signup.vue';
import index from '../components/index.vue';
import admin from '../components/admin.vue';
import manager from '../components/manager.vue';
import add_manager from '../components/add_manager.vue';
import add_product from '../components/add_product.vue';
import cart from '../cart/cart.vue';
import add_cart from '../cart/add_cart.vue';
const routes = [
  { 
    name:'login',
    path: '/', 
    component: login 
},
  { 
    name:'signup',
    path: '/signup', 
    component: signup 
},
    {
        name:'index',
        path:'/index',
        component: index
    },
    {
      name:'admin',
      path:'/admin',
      component:admin
    },
    {
      name:'manager',
      path:'/manager',
      component:manager
    },
    {
      name:'add_manager',
      path:'/add_manager',
      component:add_manager
    },
    {
      name:'add_product',
      path:'/add_product',
      component:add_product
    },
    {
      name:'cart',
      path:'/cart',
      component:cart
    },
    {
      name:'add_cart',
      path:'/add_cart',
      component:add_cart
    },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});
export default router