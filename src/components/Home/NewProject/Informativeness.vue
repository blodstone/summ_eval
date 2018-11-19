<template>
    <div>
        <label class="label">Create Project for Informativeness Evaluation</label>
        <b-field horizontal label="Name" message="Please enter the project name">
            <b-input name="name" expanded v-model="project.name"></b-input>
        </b-field>
        <b-field horizontal label="Dataset">
            <!--TODO: Placeholder doesn't show up-->
            <b-select placeholder="Select a dataset"
                      v-model="project.dataset_name" icon="database" icon-pack="fas">
                <option v-for="name in dataset.names" :value="name" :key="name">{{ name }}</option>
            </b-select>
        </b-field>
            <!--TODO: Handling error when user input 0-->
        <b-field horizontal label="# of evaluation" message="Number of evaluation per document">
            <b-input name="total_exp_results"
                     v-model.number="project.total_exp_results" type="number"></b-input>
        </b-field>
            <!--TODO: Instruction feature-->
        <!--<b-field horizontal label="Specific Instruction"
        message="Put a specific instruction.">-->
            <!--<b-switch name="guidance"></b-switch>-->
        <!--</b-field>-->
        <button class="button is-primary" v-on:click="createProject">Create Project</button>
    </div>
</template>

<script>
const axios = require('axios');

export default {
  name: 'Informativeness',
  data() {
    return {
      dataset: {
        names: [],
      },
      project: {
        name: '',
        dataset_name: '',
        type: 'Informativeness',
        total_exp_results: 1,
      },
    };
  },
  methods: {
    createProject() {
      axios.post('/project', this.project)
        .then(() => {
          this.$toast.open({
            message: 'Project created!',
            type: 'is-success',
          });
          this.$router.push('manage');
        })
        .catch((error) => {
          this.$toast.open({
            message: 'Project is not created! Something is wrong',
            type: 'is-danger',
          });
          console.log(error);
        });
    },
  },
  mounted() {
    axios.get('dataset')
      .then((response) => {
        if (response.status === 204) {
          this.$toast.open({
            message: 'There is no dataset in database. Please insert dataset first!',
            type: 'is-danger',
          });
        } else {
          this.dataset.names = response.data.names;
        }
      })
      .catch((error) => {
        console.log(error);
      });
  },
};
</script>

<style scoped>

</style>
