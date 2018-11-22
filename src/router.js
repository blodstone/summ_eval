import Vue from 'vue';
import Router from 'vue-router';
import Annotation from './views/Annotation.vue';
import EvalInfDoc from './views/EvalInfDoc.vue';
import EvalInfRef from './views/EvalInfRef.vue';
import EvalFluency from './views/EvalFluency.vue';
import Login from './views/Login.vue';
import Home from './views/Home.vue';
import ManageProject from './views/ManageProject.vue';
import NewProject from './views/NewProject.vue';
import Status from './views/Status.vue';
import NewAnnotation from './components/Home/NewProject/NewAnnotation.vue';
import NewEvaluation from './components/Home/NewProject/NewEvaluation.vue';

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
          component: NewAnnotation,
        },
        {
          path: 'annotation',
          component: NewAnnotation,
        },
        {
          path: 'evaluation',
          component: NewEvaluation,
        },
      ],
    },
    {
      path: '/manage',
      name: 'manage',
      component: ManageProject,
    },
    {
      path: '/status',
      component: Status,
    },
    {
      path: '/annotation/highlight/:project_id',
      name: 'annotation',
      component: Annotation,
    },
    {
      path: '/evaluation/informativeness_doc/:project_id',
      name: 'evalinfdoc',
      component: EvalInfDoc,
    },
    {
      path: '/evaluation/informativeness_ref/:project_id',
      name: 'evalinfref',
      component: EvalInfRef,
    },
    {
      path: '/evaluation/fluency/:project_id',
      name: 'fluency',
      component: EvalFluency,
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
    },
  ],
});
