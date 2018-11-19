<template>
    <div class="container">
        <div class="tile is-ancestor">
            <div class="tile is-parent">
                <div class="tile is-child tabs">
                    <ul>
                        <li v-bind:class="{ 'is-active': isActive.highlight }"
                            v-on:click="toggleActive('highlight')">
                            <router-link to="/new/highlight">Highlight</router-link>
                        </li>
                        <li v-bind:class="{ 'is-active': isActive.evaluation }"
                            v-on:click="toggleActive('evaluation')">
                            <router-link to="/new/informativeness">Evaluation</router-link>
                        </li>
                        <li v-bind:class="{ 'is-active': isActive.fluency }"
                            v-on:click="toggleActive('fluency')">
                            <router-link to="/new/fluency">Fluency</router-link>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
        <div class="tile is-ancestor">
            <div class="tile is-parent is-5">
                <div class="tile is-child">
                    <router-view></router-view>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
  name: 'NewProject',
  data() {
    return {
      isActive: {
        highlight: true,
        evaluation: false,
        fluency: false,
      },
    };
  },
  methods: {
    toggleActive(name) {
      this.isActive.highlight = false;
      this.isActive.evaluation = false;
      this.isActive.fluency = false;
      if (name === 'highlight') {
        this.isActive.highlight = true;
      } else if (name === 'evaluation') {
        this.isActive.evaluation = true;
      } else if (name === 'fluency') {
        this.isActive.fluency = true;
      }
    },
  },
};
</script>

<style scoped>
</style>
