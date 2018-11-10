<template>
  <div class='container, home'>
    <Survey/>
  </div>
</template>

<script>
// @ is an alias to /src
import Survey from '@/components/Survey/Survey.2.vue';

export default {
  components: {
    Survey,
  },
};
</script>

<style lang="scss">
.home {
  padding-top: 25px;
}
</style>
