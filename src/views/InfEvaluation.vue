<template>
  <div class='container, home'>
    <InfSurvey/>
  </div>
</template>

<script>
// @ is an alias to /src
import InfSurvey from '@/components/Evaluator/InfSurvey.vue';

export default {
  components: {
    InfSurvey,
  },
};
</script>

<style lang="scss">
.home {
  padding-top: 25px;
}
</style>
