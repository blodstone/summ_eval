<template>
    <div>
        Email: <input type="text" v-model="input.email" placeholder="Username">
        Password: <input type="password" v-model="input.password" placeholder="Password">
        <button type="button" v-on:click="login()">Login</button>
    </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      input: {
        email: '',
        password: '',
      },
    };
  },
  methods: {
    login() {
      if (this.input.email !== '' && this.input.password !== '') {
        this.$store.dispatch('login', {
          email: this.input.email,
          password: this.input.password,
        })
          .then(() => this.$router.push('/'))
          .catch(error => console.log(error));
      }
    },
  },
};
</script>

<style scoped>

</style>
