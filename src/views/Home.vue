<template>
  <div class="home">
    <header>
      <nav class="navbar navbar-expand-md navbar-dark fixed-top bg-dark">
        <a class="navbar-brand" href="#">Summ-Eval</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse"
                data-target="#navbarCollapse" aria-controls="navbarCollapse"
                aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item active">
              <router-link to="/manage" class="nav-link">Manage Projects</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/status" class="nav-link">Status</router-link>
            </li>
          </ul>
        </div>
      </nav>
    </header>
    <main class="container">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
// @ is an alias to /src

export default {
  name: 'home',
  components: {
  },
};
</script>
