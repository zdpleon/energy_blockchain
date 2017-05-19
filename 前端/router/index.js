/**
 * Created by finefenng on 3/15/17.
 */
import Vue from 'vue';
import Router from 'vue-router';
import Login from '../src/components/page/Login.vue';
import Home from '../src/components/common/home.vue';
import UserInfo from '../src/components/page/UserInformation.vue';
import MainPage from '../src/components/page/MainPage.vue';
import TopUpUser from  '../src/components/page/TopUpUser.vue';
import TradeRecord from  '../src/components/page/TradeRecord.vue';

Vue.use(Router);

const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/home',
    component: Home,
    children: [
      {
        path: 'userInfo',
        component: UserInfo,
      },
      {
        path: 'mainPage',
        component: MainPage,
      },
      {
        path: 'topUpUser',
        component: TopUpUser,
      },
      {
        path: 'tradeRecord',
        component : TradeRecord,
      }
    ]
  },
  {
    path: '/login',
    component: Login,
  }
];

export default new Router({
  routes: routes
});




