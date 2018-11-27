import Vue from 'vue';
import Router from 'vue-router';
import Annotation from './views/Annotation.vue';
import EvalInfDoc from './views/EvalInfDoc.vue';
import EvalInfRef from './views/EvalInfRef.vue';
import EvalFluency from './views/EvalFluency.vue';
import Login from './views/Login.vue';
import Admin from './views/Admin.vue';
import Home from './views/Home.vue';
import ManageProject from './views/ManageProject.vue';
import NewProject from './views/NewProject.vue';
import Status from './views/AnnotatingStatus.vue';
import NewAnnotation from './components/Home/NewProject/NewAnnotation.vue';
import NewEvaluation from './components/Home/NewProject/NewEvaluation.vue';
import store from './store';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      redirect: {
        name: 'admin',
      },
    },
    {
      path: '/admin',
      component: Admin,
      children: [
        {
          path: '',
          name: 'admin',
          component: Home,
        },
        {
          path: 'new',
          component: NewProject,
          children: [
            {
              path: '',
              name: 'new',
              component: NewAnnotation,
            },
            {
              path: 'annotation',
              name: 'newAnnotation',
              component: NewAnnotation,
            },
            {
              path: 'evaluation',
              name: 'newEvaluation',
              component: NewEvaluation,
            },
          ],
        },
        {
          path: 'manage',
          name: 'manage',
          component: ManageProject,
        },
        {
          path: 'status',
          name: 'status',
          component: Status,
        },
      ],
      beforeEnter(to, from, next) {
        if (!store.getters.isAuthenticated) {
          next('/login');
        } else {
          next();
        }
      },
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
