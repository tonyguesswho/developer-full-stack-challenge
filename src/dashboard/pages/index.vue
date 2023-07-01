<template>
    <div>
      <HomePage v-if="isAuthenticated" />
      <LoginForm v-else @login="submitLogin" :errorMsg="errorMessage" />
    </div>
  </template>

  <script>
  import HomePage from '~/components/HomePage.vue';
  import LoginForm from '~/components/LoginForm.vue';

  export default {
    data() {
      return {
        errorMessage: null
      };
    },
    computed: {
      isAuthenticated() {
        return this.$store.getters['auth/isAuthenticated'];
      },
    },
    methods: {
      async submitLogin(credentials) {
        try {
          await this.$store.dispatch('auth/login', credentials);
        } catch (error) {
            this.errorMessage = 'Invalid username or password';
        }
      },
    },
  };
  </script>
