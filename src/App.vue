<template>
  <div class="clearfix">
      <nav class="navbar" role="navigation" aria-label="main navigation">
        <div class="container is-fluid">
          <div class="navbar-brand" href="#">
            <a class="navbar-item">Summ-Eval</a>
          </div>
            <div id="navbarBasicExample" class="navbar-menu">
              <div class="navbar-start">
                <div class="navbar-item has-dropdown is-hoverable">
                  <a class="navbar-link">
                    Projects
                  </a>

                  <div class="navbar-dropdown">
                    <router-link class="navbar-item" to="/new">
                      New...
                    </router-link>
                    <router-link class="navbar-item" to="/manage">
                      Manage...
                    </router-link>
                  </div>
                </div>
                <router-link class="navbar-item" to="/status">
                  Status
                </router-link>
              </div>
            </div>
          </div>
      </nav>
    <router-view/>
  </div>
</template>
<style lang="scss">
@mixin clearfix() {
  &::after {
    display: block;
    content: "";
    clear: both;
  }
}

// Usage as a mixin
.element {
  @include clearfix;
}
</style>
