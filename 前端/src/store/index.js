import Vue from 'vue';
import Vuex from 'vuex';
Vue.use(Vuex);
export  default  new Vuex.Store({
  state: {
    userInfo: {
      username: sessionStorage.getItem('username'),
      money: '',
    },
    host: '',
  },
  mutations: {
    initUserInfo(state, info) {
      state.userInfo.username = info.username;
      state.userInfo.money = info.money;
      sessionStorage.setItem('username', info.username);
      sessionStorage.setItem('money', info.money);
    },
    changeUserInfoMoney(state, money) {
      state.userInfo.money = money;
    }
  },
});




