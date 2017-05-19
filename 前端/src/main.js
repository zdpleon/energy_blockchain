import Vue from 'vue'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-default/index.css'
import router from '../router/index'
import App from './App.vue'
import store from './store/index';

Vue.use(ElementUI);

  

let vm = new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');

