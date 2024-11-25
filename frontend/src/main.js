// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import 'bootstrap/dist/css/bootstrap.css';
import Vue from 'vue';
import App from './App';
import router from './router';
Vue.config.productionTip = false;
import startup from '@topomatic/tap/src/main';
import { installContext } from '@topomatic/tap/src/l10n';
/* eslint-отключение no-new */

installContext(require.context('./locales'));
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
