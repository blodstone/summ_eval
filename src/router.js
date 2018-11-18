import Vue from 'vue';
import Router from 'vue-router';
import store from './store';
import Annotation from './views/Annotation.vue';
import SurveyForm from './views/SurveyForm.vue';
import Login from './views/Login.vue';
import Home from './views/Home.vue';
import ManageProject from './components/Home/ManageProject.vue';
import NewProject from './components/Home/NewProject.vue';
import Status from './components/Home/Status.vue';
import Highlight from './components/Home/NewProject/Highlight.vue';
import Evaluation from './components/Home/NewProject/Evaluation.vue';
import Fluency from './components/Home/NewProject/Fluency.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
    },
    {
      path: '/new',
      component: NewProject,
      children: [
        {
          path: '',
          component: Highlight,
        },
        {
          path: 'highlight',
          component: Highlight,
        },
        {
          path: 'evaluation',
          component: Evaluation,
        },
        {
          path: 'fluency',
          component: Fluency,
        },
      ],
    },
    {
      path: '/manage',
      component: ManageProject,
    },
    {
      path: '/status',
      component: Status,
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
