<template>
    <span :style="charStyle" v-bind:data-type="type" v-bind:data-index="index"><slot></slot></span>
</template>

<script>
export default {
  name: 'Char',
  props: ['index', 'fgColor', 'bgColor', 'type', 'fontWeight', 'cursor'],
  data() {
    return {
      charStyle: {
        'background-color': this.bgColor,
        color: this.fgColor,
        'font-weight': this.fontWeight,
        cursor: this.cursor,
      },
    };
  },

};
</script>

<style scoped>

</style>
