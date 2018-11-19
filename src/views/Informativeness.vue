<template>
  <div class='container, home'>
    <Informativeness/>
  </div>
</template>

<script>
// @ is an alias to /src
import Informativeness from '@/components/Evaluator/InformativenessEval.vue';

export default {
  components: {
    Informativeness,
  },
};
</script>

<style lang="scss">
.home {
  padding-top: 25px;
}
</style>
