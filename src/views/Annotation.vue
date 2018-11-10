<template>
  <div class='container, home'>
    <Editor/>
  </div>
</template>

<script>
// @ is an alias to /src
import Editor from '@/components/Annotator/HighlightEditor.vue';

export default {
  name: 'Annotation',
  components: {
    Editor,
  },
};
</script>

<style lang="scss">
.home {
  padding-top: 25px;
}
</style>
