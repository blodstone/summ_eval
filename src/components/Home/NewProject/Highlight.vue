<template>
    <div>
        <b-field horizontal label="Name" message="Please enter the project name">
            <b-input name="name" expanded v-model="project.name"></b-input>
        </b-field>
        <b-field horizontal label="Dataset">
            <!--TODO: Placeholder doesn't show up-->
            <b-select placeholder="Select a dataset" v-model="project.dataset_name">
                <option v-for="name in dataset.names" :i="name" :key="name">{{ name }}</option>
            </b-select>
        </b-field>
            <!--TODO: Handling error when user input 0-->
        <b-field horizontal label="# of annotation" message="Number of annotation per document">
            <b-input name="totalExpResults"
                     v-model.number="project.totalExpResults" type="number"></b-input>
        </b-field>
            <!--TODO: Instruction feature-->
        <b-field horizontal label="Specific Instruction" message="Put a specific instruction.">
            <b-switch name="guidance"></b-switch>
        </b-field>
        <button class="button is-primary" v-on:click="createProject">Create Project</button>
    </div>
</template>

<script>
const axios = require('axios');

export default {
  name: 'Highlight',
  data() {
    return {
      dataset: {
        names: [],
      },
      project: {
        name: '',
        dataset_name: '',
        type: 'highlight',
        totalExpResults: 0,
      },
    };
  },
  methods: {
    createProject() {
      // TODO: Error handling
      axios.post('/project', this.project)
        .then(() => {
          this.$toast.open({
            message: 'Project created!',
            type: 'is-success',
          });
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
  beforeCreate() {
    axios.get('dataset')
      .then((response) => {
        if (response.status === 204) {
          this.$toast.open({
            message: 'There is no dataset in database. Please insert dataset first!',
            type: 'is-danger',
          });
        }
        this.dataset.names = response.data.names;
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style scoped>

</style>
