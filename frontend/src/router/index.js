import Vue from 'vue';
import Router from 'vue-router';
import MinifyURL from '../components/MinifyURL.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'MinifyURL',
      component: MinifyURL,
    },
  ],
});