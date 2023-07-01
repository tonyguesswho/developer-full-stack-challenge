<template>
    <div>
      <nav>
        <b-navbar toggleable="lg" type="light" variant="light">
          <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
          <b-navbar-brand href="/">Library App</b-navbar-brand>
          <b-collapse id="nav-collapse" is-nav>
            <b-navbar-nav class="mr-auto">
              <b-nav-item v-if="authenticated" to="/authors">Authors</b-nav-item>
              <b-nav-item v-if="authenticated" to="/books">Books</b-nav-item>
            </b-navbar-nav>
            <b-navbar-nav v-if="!authenticated">
              <b-nav-item to="/">Login</b-nav-item>
            </b-navbar-nav>
            <b-navbar-nav v-if="authenticated">
              <b-nav-item @click="logout">Logout</b-nav-item>
            </b-navbar-nav>
          </b-collapse>
        </b-navbar>
      </nav>
      <main>
        <Nuxt />
      </main>
      <footer>
      </footer>
    </div>
  </template>

  <script>
  export default {
    computed: {
      authenticated() {
        return this.$store.getters['auth/isAuthenticated'];
      },
    },
    methods: {
      logout() {
        this.$store.dispatch('auth/logout');
      },
    },
  };
  </script>

  <style>
  .navbar-nav {
    justify-content: center;
  }

  .navbar-nav:last-child {
    margin-left: auto;
  }
  </style>
