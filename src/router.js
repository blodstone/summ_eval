import Vue from 'vue';
import Router from 'vue-router';
import Annotation from './views/Annotation.vue';
import InfEvaluation from './views/InfEvaluation.vue';
import Login from './views/Login.vue';
import Home from './views/Home.vue';
import ManageProject from './components/Home/ManageProject.vue';
import NewProject from './components/Home/NewProject.vue';
import Status from './components/Home/Status.vue';
import Highlight from './components/Home/NewProject/Highlight.vue';
import Informativeness from './components/Home/NewProject/Informativeness.vue';
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
          path: 'informativeness',
          component: Informativeness,
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
      path: '/annotation/:project_id',
      name: 'annotation',
      component: Annotation,
    },
    {
      path: '/inf_eval/:project_id',
      name: 'inf_eval',
      component: InfEvaluation,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ],
});
