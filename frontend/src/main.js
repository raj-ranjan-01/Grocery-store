import { createApp } from 'vue'
import store from "./store";

import App from './App.vue'
import router from './routes/routes'

createApp(App).use(router).use(store).mount('#app')
