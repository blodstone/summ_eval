import Vue from 'vue';
import Router from 'vue-router';
import Annotation from './views/Annotation.vue';
import SurveyForm from './views/SurveyForm.vue';

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
    },
  ],
});
