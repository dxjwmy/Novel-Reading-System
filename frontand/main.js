import { createApp } from 'vue'
import App from './App.vue'
const app = createApp(App);

import router from './router'
app.use(router);

import store from './store';
app.use(store);

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';
app.use(ElementPlus);

app.config.globalProperties.$backend = 'http://127.0.0.1:8000'

app.mount('#app');