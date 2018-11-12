import Vue from 'vue';
import Router from 'vue-router';
import store from './store';
import Annotation from './views/Annotation.vue';
import SurveyForm from './views/SurveyForm.vue';
import Login from './views/Login.vue';
import Home from './views/Home.vue';
import ManageProject from './components/Home/ManageProject.vue';
import Status from './components/Home/Status.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      children: [
        {
          path: 'manage',
          component: ManageProject,
        },
        {
          path: 'status',
          component: Status,
        },
      ],
    },
    {
      path: '/annotation',
      name: 'annotation',
      component: Annotation,
    },
    {
      path: '/survey',
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
