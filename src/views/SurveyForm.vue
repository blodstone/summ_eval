<template>
  <main role='main' class='container-fluid, home'>
    <Survey/>
  </main>
</template>

<script>
// @ is an alias to /src
import Survey from '@/components/Survey.vue';

export default {
  components: {
    Survey,
  },
};
</script>

<style lang="scss">
.home {
  padding: 40px;
}
</style>
