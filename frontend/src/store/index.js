// import { create } from "core-js/core/object";
// import Vue from "vue";
import { createStore} from "vuex";

// Vue.use(Vuex);

const store = createStore({
  state () {
    return {
      cart:"",
      user_id:""
  }},
  getters: {
    user_id: state => state.user_id,
    cart:state=> state.cart
  },
  mutations: {
    add_user_id: (state, user_id) => {
      state.user_id = user_id
    },
    add_to_cart: (state, {cart_item}) => {
      state.cart = cart_item
    },
  },
  actions: {},
  modules: {},
});
export default store;