<template>
  <main role='main' class='container-fluid, home'>
    <Editor/>
  </main>
</template>

<script>
// @ is an alias to /src
import Editor from '@/components/Annotator/HighlightEditor.1.vue';

export default {
  components: {
    Editor,
  },
};
</script>

<style lang="scss">
.home {
  padding: 40px;
}
</style>
