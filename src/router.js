import Vue from 'vue';
import Router from 'vue-router';
import store from './store';
import Annotation from './views/Annotation.vue';
import SurveyForm from './views/SurveyForm.vue';
import Login from './views/Login.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/annotation',
      name: 'annotation',
      component: Annotation,
    },
    {
      path: '/',
      name: 'surveyForm',
      component: SurveyForm,
      beforeEnter(to, from, next) {
        if (!store.getters.isAuthenticated) {
          next('/login');
        } else {
          next();
        }
      },
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ],
});
